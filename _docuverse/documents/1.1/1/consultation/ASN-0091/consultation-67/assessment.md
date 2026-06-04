# Channel Assignment — ASN-0091 review-67

**Date:** 2026-06-04 02:09

## Issue 1: Clause (i) discharge bundles per-position and set-level invariants under one justification
Reason: Internal — the split between per-position predicates (S8a) and set-level predicates of V_S(d) (D-CTG★, D-MIN★, S8-depth) is derivable entirely from RA-dom and the definitions already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Duplicate downstream deferral and redundant restatement of the RA-adm discharge
Reason: Internal — this is a de-duplication of two restatements of the same reachability⟹invariants discharge; resolving it requires only choosing one location, no external input.

## Issue 3: Collapse case explained twice
Reason: Internal — consolidating the collapse-case derivation (Σ'=Σ ⇒ empty composite) to a single point and dropping the forward pointer is a pure editorial restructuring of content already in the ASN.

## Issue 4: Meta-prose justifying proof economy rather than advancing the argument
Reason: Internal — deleting the meta-prose and ordering parenthetical removes commentary about the proof rather than any object-level claim; the reachability implication remains self-contained in the ASN.
