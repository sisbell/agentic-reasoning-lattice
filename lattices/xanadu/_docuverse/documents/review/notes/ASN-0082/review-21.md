# Review of ASN-0082

## REVISE

### Issue 1: I3-S (SpanShiftPreservation) lacks a concrete worked example

**ASN-0082, Span Width Preservation**: "I3-S — SpanShiftPreservation (LEMMA, introduced). For a level-uniform span σ = (s, ℓ) with s ≥ p..."

**Problem**: I3-S is the central span-level result — the lemma that justifies the ASN's title "Span Displacement" — yet it has no concrete numerical verification. The I3 worked example verifies point-level shifts exhaustively but never lifts the verification to span-level: it never names a span, computes its shifted reach, or checks width preservation against the tabulated data. OrdinalAdditiveCompatibility has a "Verification at m = 2" paragraph that instantiates the general proof on specific forms; I3-S deserves the same treatment. The algebraic proof is correct, but the absence of a concrete check means the reader must trust that TA-assoc preconditions, the commutativity swap, and the reverse TA-assoc application are all correctly composed — precisely the kind of multi-step manipulation where a numerical spot-check catches bookkeeping errors.

**Required**: Add a verification paragraph to I3-S (or extend the I3 worked example) that names a specific span from the existing worked example data and checks both postconditions against it. For instance: take σ = ([1,3], [0,3]) covering positions [1,3]–[1,5] in the pre-state, shift by n = 2, form σ' = ([1,5], [0,3]), compute reach(σ') = [1,8], verify shift(reach(σ), 2) = shift([1,6], 2) = [1,8] for part (a), and observe width(σ') = [0,3] = ℓ for part (b). Three lines suffice.

## OUT_OF_SCOPE

### Topic 1: Span width preservation under contraction

I3-S proves that ordinal shift preserves span width for the insertion direction. The contraction section proves point-level properties (D-SHIFT, D-BJ, D-SEP, D-DP) and all arrangement invariants, but does not state or prove a contraction analog of I3-S — that for a span σ = (s, ℓ) in the right region, the contracted span (σ(s), ℓ) preserves width. The machinery is in place (TA3-strict, D-BJ order-preservation, TumblerSub), and the result would follow by a symmetric argument.

**Why out of scope**: The contraction section's scope is point-level correctness and invariant re-establishment; a span-level contraction property is a natural enrichment but not an error in the current formulation.

### Topic 2: Composition of shift operations

The ASN defines insertion shift (I3) and contraction shift (D-SHIFT) independently. It does not analyze their composition — whether an insertion followed by a contraction at the same position recovers the original arrangement, or whether the two shift functions are inverses under appropriate conditions. This would connect the two halves of the ASN and provide a round-trip guarantee.

**Why out of scope**: Composition analysis is a property of the combined INSERT/DELETE operations, not of the displacement primitives defined here.

VERDICT: REVISE
