"""Gradio interface for the TakeMeter fine-tuned classifier.

Use ``launch_interface`` directly in the Colab notebook after training, or run
this file with ``--model-dir`` when a saved Hugging Face checkpoint is local.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping


DEFAULT_LABELS = {
    0: "supported_analysis",
    1: "reasoned_opinion",
    2: "unelaborated_response",
}


def _normalize_labels(id_to_label: Mapping) -> dict[int, str]:
    """Return an integer-keyed label map in classifier output order."""

    normalized = {int(key): str(value) for key, value in id_to_label.items()}
    expected = list(range(len(normalized)))
    if sorted(normalized) != expected:
        raise ValueError(f"Label IDs must be consecutive from 0; received {sorted(normalized)}")
    return normalized


def build_interface(model, tokenizer, id_to_label=DEFAULT_LABELS, max_length: int = 256):
    """Build a Gradio interface around an already loaded classifier."""

    try:
        import gradio as gr
        import torch
    except ImportError as exc:  # pragma: no cover - depends on runtime packages
        raise RuntimeError(
            "Install the interface dependencies with: pip install -r requirements.txt"
        ) from exc

    labels = _normalize_labels(id_to_label)
    model.eval()
    device = next(model.parameters()).device

    def classify(text: str) -> dict[str, float]:
        cleaned = (text or "").strip()
        if not cleaned:
            raise gr.Error("Enter a post or comment before classifying it.")

        encoded = tokenizer(
            cleaned,
            truncation=True,
            max_length=max_length,
            padding=True,
            return_tensors="pt",
        )
        encoded = {name: tensor.to(device) for name, tensor in encoded.items()}

        with torch.no_grad():
            logits = model(**encoded).logits[0]
            probabilities = torch.softmax(logits, dim=-1).detach().cpu().tolist()

        return {
            labels[index]: float(probabilities[index])
            for index in range(len(probabilities))
        }

    return gr.Interface(
        fn=classify,
        inputs=gr.Textbox(
            lines=8,
            label="r/LetsTalkMusic post or comment",
            placeholder="Paste a new public music-discussion comment here...",
        ),
        outputs=gr.Label(num_top_classes=len(labels), label="Predicted support level"),
        title="TakeMeter",
        description=(
            "Classifies how a music-community response supports its central point. "
            "This classroom model is diagnostic and should not be used for moderation."
        ),
        examples=[
            ["That album aged really well."],
            ["I prefer the earlier records because they feel more focused."],
            [
                "The live version works better because the slower tempo leaves space "
                "around the vocal, which makes the final chorus feel larger."
            ],
        ],
        flagging_mode="never",
    )


def launch_interface(
    model,
    tokenizer,
    id_to_label=DEFAULT_LABELS,
    *,
    share: bool = True,
    max_length: int = 256,
):
    """Launch the interface and optionally create a temporary public Gradio URL."""

    demo = build_interface(model, tokenizer, id_to_label, max_length=max_length)
    return demo.launch(share=share)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the TakeMeter Gradio interface.")
    parser.add_argument(
        "--model-dir",
        required=True,
        help="Path to a saved Hugging Face sequence-classification checkpoint.",
    )
    parser.add_argument(
        "--tokenizer-name",
        default="distilbert-base-uncased",
        help="Tokenizer name or local path (default: distilbert-base-uncased).",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Ask Gradio to create a temporary public link.",
    )
    args = parser.parse_args()

    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)
    config_labels = getattr(model.config, "id2label", None) or DEFAULT_LABELS
    launch_interface(model, tokenizer, config_labels, share=args.share)


if __name__ == "__main__":
    main()
