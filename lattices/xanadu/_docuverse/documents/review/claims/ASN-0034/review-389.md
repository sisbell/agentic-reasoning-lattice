# Regional Review — ASN-0034/ActionPoint (cycle 2)

*2026-04-22 23:21*

### NAT-wellorder's Formal Contract has no Depends slot
**Class**: REVISE
**Foundation**: n/a (NAT-wellorder itself)
**ASN**: NAT-wellorder *Formal Contract* lists only *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` with no *Depends:* declaration.
**Issue**: The axiom body uses the non-strict relation `≤` on ℕ, which is not a primitive of ℕ — NAT-order *defines* it via `m ≤ n ⟺ m < n ∨ m = n`. Every other NAT axiom that uses `≤` (NAT-discrete) or `0`/`+` (NAT-closure, NAT-discrete, NAT-zero's Consequence) declares the supplier in Depends so the axiom body reads without silently importing foundations. NAT-wellorder's axiom body uses `≤` but the Depends slot is absent entirely. Downstream (ActionPoint) cites NAT-wellorder and NAT-order separately, but at the NAT-wellorder node the `≤` symbol is ungrounded.
**What needs resolving**: Add a Depends declaration on NAT-order for `≤` (and note the register choice for `⊆ ℕ`/`≠ ∅` if the ASN wishes to treat set-theoretic primitives with the same rigor as the other NAT axioms).

### NAT-discrete "equivalently" asserts equivalence without derivation
**Class**: OBSERVE
**Foundation**: n/a (internal to NAT-discrete)
**ASN**: NAT-discrete *Axiom:* "`(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)`; equivalently `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)`".
**Issue**: The two forms are declared equivalent by the word "equivalently," but the equivalence is not a propositional re-writing — it requires NAT-order's irreflexivity, transitivity, totality, and the definition of `≤`. A precise reader must reconstruct that argument to see the two forms truly coincide. Unlike NAT-zero, which derives its Consequence bullet explicitly, NAT-discrete asserts the alternate form without a discharge.

### ActionPoint Depends gloss on NAT-zero's contribution
**Class**: OBSERVE
**Foundation**: NAT-zero (NatZeroMinimum) axiom is `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.
**ASN**: ActionPoint *Depends:* "NAT-zero (NatZeroMinimum) — supplies 0 ≤ w_{actionPoint(w)} and 0 ∈ ℕ." Derivation: "by NAT-zero, 0 ≤ w_{actionPoint(w)}".
**Issue**: NAT-zero supplies the disjunction `0 < n ∨ 0 = n`, not `0 ≤ n` directly. Collapsing the disjunction to `0 ≤ w_{actionPoint(w)}` requires NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n`. The citation "by NAT-zero" elides NAT-order's contribution at that step, and the Depends gloss similarly overstates what NAT-zero alone delivers.

VERDICT: REVISE
