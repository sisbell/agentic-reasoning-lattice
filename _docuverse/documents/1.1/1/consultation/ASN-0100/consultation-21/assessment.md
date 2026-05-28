# Channel Assignment — ASN-0100 review-21

**Date:** 2026-05-28 13:12

## Issue 1: S8★ single-run merge relies on an unstated inc/shift identification
Reason: The fix is internal — it spells out a derivation from foundation lemmas already cited in the corpus (TA5-SigValid, TA5a, TS3 from ASN-0034; OrdinalShiftBase from ASN-0058) plus the chain-structure facts the ASN already establishes in Effect One. No design intent or implementation evidence is required; this is a proof-rigor gap (Standard 6).

## Issue 2: The `a_k + k` run-denotation is reused without derivation across sections
Reason: Same internal derivation as Issue 1 — establishing the lemma `a_k = shift(a_0, k)` once from the T4-validity and same-length-successor structure already asserted in the ASN, then referencing it. The needed facts are foundation theorems and the ASN's own allocation clauses, so neither Nelson nor Gregory is needed.
