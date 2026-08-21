# Reproduction of Brusini, Seminck, Amsili & Christophe (2021)

**Target model:** *The Acquisition of Noun and Verb Categories by Bootstrapping
From a Few Known Words: A Computational Model.* Front. Psychol. 12:661479.
doi:10.3389/fpsyg.2021.661479
**Original code/data:** github.com/oseminck/bootstrapping_model
**Corpus:** Lyon corpus (Marie & Theotime), CHILDES / PhonBank — *not redistributed here;*
obtain from https://phonbank.talkbank.org/access/French/Lyon.html

This report documents an independent, deterministic reproduction of the model.
It is a reproduction/robustness exercise, not new theory, and makes no claim
beyond what is shown below.

---

## 1. What the model does

For a low-frequency target word, the model looks at its two-word local context,
replaces any context word belonging to a small *semantic seed* (concrete nouns /
action verbs) with its category (N/V), and predicts the category most often seen
in that context slot during training, backing off from trigram to bigram. Three
context types are compared — left, framing (one word either side), right — plus a
stochastic chance baseline. Seed size is varied from 8 nouns / 1 verb up to the
full lexicon.

## 2. Reconstruction of a missing preprocessing step

The original `models_and_errors.py` imports `from call_my_corpus import
utterances` and loads two pickles (`utterances`, `voca`) that are not present in
the repository, and `call_my_corpus.py` itself is absent. This step was
reconstructed (`call_my_corpus.py`) by building the corpus from the corrected
CoNLL files and pickling the utterance list and vocabulary. The reconstruction
reproduces the authors' reported corpus size **exactly**:

| Quantity | Paper | This reproduction |
| --- | --- | --- |
| Utterances | 58,241 | 58,241 |
| Noun tokens retagged | 6,911 | 6,911 (corrected corpus as shipped) |

## 3. Determinism

The original evaluation is not reproducible as shipped, for two reasons, both
fixed in the deterministic runner (`v1_run.py`) without altering the original
model code (only the class/function definitions are reused):

1. **Corpus ordering.** The utterance list was built from an unsorted `os.walk`,
   and the ten mini-corpora are index-slices of that list, so results depend on
   filesystem order. V1 reads files in fixed numeric order.
2. **Unseeded baseline.** The chance model uses `np.random.choice` with no seed.
   V1 seeds NumPy per model.

V1 is bit-for-bit identical across repeated runs (verified by diff).

## 4. Validation against the published results

Mean precision / recall over the 10 mini-corpora (V1, deterministic).
Repo context names map to the paper as: gauche→left, imbrique→framing, droit→right.

| Context | Seed | Prec N | Prec V | Rec N | Rec V |
| --- | --- | --- | --- | --- | --- |
| **left** | 8N/1V | 0.886 | 0.884 | 0.131 | 0.064 |
| left | 64N/6V | 0.905 | 0.795 | 0.421 | 0.248 |
| left | 192N/24V | 0.906 | 0.817 | 0.571 | 0.374 |
| **framing** | 8N/1V | 0.838 | 0.845 | 0.303 | 0.042 |
| framing | 64N/6V | 0.869 | 0.741 | 0.626 | 0.228 |
| framing | 192N/24V | 0.868 | 0.748 | 0.696 | 0.383 |
| **right** | 8N/1V | 0.450 | 0.617 | 0.017 | 0.031 |
| right | 192N/24V | 0.638 | 0.527 | 0.204 | 0.321 |
| **chance** | 8N/1V | 0.552 | 0.280 | 0.009 | 0.013 |

Published claims reproduced:

- Left/framing precision ≈ 0.90 (N) / ≈ 0.80 (V), roughly flat across seed size.
- Recall low for the smallest seed, rising monotonically with seed size.
- Right context clearly poorest of the three context models.
- Framing has a noun-recall advantage over left.
- Verb precision is highest at the smallest seed and declines slightly as it grows.
- Context models greatly outperform the chance baseline.

## 5. Honest caveats

- This reproduces the paper's **qualitative findings and approximate magnitudes**,
  not its exact per-fold figures: the corpus ordering behind the original folds
  was not shipped, and the baseline is stochastic, so cell-exact replication of
  the published figure is not possible from the released artifacts.
- The repository runs one seed size (V5 = 192N/24V) beyond those in the paper's
  Table 1 (which stops at V4 = 128N/12V, then the full-lexicon Vm); it is included
  here for completeness and labelled as a superset.
- A latent bug remains in the original `main` (an undefined variable in the
  zero-denominator branch for verb precision); it is not triggered by this corpus
  but is noted rather than silently patched, to keep the reused code faithful.

## 6. Reproduce

```
# place the corrected corpus at ./corrected_corpus/  (from the original repo / CHILDES)
python3 call_my_corpus.py     # rebuild the utterances / voca pickles
python3 v1_run.py             # deterministic run -> v1_resultats/
```
