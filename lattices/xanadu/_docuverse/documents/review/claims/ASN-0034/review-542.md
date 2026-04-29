# Cone Review — ASN-0034/T4 (cycle 1)

*2026-04-25 16:38*

### T4a missing NAT-addcompat in Depends
**Class**: REVISE
**Foundation**: NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
**ASN**: T4a (SyntacticEquivalence), Forward Condition (i): "Then `i` and `i + 1` are both zero positions, so `i = s_j` and `i + 1 = s_{j'}` for some enumeration indices `j < j'` (strict monotonicity from `i < i + 1`)".
**Issue**: The parenthetical "strict monotonicity from `i < i + 1`" cites the strict successor inequality `i < i + 1` to conclude `j < j'` from `s_j = i` and `s_{j'} = i + 1` against the strictly increasing enumeration `s_1 < … < s_k`. The fact `i < i + 1` is exactly NAT-addcompat's third axiom clause; it is not derivable from T4a's currently declared foundations (NAT-discrete delivers the converse direction `m < n ⟹ m + 1 ≤ n`, not `n < n + 1` from nothing). NAT-addcompat does not appear in T4a's Depends list, so this use is ungrounded.
**What needs resolving**: Either declare NAT-addcompat in T4a's Depends with a use-site citation for the `n < n + 1` instantiation at `n := i` in Forward Condition (i), or replace the `i < i + 1` step with a derivation that does not lean on the strict successor inequality.

### Meta-prose justifying Consequence-vs-Axiom slotting in NAT-sub
**Class**: OBSERVE
**Foundation**: n/a (internal structural slot prose)
**ASN**: NAT-sub (NatPartialSubtraction), strict-monotonicity Consequence: "Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive…". Similar prose appears around strict positivity ("recorded as a Consequence rather than an axiom clause because its content is not purely subtractive").
**Issue**: These passages explain *why* the author chose the Consequence slot rather than the Axiom slot, with cross-references to choices made in other ASNs (NAT-order's disjointness form). They do not advance the reasoning a downstream consumer needs and read as defensive editorial rationale embedded in the contract. A consumer needs the derivation; the slotting rationale belongs in review notes, not the formal contract.

VERDICT: REVISE
