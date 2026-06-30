Reading through each claim and tracing the dependency chains, the body of every claim is sound and the proofs go through. One structural issue surfaces in D-SEQ's Formal Contract.

**D-SEQ proof body directly invokes three claims absent from its Depends list.** The proof text names each by label, passes explicit arguments to them, and relies on their postconditions as load-bearing steps; none is a transitive dependency absorbed by an already-listed claim.

1. **T0(a) (UnboundedComponentValues, ASN-0034)** — Step 3: *"The admissible values are drawn from T0(a)… We instantiate it at t = u and i = j + 1"*; Assembly: *"we invoke T0(a) exactly N + 1 times, each application feeding its output back as the next bound."* Without T0(a) the strictly-increasing run n₁ < n₂ < … of N + 1 admissible values has no grounding — T0's comprehension clause only supplies existence of a tumbler from a given component map; it gives no tumbler whose specified component exceeds an arbitrary bound M.

2. **T3 (CanonicalRepresentation, ASN-0034)** — Step 3: *"distinct admissible values yield distinct positions, since two witnesses built at n ≠ n′ differ at component j + 1 — their sole varying component — and are unequal by T3 (CanonicalRepresentation, ASN-0034)."* The step is the reverse direction of T3 (same length + one component differs → not equal). T0's extensionality clause provides the forward direction (componentwise equal → equal), not the contrapositive consumed here.

3. **D-INJ (InjectiveImageCardinality, this ASN)** — Assembly: *"For the exact count we invoke D-INJ (InjectiveImageCardinality), instantiated at P := N + 1 and n := N. D-INJ discharges, by an explicit induction on the segment length {k ∈ ℕ : 1 ≤ k ≤ N + 1}, exactly the step a bare counting argument would leave circular."* This is a named, explicit invocation in D-SEQ's own Assembly — a distinct use from D-CTG-depth's separate invocation of D-INJ for its prefix-disagreement contradiction.

All three are already in D-CTG-depth's Depends (where they serve analogous roles), confirming the pattern of use is correct; the gap is purely that D-SEQ's Formal Contract omits them despite the proof body depending on them directly.

### D-SEQ Depends list missing T0(a), T3, and D-INJ
**Class**: REVISE
**Foundation**: T0(a) (UnboundedComponentValues, ASN-0034); T3 (CanonicalRepresentation, ASN-0034); D-INJ (InjectiveImageCardinality, this ASN)
**ASN**: D-SEQ (SequentialPositions), Formal Contract Depends — all three are absent despite being named and directly invoked in the proof body: T0(a) in Step 3 ("The admissible values are drawn from T0(a)") and Assembly ("invoke T0(a) exactly N + 1 times"); T3 in Step 3 ("unequal by T3 (CanonicalRepresentation, ASN-0034)"); D-INJ in Assembly ("we invoke D-INJ (InjectiveImageCardinality), instantiated at P := N + 1 and n := N")
**Issue**: The Formal Contract Depends list is the authoritative dependency record for formalization tools and downstream consumers. A consumer reading it would not know to import T0(a), T3, or D-INJ, leaving the dependency graph incomplete. Each is a direct, load-bearing step: T0(a) grounds the existence of N + 1 admissible witnesses with strictly increasing j+1 components; T3 licenses the conclusion that distinct component values yield distinct tumblers; D-INJ supplies the exact image cardinality that, set against NAT-card's upper bound, closes the greatest-element contradiction.
**What needs resolving**: Add T0(a), T3, and D-INJ to D-SEQ's Formal Contract Depends list, with entries describing each claim's direct use: T0(a) for the N + 1 admissible-value witnesses in Step 3 and Assembly; T3 for the distinctness argument in Step 3; D-INJ for the pigeonhole count in the Assembly at instantiation P := N + 1, n := N.

VERDICT: REVISE