#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deterministic V1 reproduction of Brusini, Seminck, Amsili & Christophe (2021),
"The acquisition of noun and verb categories by bootstrapping from a few known
words" (Front. Psychol. 12:661479). Original repo: github.com/oseminck/bootstrapping_model.

This runner does NOT modify the original source. It execs ONLY the class/function
definitions from models_and_errors.py (everything above the module-level driver,
which starts at `corp = Corpus(...)`), so the exact original model code is reused.
It then supplies its own deterministic driver that fixes the two sources of
non-reproducibility identified during faithful reproduction:

  1. Corpus ordering. The original builds the utterance list from an unsorted
     os.walk, and its 10 mini-corpora are index-slices of that list. Here the
     corpus is read in numeric filename order so the split is fixed.
  2. Baseline RNG. The chance model uses np.random.choice; the original never
     seeds it. Here numpy is seeded once per model, so every run is identical.

Outputs go to v1_resultats/ and v1_err/ (the shipped resultats/ is left intact).
"""

import os, re, copy, pickle
import numpy as np
from corpus import Corpus

SEED = 20260820
CORPUS_DIR = "corrected_corpus/"
SEUIL = 0.0005
OUT_RES, OUT_ERR = "v1_resultats/", "v1_err/"

# ---- 1. Load original definitions only (no driver side-effects) -------------
src = open("models_and_errors.py", encoding="utf-8").read()
prefix = src.split('\ncorp = Corpus("corrected_corpus/", 0.0005)')[0]
# drop the side-effecting import of the (reconstructed) preprocessing module
prefix = "\n".join(l for l in prefix.splitlines()
                   if not l.startswith("from call_my_corpus import"))
ns = {}
exec(compile(prefix, "models_and_errors.py[defs]", "exec"), ns)
main = ns["main"]

# ---- 2. Build corpus in a fixed (numeric filename) order --------------------
def numkey(fn):
    m = re.match(r"(\d+)", fn)
    return int(m.group(1)) if m else 10**9

corp = Corpus(CORPUS_DIR, SEUIL)
for fn in sorted(os.listdir(CORPUS_DIR), key=numkey):
    if fn.endswith(".txt"):
        with open(CORPUS_DIR + fn, encoding="utf-8") as f:
            corp.get_voca_aux(f)          # fills corp.utterances (sorted) + corp.voca
corp.get_freqlist()
sorted_corpus = corp.utterances

# voca pickle is required by ModeleContextesImbriques.__init__ (error analysis)
with open("voca", "wb") as f:
    pickle.dump(corp.voca, f)

# ---- 3. Semantic seeds (deterministic: read from curated word lists) --------
seeds = {i: corp.get_graine_semantique(n, v) for i, (n, v) in enumerate(
    [(8, 1), (16, 2), (32, 3), (64, 6), (128, 12), (192, 24)])}

# ---- 4. Model roster (mirrors the original driver) --------------------------
C = ns  # class namespace
roster = [
    ("Modele_Baseline_Vm",       None, "modele_baseline_vm.txt"),
    *[("Modele_Baseline",        s,    f"modele_baseline_v{i}.txt") for i, s in seeds.items()],
    *[("ModeleContextesImbriques", s,  f"modele_imbrique_v{i}.txt") for i, s in seeds.items()],
    ("Modele_Imbrique_Vm",       None, "modele_imbrique_vm.txt"),
    *[("ModeleContextesGauches", s,    f"modele_gauche_v{i}.txt")   for i, s in seeds.items()],
    ("Modele_Gauche_Vm",         None, "modele_gauche_vm.txt"),
    *[("ModeleContextesDroits",  s,    f"modele_droit_v{i}.txt")    for i, s in seeds.items()],
    ("Modele_Droit_Vm",          None, "modele_droit_vm.txt"),
]

os.makedirs(OUT_RES, exist_ok=True)
os.makedirs(OUT_ERR, exist_ok=True)

for cls_name, seed, outfile in roster:
    np.random.seed(SEED)                  # per-model reseed => each run reproducible
    graine = seed if seed is not None else []
    model = C[cls_name](graine, [], [], [])
    main(model, sorted_corpus, outfile, OUT_RES, OUT_ERR)
    print("done:", outfile)

print("V1 complete ->", OUT_RES)
