# Revision Categorization — ASN-0043 review-13

**Date:** 2026-03-22 22:27



## Issue 1: Link definition and L3 — body vs. Properties table contradiction
Category: INTERNAL
Reason: The contradiction is between two parts of the same ASN — the body text defines N-ary links while the Properties table says ternary. All the evidence needed to resolve it (Nelson's N-endset quotes, Gregory's hardcoded-three implementation notes, the StandardTriple convention) is already present in the ASN's own text. The fix is editorial: choose one position and propagate it consistently.

## Issue 2: "GlobalUniqueness (ASN-0034)" — unnamed in foundation
Category: INTERNAL
Reason: This is a missing derivation from properties (T9, T10) already defined in ASN-0034. The fix is to either cite T9+T10 directly or derive the lemma explicitly — no external evidence is needed beyond what the foundation ASN already contains.

## Issue 3: PrefixSpanCoverage introduces `ℓ_x`; foundation already defines `δ(1, #x)`
Category: INTERNAL
Reason: The ASN-0034 foundation already defines `δ(n, m)` and `shift(x, n)`. The fix is notational unification — replacing a redundant symbol with the existing one — which requires only reading ASN-0034's definitions.

## Issue 4: L8 classified as INV — it is a definition
Category: INTERNAL
Reason: This is a classification error in the Properties table. L8 introduces a derived relation (`same_type`), which is definitional, not a state constraint. The reclassification from INV to DEF is decidable from the ASN's own content.
