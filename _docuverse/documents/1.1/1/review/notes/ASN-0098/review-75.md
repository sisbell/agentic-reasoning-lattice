# Review of ASN-0098

I checked the projection definition and every LP-lemma proof, the LP-Fin case analysis (sub-cases A/B and the four chain-index sub-sub-cases), the wp derivations LP12a/LP12b, and the two worked traces. The mathematics is sound: case coverage is exhaustive, the boundary cases (empty arrangement, empty retention `R = ∅`, orphan/resurrection) are handled, and the traces are internally consistent. No correctness gap survives scrutiny. All cross-ASN references are to foundation ASNs (0034/0036/0043/0047/0093), so standard 7 is satisfied.

The `review-mode.anti-bloat` classifier is the operative concern. Residual meta-prose remains at the following sites.

## REVISE

### Issue 1: Roadmap sentence previewing the LP9–LP11 proofs
**ASN-0098, "Operation Effects on Projection"**: "We now examine each operation that *can* displace a projection. The pattern is uniform: each K.μ operation modifies `Σ.M(d)` in a constrained way, and the projection follows mechanically."
**Problem**: The second sentence is a roadmap/essay statement that previews the *shape* of the proofs to come without advancing any claim. LP9, LP10, and LP11 each carry their own statement and proof; "the pattern is uniform … follows mechanically" is exactly the meta-prose a precise reader skips to reach the lemmas.
**Required**: Drop the second sentence; the section transition "We now examine each operation that can displace a projection" suffices.

### Issue 2: Restatement of the arrangement type in "State Components"
**ASN-0098, "State Components"**: "The two address spaces communicate through the `Σ.M(d)` mappings: V-positions in V-space resolve to I-addresses in I-space."
**Problem**: The immediately preceding paragraph already defines `Σ.M(d) : T ⇀ T` as "a partial function from V-positions to I-addresses." This sentence restates that fact in narrative form and advances nothing.
**Required**: Delete the sentence.

### Issue 3: Unused anchor-exclusion aside in the F-definition
**ASN-0098, "Boundary and Width Behaviour"**: "An address outside `F` cannot be the target of any K.α/K.λ emission. In particular, the sub-allocator anchors `b_C(d) = [d, 0, s_C]` and `b_L(d) = [d, 0, s_L]` of ASN-0093 have `#E = 1` and so lie outside `F`."
**Problem**: The first sentence pre-states the contrapositive of LP-Sub (proved two paragraphs later: `dom(Σ.C) ∪ dom(Σ.L) ⊆ F`); the anchor remark is never consulted by LP-Sub, LP-Fin, the LP-Fin Corollary, or LP12b. It is a clarifying aside that does not feed the F machinery the section is building toward.
**Required**: Remove the anchor sentence; if the "outside F is not emittable" point is wanted, fold it into LP-Sub rather than asserting it before proof.

## OUT_OF_SCOPE

### Topic 1: V-order of projected positions vs. I-order under K.μ~
Whether the V-order of projected positions reflects the I-order of underlying I-addresses (and its preservation under reordering) is correctly deferred to a future ASN — the note's Open Questions already register it. Not an error here.

### Topic 2: Reverse-discovery primitive (V-position → links)
Invariants for a reverse-discovery operation are new state/operation territory, appropriately listed under Open Questions rather than specified here.

VERDICT: REVISE
