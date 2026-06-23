# TakeMeter Planning

## Project Status

- I completed Milestone 1: community review and taxonomy design.
- I completed Milestone 2: written specification.
- I completed Milestone 3: collection, annotation, and human review.
- I completed Milestone 4: zero-shot baseline evaluation.
- I completed Milestone 5: DistilBERT fine-tuning and test evaluation.
- I completed the written Milestone 6 evaluation; the demo recording remains.

My final dataset contains 200 public comments from r/LetsTalkMusic. I used Codex
to pre-label every row, and then I reviewed the annotations and made minor
corrections where needed. All `human_reviewed` values are `yes`.

## Milestone 1: Community and Label Taxonomy

### Community

I chose [r/LetsTalkMusic](https://www.reddit.com/r/LetsTalkMusic/), a text-heavy
community where participants discuss artists, albums, genres, music history,
listening habits, concerts, and the music industry. I found that its comments
range from evidence-rich historical or musical arguments to reasoned personal
interpretations and one-line reactions, making it a strong setting for my
discourse-support classifier.

I want my classifier to measure **how a response supports its central point**,
not whether the musical opinion is correct or whether I agree with it. I chose
this distinction because concrete support gives other participants something
specific to examine, challenge, or build on.

### Community Review Before Finalizing Labels

I read an initial sample of 40 comments before I locked the taxonomy. I found 24
`supported_analysis`, 9 `reasoned_opinion`, and 7
`unelaborated_response` candidates. I then read the remaining 160 comments to
stress-test coverage across ten threads, and I did not need a catch-all `other`
label.

### Labels

#### `supported_analysis`

**Definition:** The response makes or answers a musical claim with concrete
details, examples, comparisons, facts, or firsthand observations and connects
that support to its conclusion.

Clear dataset examples:

1. `ltm043` compares a stadium seat hundreds of feet from the performers with
   a club show close enough to fist-bump the band, then connects that difference
   to why the club felt more special.
2. `ltm181` cites several releases and dates after Disco Demolition Night to
   support the conclusion that disco remained popular after July 1979.

Uncertain example:

- `ltm039` says the Sex Pistols should not be called a boy band because they
  wrote their own songs. It is short, but the checkable fact directly rebuts the
  claim, so the final label is `supported_analysis`.

#### `reasoned_opinion`

**Definition:** The response states a position, interpretation, or personal
practice and gives a distinct rationale, but does not substantiate that
rationale with concrete, checkable detail.

Clear dataset examples:

1. `ltm056` argues that neither underground nor mainstream concerts are better
   because large productions and small shows provide fundamentally different
   experiences.
2. `ltm125` argues that musical genres are retrospective labels rather than
   universal, objective truths.

Uncertain example:

- `ltm080` wonders whether positive ICP posts are propaganda because three
  similar recommendations appeared in the commenter's feed. That observation
  is a reason, but it is too weak and undeveloped to count as supported
  analysis, so the final label is `reasoned_opinion`.

#### `unelaborated_response`

**Definition:** The response gives a verdict, reaction, question,
acknowledgment, joke, or factual answer without a distinct supporting
rationale.

Clear dataset examples:

1. `ltm071`: "Yeah they aged really well."
2. `ltm187`: "Bee Gees made infinitely better music, too."

Uncertain example:

- `ltm112` describes a goal to hear 100 albums and an album-bingo board. It has
  several details, but it does not explain or defend a claim. It is labeled
  `unelaborated_response`; length alone is not analysis.

### Annotation Decision Ladder

I apply the rules in this order:

1. If the response contains concrete support **and explains or clearly implies
   how that support answers the central point**, label it `supported_analysis`.
2. Otherwise, if it gives a distinct rationale that adds information beyond the
   verdict, label it `reasoned_opinion`.
3. Otherwise, label it `unelaborated_response`.

Additional rules:

- A named artist, album, song, genre, statistic, or technical term is not
  automatically evidence; it must support the response's point.
- A list of examples with no explanation of what the examples demonstrate is
  `unelaborated_response`.
- Firsthand experience can count as concrete support when the response connects
  the observed details to its conclusion.
- A `because` clause counts only when it adds a real rationale rather than
  restating the verdict.
- For mixed comments, label the most developed support level used for the
  central point. Do not let a brief side reaction determine the label.
- Judge only the text present. Do not supply evidence from personal knowledge
  or decide based on agreement with the opinion.

### Hardest Anticipated Edge Case

I expect the hardest boundary to be between `supported_analysis` and
`reasoned_opinion` when a response sounds technical or mentions one concrete
detail without showing why it supports the conclusion. My test is to remove the
evaluative language and ask whether the remaining material lets another reader
identify the evidence and understand its connection to the claim. If both are
present, I use `supported_analysis`; if the explanation remains general, I use
`reasoned_opinion`.

I identified a second hard boundary between `reasoned_opinion` and
`unelaborated_response`. I require a reason to add new information. "This album
is boring because every song is boring" remains unelaborated, while "this album
is boring because every track uses the same dynamics" supplies a distinct,
though still general, rationale.

### Mutual Exclusivity and Coverage

My decision ladder assigns exactly one label based on the strongest support
used for the central point. I was able to use it for all 200 comments, including
questions, jokes, brief factual replies, and detailed personal accounts. My
largest class is 53.5%, so the taxonomy is meaningfully discriminating rather
than collapsing almost everything into one category.

## Milestone 2: Written Specification

### Data Collection Plan

I collected 200 public r/LetsTalkMusic comments from ten discussion threads,
with 20 comments per thread. My topics include a new Olivia Rodrigo album, the
Sex Pistols, underground concerts, ICP, Kate Bush, album listening habits, the
origins of heavy metal, B-side hits, Reddit music taste, and disco history. I
sampled several topics to reduce the risk that my classifier learns a single
artist or genre instead of the intended support distinction.

I kept only the three notebook-facing columns in my final training CSV: `text`,
`label`, and `notes`. I preserved the anonymous dataset ID, permalink,
source-thread title, AI-assistance flag, and human-review flag in a separate
annotation-review workbook. I omitted Reddit usernames and collection-only
metadata from the training CSV. The notebook will create the 70%/15%/15% train,
validation, and test split, so I did not include a manual split column.

My collection target is at least 40 examples per label (20% of 200). If a label
falls below 40, I will collect more public comments from threads likely to
contain that response type. If any label rises above 70%, I will focus my
additional collection on the other two labels before training.

### Evaluation Metrics

I will evaluate my model and the Groq zero-shot baseline on the same locked test
set using:

- **Accuracy**, to summarize the share of all correct predictions.
- **Per-class precision, recall, and F1**, to reveal whether the model
  over-predicts or misses any one support level.
- **Macro-averaged F1**, to give all three labels equal importance even if the
  final human-reviewed distribution is not perfectly balanced.
- **A confusion matrix**, to show which boundary fails and in which direction,
  especially `supported_analysis` versus `reasoned_opinion`.
- **Specific error review**, to determine whether mistakes arise from ambiguous
  definitions, inconsistent annotation, sarcasm, missing conversational
  context, or insufficient training examples.

I will not rely on accuracy alone because my model could perform reasonably
overall while rarely recognizing the smallest class. Macro F1 and per-class
metrics will make that failure visible.

### Definition of Success

I will consider this class project successful if I achieve:

- fine-tuned test accuracy of at least 70%;
- macro F1 of at least 0.70;
- F1 of at least 0.60 for every label; and
- a meaningful improvement over both the majority-class strategy and the Groq
  zero-shot baseline, defined as at least five percentage points in accuracy or
  macro F1.

For real community deployment, I would use a stricter threshold: macro F1 of at
least 0.80, no class below 0.75 F1, and human review for low-confidence or
moderation-sensitive predictions. I would treat the classifier as a descriptive
aid, not as an automatic judgment of whether a person's taste is good.

### AI Tool Plan

#### Label stress-testing

I asked Codex to test my proposed boundaries against cases such as a comment
that uses technical vocabulary without an explanation, a detailed personal
answer with no argument, a single fact that directly rebuts a claim, and a list
of examples with no conclusion. Based on this testing, I renamed my original
`bare_assertion` category to `unelaborated_response`, which more accurately
covers questions, acknowledgments, jokes, and short factual replies in my real
dataset.

#### Annotation assistance

I used Codex to pre-label all 200 comments with my written decision ladder and
mark six especially difficult cases in the review workbook's `notes` column. I
also included those six explanations in the notebook CSV's `notes` column and
left the other 194 note cells blank. Every row contains `ai_prelabeled=yes` in my
review workbook. I subsequently reviewed the annotations, confirmed the proposed labels and made minor corrections, and recorded
all `human_reviewed` values as `yes`. I will disclose this assistance and my
review process in the README's final AI usage section.

#### Failure analysis

After evaluation, I plan to give the wrong predictions to an AI tool and ask it
to propose patterns involving comment length, sarcasm, quotations, factual
lists, firsthand anecdotes, missing parent-comment context, and the two
adjacent label boundaries. I will manually check each proposed pattern against
the complete misclassified texts and confusion matrix before I report it.

## Milestone 3: Collection and Annotation Record

### Dataset Audit

- Source community: r/LetsTalkMusic
- Public comments: 200
- Source threads: 10
- Comments per source thread: 20
- Empty, deleted, or removed comments: 0
- Duplicate comment bodies: 0
- Training file: `takemeter_labeled_data.csv`
- Annotation-review workbook: `takemeter_annotation_review.xlsx`

### Final Human-Reviewed Distribution

| Label | Count | Share |
|---|---:|---:|
| `supported_analysis` | 107 | 53.5% |
| `reasoned_opinion` | 50 | 25.0% |
| `unelaborated_response` | 43 | 21.5% |
| **Total** | **200** | **100.0%** |

No label exceeds 70%, and every label exceeds the 20% collection target.

### Difficult Annotation Decisions

1. **`ltm039`: `supported_analysis` vs. `reasoned_opinion`.** The response is
   only one sentence, but the fact that the Sex Pistols wrote their own songs
   directly rebuts the boy-band comparison. The evidence-to-claim connection is
   clear, so I labeled it `supported_analysis`.
2. **`ltm080`: `reasoned_opinion` vs. `unelaborated_response`.** The commenter
   suspects ICP propaganda after seeing three similar posts. Three appearances
   do not strongly prove coordination, but they are a distinct rationale, so I
   labeled it `reasoned_opinion`.
3. **`ltm112`: `reasoned_opinion` vs. `unelaborated_response`.** The response
   includes a numerical listening goal and bingo-board details but makes no
   supported claim. I labeled it `unelaborated_response` because comment length
   does not determine discourse support.
4. **`ltm129`: joke vs. `supported_analysis`.** The hip-hop comparison is
   playful, but the instruction to listen to Ringo's second-verse performance is
   a checkable musical cue, so I labeled it `supported_analysis`.
5. **`ltm141`: `supported_analysis` vs. `unelaborated_response`.** The response
   lists several B-sides but does not explain what their success demonstrates.
   I labeled it `unelaborated_response`.
6. **`ltm149`: `supported_analysis` vs. `unelaborated_response`.** The delayed
   release of "Cruel Summer" is relevant, but the response does not connect it
   to an explanation of success, so I labeled it `unelaborated_response`.

### Human Review Completion

I reviewed the annotations and made minor corrections where needed.
My review workbook records `human_reviewed=yes` for all 200 rows, while my
notebook CSV intentionally contains only `text`, `label`, and `notes`. I
recalculated the final distribution and confirmed that it still passes the
balance requirements, so my dataset is ready for the Colab baseline and
training pipeline.

## Milestone 4: Zero-Shot Baseline

### Prompt Design

I copied my three label definitions from this planning document into the Groq
classification prompt without changing their wording. The prompt also used my
decision ladder and required the model to respond with only one of the three
exact label names. I used newly written examples rather than comments from my
labeled dataset because the dataset examples could appear in the locked test
split. This kept the baseline prompt from revealing labels for possible test
examples.

### Baseline Results

I ran `llama-3.3-70b-versatile` on the locked 30-example test set before
fine-tuning. All 30 responses were parseable.

| Label or metric | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| `supported_analysis` | 1.000 | 0.500 | 0.667 | 16 |
| `reasoned_opinion` | 0.533 | 1.000 | 0.696 | 8 |
| `unelaborated_response` | 0.714 | 0.833 | 0.769 | 6 |
| Macro average | 0.749 | 0.778 | 0.711 | 30 |
| Weighted average | 0.818 | 0.700 | 0.695 | 30 |

Overall accuracy was 0.700, or 21 correct predictions out of 30. The complete
machine-readable results are saved in `baseline_results.json`.

### Baseline Reflection

The baseline performed best on `unelaborated_response`, while its main weakness
was recognizing `supported_analysis`. It correctly identified only 8 of the 16
supported-analysis examples. The reported class counts imply that it labeled 6
of the remaining supported analyses as `reasoned_opinion` and 2 as
`unelaborated_response`. It correctly identified all 8 reasoned opinions, but
the additional false positives reduced that class's precision.

This pattern supports my hypothesis that a general model is conservative about
calling a response supported analysis when the evidence-to-claim connection is
implicit. I expect fine-tuning on my annotated examples to improve the boundary
between `supported_analysis` and `reasoned_opinion`.

### Fine-Tuning Target

To meet my definition of a meaningful improvement, the fine-tuned model must
beat the baseline by at least five percentage points in accuracy or macro F1.
Because the test set has 30 examples, the next attainable accuracy at least five
points above 0.700 is 23 correct predictions, or 0.767. The corresponding macro
F1 target is at least 0.761. I will also retain my requirements of at least 0.60
F1 for every label and at least 0.70 overall macro F1.

## Milestone 5: Fine-Tuning Record

I fine-tuned `distilbert-base-uncased` on a T4 GPU using the starter notebook.
The stratified split contained 140 training, 30 validation, and 30 test
examples. I retained the original settings of three epochs, learning rate
`2e-5`, training batch size 16, evaluation batch size 32, weight decay 0.01,
50 warmup steps, and random seed 42. I kept these defaults for the report so the
result reflects the provided pipeline without choosing settings based on the
test set.

Validation loss decreased from 1.083 to 0.998, but validation accuracy stayed
at 0.533 for all three epochs. On the locked test set, the model also achieved
0.533 accuracy. Its per-class F1 scores were 0.696 for
`supported_analysis` and 0.000 for both `reasoned_opinion` and
`unelaborated_response`. The confusion matrix showed that it predicted
`supported_analysis` for all 30 examples.

The fine-tuned model therefore missed my success criteria. It scored 0.167
below the Groq baseline in accuracy, had macro F1 of 0.232 rather than at least
0.70, and failed the minimum 0.60 F1 requirement for two labels. A separate
warmup-three checkpoint was exploratory only; I did not evaluate it or replace
the default run with it after viewing the locked test results.

## Milestone 6: Evaluation Notes

### Verified Failure Pattern

I used Codex to propose patterns across the 14 wrong predictions and then
checked those suggestions against every error. I considered short length,
sarcasm, named artists or songs, factual answers, and long personal responses.
Those features appeared in individual examples, but I rejected them as the
main explanation because the errors covered many lengths, topics, and writing
styles. The decisive pattern was that every one of the eight true
`reasoned_opinion` examples and every one of the six true
`unelaborated_response` examples was predicted as `supported_analysis`.

The training distribution was 75, 35, and 30 examples across the three labels,
and the 50 warmup steps exceeded the run's 27 optimization steps. Combined with
confidence scores near one third and validation accuracy fixed at the majority
rate, this supports a diagnosis of majority-class collapse rather than one
isolated semantic boundary failure.

### Next Experimental Design

If I repeated the project with a new locked test set, I would use a warmup ratio
near 10%, choose checkpoints using macro F1, and compare class-weighted loss or
balanced sampling against the unchanged default. I would also collect more
minority-class examples that mention artists, songs, statistics, or personal
details without using those details as evidence. I would not tune further on
the current 30-example test set because it has already been examined.

## Stretch Feature Plan

### Inter-Annotator Reliability

I will give a blinded, balanced set of 30 comments to another person and ask
them to label every item independently with the same definitions and decision
ladder. I will not show them my labels until they return the completed
`inter_annotator_reliability.xlsx` workbook. I will then calculate percentage
agreement and Cohen's kappa and examine every disagreement by label pair. This
stretch feature is complete only after another person returns the workbook.

### Confidence Calibration

I used the fine-tuned model's saved test probabilities to compare average
confidence with empirical accuracy, calculate expected calibration error and a
multiclass Brier score, and report confidence separately for correct and
incorrect predictions. All 30 predictions landed in the 0.3–0.4 bin, with mean
confidence 0.3546 and accuracy 0.5333. Expected calibration error was 0.1787,
and the multiclass Brier score was 0.6573. Mean confidence was 0.3536 for
correct predictions and 0.3558 for incorrect predictions, so confidence did
not distinguish successful classifications from errors. I therefore rejected
any claim that the confidence scores provided a useful ranking of certainty.

### Error Pattern Analysis

I completed a systematic review of all 14 errors rather than selecting only
three examples. I tested possible patterns involving length, sarcasm, factual
answers, named musical references, and personal anecdotes. I retained the
majority-class collapse as the supported pattern and rejected the surface-level
patterns as primary explanations because they did not cover the complete error
set.

### Deployed Interface

I added a small Gradio interface that accepts a new comment and displays all
three label probabilities using the trained model already loaded in Colab. The
interface uses the same 256-token truncation as evaluation and is documented as
a diagnostic demonstration rather than a production community moderation tool.
The deployment stretch is complete only after I launch the interface and verify
that it returns a label and confidence scores for a new comment.
