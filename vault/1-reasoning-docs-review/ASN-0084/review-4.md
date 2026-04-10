# Review of ASN-0084

## REVISE

### Issue 1: Foundation misreference for multi-step ordinal shift
**ASN-0084, State and Vocabulary**: "We write `c₀ + j` for the V-position [S, ord(c₀) + j] — that is, j ordinal increments via TA5(c) (ASN-0034)."
**Problem**: TA5(c) defines a single-step sibling increment: `inc(t, 0)` advances `sig(t)` by exactly 1. Multi-step ordinal advancement is defined by OrdinalShift (ASN-0034): `shift(v, j) = v ⊕ δ(j, #v)`. The correspondence run definition in ASN-0036 already establishes the convention `v + k = shift(v, k)` for `k ≥ 1`. Separately, the associativity claim "follows from natural-number addition at the ordinal level" is correct at depth 2 but the foundation property grounding it is TS3 (ShiftComposition, ASN-0034): `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)`.
**Required**: Replace "j ordinal increments via TA5(c)" with "ordinal shift via OrdinalShift (ASN-0034): `c₀ + j = shift(c₀, j)`, consistent with the correspondence-run convention of ASN-0036." Cite TS3 for associativity.

### Issue 2: Properties table omits all definitions
**ASN-0084, Properties Introduced**: The table lists 8 entries — all lemmas and frame conditions. No definitions appear.
**Problem**: The ASN introduces at least 9 formal definitions (CutSequence with CS1–CS4, RegionPartition, R-PRE, PivotPostcondition, SwapPostcondition, ArrangementRearrangement, PermutationDisplacement, Block/Split/Merge). Foundation ASNs (ASN-0036, ASN-0053) list definitions in their property tables with type DEF. Without table entries, downstream ASNs cannot reference these definitions by label.
**Required**: Add the definitions to the properties table with type DEF. Each should have a one-line statement. Example:

| CutSequence | DEF | Tuple (c₀, ..., c_{n−1}) with n ∈ {3,4}, strictly ordered, same subspace, depth 2 | introduced |

### Issue 3: Invariant preservation not systematically stated
**ASN-0084, throughout**: The ASN proves preservation of S0 (C' = C), S2 (R-PIV/R-SWP), S3 (R-RI), and S8/B1–B3 (R-BLK). It does not state that D-CTG, D-MIN, S8-fin, S8a, S8-depth are preserved.
**Problem**: All five are preserved trivially because `dom(M'(d)) = dom(M(d))`. But a downstream ASN reasoning about the post-rearrangement state needs to know they hold without re-deriving the argument. The arrangement rearrangement definition guarantees domain identity — the consequence for domain-dependent invariants should be explicit.
**Required**: Add a brief note listing all preserved ASN-0036 invariants with the reason. For example: "The following invariants depend only on `dom(M(d))` and are preserved because `dom(M'(d)) = dom(M(d))`: D-CTG, D-MIN, S8-fin, S8a, S8-depth. Together with R-RI (S3), R-PIV/R-SWP (S2), and C' = C (S0, S1), every ASN-0036 invariant is maintained."

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 V-positions
**Why out of scope**: The ASN explicitly restricts to depth 2 and notes the generalization is "structurally identical by D-CTG-depth." The claim is plausible — D-CTG-depth and D-SEQ reduce arbitrary depth to last-component contiguity — but the full argument belongs in a follow-up or a revision that lifts the restriction.

### Topic 2: Composition and expressiveness of cut-point rearrangements
**Why out of scope**: The open questions about k-cut generalization, composability, and block-count bounds are research questions for future ASNs, not errors in this one.

VERDICT: REVISE
