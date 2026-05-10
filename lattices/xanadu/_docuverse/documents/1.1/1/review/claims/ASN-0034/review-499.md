# Regional Review — ASN-0034/T10 (cycle 2)

*2026-04-24 06:59*

### "Forward direction of T3" has opposite meanings in T3 and T10
**Class**: REVISE
**Foundation**: T3 (CanonicalRepresentation); T10 (PartitionIndependence)
**ASN**: T3 proof labels *Forward direction* as `#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) ⟹ a = b` ("instantiated at `(a, b)` yields `a = b` directly"). T10 proof cites "the contrapositive of the forward direction of T3 (`a = b ⟹ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`)".
**Issue**: The biconditional in T3 is `(conjunction) ≡ (a = b)`. T3's own proof fixes "Forward direction" as `conjunction ⟹ a = b`. T10 uses "forward direction" for the opposite orientation (`a = b ⟹ conjunction`), which is T3's *Reverse direction*. A reader following citation labels across sections is pointed at the wrong half of the biconditional and must recover from the parenthetical. The term "forward direction of T3" is doing two different jobs in the same ASN — precisely the kind of meaning-shift across sections the review is meant to catch. It also silently drops the `#a = #b` conjunct in T10's restatement, further deforming the cited direction.
**What needs resolving**: Pick a single orientation for "forward/reverse" of T3 and apply it consistently, or drop the directional labels in favor of quoting the specific implication being used. Either way, T10's invocation should name the same half of the biconditional T3's proof names.

VERDICT: REVISE
