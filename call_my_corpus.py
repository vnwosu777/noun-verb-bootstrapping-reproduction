#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reconstructed preprocessing step (the file referenced by the README as the
first script to run, and imported by models_and_errors.py via
`from call_my_corpus import utterances`).

Its job is to build the two pickle artifacts that models_and_errors.py loads
but that were not shipped in the repository:

  - "utterances" : the corpus as a list of utterances (list of token rows),
                   loaded at the bottom of models_and_errors.py.
  - "voca"       : the {form: {pos: count}} vocabulary dict, loaded in
                   ModeleContextesImbriques.__init__ for the error analysis.

It also exposes a module-level name `utterances` so that
`from call_my_corpus import utterances` succeeds.

Source directory: "corrected_corpus/" — chosen because every Corpus(...)
instantiation in models_and_errors.py points at "corrected_corpus/". (Note:
the README lists call_my_corpus.py *before* correct_corpus.py, which is
inconsistent with that; see the accompanying notes. Building from the
corrected corpus is what makes the downstream model self-consistent.)

The frequency threshold 0.0005 mirrors the value used throughout
models_and_errors.py.
"""

import pickle
from corpus import Corpus

CORPUS_DIR = "corrected_corpus/"
SEUIL = 0.0005


def build():
    corp = Corpus(CORPUS_DIR, SEUIL)
    corp.get_voca_and_utterances()   # fills corp.utterances and corp.voca
    corp.get_freqlist()              # needed before get_test_vocab downstream

    with open("utterances", "wb") as f:
        pickle.dump(corp.utterances, f)
    with open("voca", "wb") as f:
        pickle.dump(corp.voca, f)

    return corp


# Executed on import (mirrors the original module-with-side-effects pattern,
# so that `from call_my_corpus import utterances` yields a populated corpus).
_corp = build()
utterances = _corp.utterances

if __name__ == "__main__":
    _corp.get_info_utterances()
    _corp.get_info_voca()
