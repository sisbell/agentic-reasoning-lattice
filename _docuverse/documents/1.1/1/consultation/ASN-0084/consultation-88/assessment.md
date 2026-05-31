# Channel Assignment — ASN-0084 review-88

**Date:** 2026-05-30 18:18

## Issue 1: R-COMM non-S case re-derives what its own precondition supplies
Reason: Purely internal editorial fix — the required reduction cites R-NS(NS-π) and the lemma's own precondition, both already present in the ASN. No design intent or implementation evidence bears on dropping a redundant derivation step.

## Issue 2: Width-positivity alignment argument duplicates the singleton↔ordinal coincidence already established
Reason: Internal deduplication — the singleton↔ordinal coincidence is already proven in the State and Vocabulary section, so collapsing the restatement requires only a back-citation within the ASN.

## Issue 3: R-NS forward-references R-PPERM/R-SPERM definitions that appear after it
Reason: Internal restructuring — both fix options (prove from frame conditions, or relocate the lemma) rely only on material already in the ASN; no external channel informs the ordering or citation choice.

## Issue 4: Intro dependency inventory is meta-prose
Reason: Internal editorial deletion — removing a redundant dependency-inventory sentence whose citations are already carried in-proof requires no design or implementation input.
