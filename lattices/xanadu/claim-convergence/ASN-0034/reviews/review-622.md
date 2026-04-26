# Cone Review — ASN-0034/T10a.7 (cycle 1)

*2026-04-26 10:54*

Looking at this carefully, I need to check the proofs for soundness, the dependency lists for completeness, and look for unstated principles.

### Induction principle missing from T10a.7's Depends
**Class**: REVISE
**Foundation**: T10a.7 (EnumerationInjectivity) — standalone claim at end of ASN
**ASN**: T10a.7's standalone proof: "We route the argument through the lemma **L**: `(A d : d ≥ 1 :: (A m : m ≥ 0 :: tₘ < t_{m+d}))`... *Base case of L* (`d = 1`)... *Inductive step of L* (from `d` to `d + 1`)..."
**Issue**: The lemma L is proved by induction on `d ∈ ℕ` (base `d = 1`, step `d → d + 1`). The Depends slot lists T10a, TA5, T1, NAT-order, NAT-sub, NAT-addassoc — none of which posits or supplies the principle of mathematical induction on ℕ. NAT-wellorder is the document's source for ℕ-induction (it is cited that way in T1 for "first divergence position" and in TA5-SIG for `max(S)`), and is in the document, but is not declared by T10a.7. The induction step is not justified by any cited dependency.
**What needs resolving**: Identify the source of the induction principle T10a.7's lemma L invokes (NAT-wellorder is the natural candidate given the document's existing usage) and add it to the Depends list, with the use-site annotation.

### Vacuous `i = sig(t)` sub-case in TA5a Case k = 0
**Class**: OBSERVE
**Foundation**: TA5a Case `k = 0`, T4(ii) sub-cases
**ASN**: "we split each `i` with `1 ≤ i < #t'`... when `i = sig(t)`, `t'ᵢ = t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` ... falsifies the conjunct `t'ᵢ = 0`, and hence the conjunction"
**Issue**: TA5a's precondition is "`t` satisfies T4", and TA5-SigValid (in Depends) gives `sig(t) = #t` for any T4-valid `t`. The case-split index range is `1 ≤ i < #t`, which excludes `i = #t`. So the sub-case `i = sig(t)` is empty under the standing precondition; the sub-case `i + 1 = sig(t)` (i.e., `i = #t − 1`) is the only one of the two boundary sub-cases that can fire. Discussing the empty sub-case is harmless but is reviser drift — the prose imagines a case the precondition (via TA5-SigValid) already excludes.
**What needs resolving**: N/A (OBSERVE).

VERDICT: REVISE
