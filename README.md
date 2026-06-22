# TakeMeter

For TakeMeter, I am building a three-class text classifier to study how
participants in [r/LetsTalkMusic](https://www.reddit.com/r/LetsTalkMusic/)
support their musical claims. I designed the project to distinguish
evidence-backed discussion from general reasoning and unelaborated responses,
not to judge whether a person's musical taste is correct.

## Current Status

- I completed Milestones 1–3.
- I have not started the baseline, fine-tuning, or evaluation milestones yet.

## Label Taxonomy

### `supported_analysis`

A response makes or answers a musical claim with concrete details, examples,
comparisons, facts, or firsthand observations and connects that support to its
conclusion.

Examples from the dataset:

- `ltm043` compares the viewing distance at a stadium and club show to explain
  why the club experience felt more special.
- `ltm181` cites releases after Disco Demolition Night to argue that disco did
  not suddenly disappear in 1979.

### `reasoned_opinion`

A response states a position, interpretation, or personal practice and gives a
distinct rationale, but does not substantiate it with concrete, checkable
detail.

Examples from the dataset:

- `ltm056` argues that mainstream and underground concerts are different
  experiences rather than one being inherently better.
- `ltm125` argues that genres are retrospective labels rather than objective
  truths.

### `unelaborated_response`

A response gives a verdict, reaction, question, acknowledgment, joke, or factual
answer without a distinct supporting rationale.

Examples from the dataset:

- `ltm071`: "Yeah they aged really well."
- `ltm187`: "Bee Gees made infinitely better music, too."

I documented my complete definitions, decision ladder, edge cases, data plan,
evaluation plan, and success criteria in [planning.md](planning.md).

## Dataset

I collected 200 public comments from ten r/LetsTalkMusic discussion threads,
with 20 comments sampled from each thread. I found no empty, deleted, removed,
or duplicate comment bodies, and I excluded usernames from the training file.

Final human-reviewed distribution:

| Label | Count | Share |
|---|---:|---:|
| `supported_analysis` | 107 | 53.5% |
| `reasoned_opinion` | 50 | 25.0% |
| `unelaborated_response` | 43 | 21.5% |

I saved the notebook-ready data in
[takemeter_labeled_data.csv](takemeter_labeled_data.csv), which contains exactly
`text`, `label`, and `notes`. I kept the additional review information in the
[annotation review workbook](takemeter_annotation_review.xlsx), including label
drop-downs, difficult-case notes, provenance links, and a `human_reviewed`
status column.

## Annotation Process and Human Review

I used Codex to read and pre-label all 200 comments using the decision ladder in
`planning.md`. I documented six especially ambiguous rows with annotation
notes. I then reviewed the annotations and confirmed them without corrections.
Every row in my review workbook is marked `ai_prelabeled=yes` and
`human_reviewed=yes`, while I omitted those tracking fields from the notebook
CSV. My final distribution satisfies my planned balance requirements.

## AI Usage So Far

1. I asked Codex to stress-test my taxonomy against boundary cases. Based on
   that output, I replaced the overly narrow `bare_assertion` label with
   `unelaborated_response` so my taxonomy also covers questions,
   acknowledgments, jokes, and short factual replies.
2. I asked Codex to pre-label all 200 comments and identify difficult cases. It
   identified six, and I reviewed and accepted the proposed labels without
   corrections.

I will add my training details, baseline results, evaluation metrics, failure
analysis, reflection, and demo information in later milestones.
