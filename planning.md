# TakeMeter Planning

## Project Status

- I completed Milestone 1: community review and taxonomy design.
- I completed Milestone 2: written specification.
- I completed Milestone 3: collection, annotation, and human review.

My final dataset contains 200 public comments from r/LetsTalkMusic. I used Codex
to pre-label every row, and then I reviewed the annotations and confirmed them
without corrections. All `human_reviewed` values are `yes`.

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
mark six especially difficult cases in the `notes` column. Every row contains
`ai_prelabeled=yes` in my review workbook. I subsequently reviewed the
annotations, confirmed the proposed labels without corrections, and recorded
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

I reviewed the annotations and confirmed the proposed labels without changes.
My review workbook records `human_reviewed=yes` for all 200 rows, while my
notebook CSV intentionally contains only `text`, `label`, and `notes`. I
recalculated the final distribution and confirmed that it still passes the
balance requirements, so my dataset is ready for the Colab baseline and
training pipeline.
