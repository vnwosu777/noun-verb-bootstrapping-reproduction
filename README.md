# Reproducing a semantic-seed model of noun/verb acquisition (Brusini et al., 2021)

An independent, deterministic reproduction and validation of the computational model in **Brusini, Seminck, Amsili & Christophe (2021)**, *The Acquisition of Noun and Verb Categories by Bootstrapping From a Few Known Words*
([Front. Psychol. 12:661479](https://doi.org/10.3389/fpsyg.2021.661479)).

Original model code and data: **[github.com/oseminck/bootstrapping_model](https://github.com/oseminck/bootstrapping_model)**.

## What the model does

For a low-frequency target word, the model reads its two-word local context, replaces any context word belonging to a small *semantic seed* (concrete nouns / action verbs) with its category (N/V), and predicts the category most often seen in that context slot during training — backing off from trigram to bigram. Three context types are compared (left, framing, right) against a stochastic chance baseline, across semantic seeds ranging from 8 nouns / 1 verb up to the full lexicon. It is trained and tested on French child-directed speech from the Lyon
corpus (CHILDES).

## What this repository adds

- **`call_my_corpus.py`** — reconstruction of a preprocessing stage that the original driver imports but that is not shipped in the repository (it builds  the `utterances` and `voca` artifacts the model loads).
- **`v1_run.py`** — a deterministic runner that reuses the original model code unchanged (it executes only the class/function definitions) and fixes two sources of non-reproducibility: corpus ordering (the original built its folds from an unsorted `os.walk`) and an unseeded baseline RNG.
- **`REPRODUCTION_REPORT.md`** — full documentation and validation against the published results.
- **`replication_comparison.csv`** — per-model comparison of reproduced vs. shipped results.

## Key results

- The reproduced corpus matches the paper exactly: **58,241 utterances** and **6,911 retagged noun tokens**.
- V1 recovers the paper's reported pattern: left/framing precision ≈ 0.90 (nouns) / ≈ 0.80 (verbs), roughly flat across seed size; recall low for small seeds and  rising monotonically with seed size; the right-context model clearly poorest; the baseline far below the context models.
- V1 is bit-for-bit reproducible across runs.

Details and the full comparison table are in
[`REPRODUCTION_REPORT.md`](REPRODUCTION_REPORT.md).

## Data statement

This project uses the Lyon corpus (Marie & Théotime), part of CHILDES / PhonBank.
**The corpus is not redistributed here.** Obtain it from
<https://phonbank.talkbank.org/access/French/Lyon.html> and place the corrected CoNLL files at `./corrected_corpus/`.

## Reproduce

```bash
# 1. original model code + corrected corpus git clone https://github.com/oseminck/bootstrapping_model cd bootstrapping_model
#    (unzip corrected_corpus.zip so ./corrected_corpus/ exists)

# 2. add this repository's files into that folder
#    call_my_corpus.py  and  v1_run.py

# 3. run
python3 call_my_corpus.py   # rebuild the utterances / voca pickles
python3 v1_run.py           # deterministic run -> v1_resultats/
```

Requires Python 3 with `numpy` and `nltk`.

## Citation

Brusini, P., Seminck, O., Amsili, P., & Christophe, A. (2021). The acquisition of noun and verb categories by bootstrapping from a few known words: A computational model. *Frontiers in Psychology*, 12, 661479. <https://doi.org/10.3389/fpsyg.2021.661479>

## Licence

The additions in this repository (`call_my_corpus.py`, `v1_run.py`, the report and comparison data) are released under the MIT Licence. The original model code and the corpus are governed by their own licences — see the original repository and the CHILDES terms of use.
comparison data) are released under the MIT Licence. The original model code and
the corpus are governed by their own licences — see the original repository and
the CHILDES terms of use.
