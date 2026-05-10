# Review of ASN-0054

## REVISE

### Issue 1: Notation collision in A0

**ASN-0054, A0 formula**: `(A v, v₁, v₂ : v₁ ∈ V(d) ∧ v₂ ∈ V(d) ∧ v₁ ≤ v ≤ v₂ ∧ #v = L(d) ∧ v₁ ≥ 1 : v ∈ V(d))`

**Problem**: The variables `v₁` and `v₂` are bound as tumblers in the quantifier, but one line earlier, the V(d) definition uses `v₁` to denote the first component of `v`. The trailing guard `v₁ ≥ 1` is then ambiguous — it could compare the tumbler variable `v₁` to `[1]` under T1, or assert the first component of the interpolated tumbler `v` is ≥ 1. Under either reading the condition is redundant (the first follows from membership in V(d); the second follows from `v₁ ≤ v` and T1), but the collision makes the formula unparseable on first read.

**Required**: Use distinct variable names for the bound V-positions (e.g., `u, w`), and if a text-subspace guard on `v` is wanted, write it unambiguously as `(v)₁ ≥ 1`.

### Issue 2: wp direction reversed in preservation arguments

**ASN-0054, INSERT**: `wp(INSERT(d, j, w), A0) ⟹ A0 ∧ 0 ≤ j ≤ n`

**Problem**: As written, the weakest precondition *implies* the stated conditions, making A0 ∧ 0 ≤ j ≤ n a *necessary* but not *sufficient* condition for preservation. The intended claim is the converse: A0 ∧ 0 ≤ j ≤ n is strong enough to guarantee A0 in the post-state. The same reversed implication appears in DELETE.

**Required**: Reverse to `A0 ∧ 0 ≤ j ≤ n ⟹ wp(INSERT(d, j, w), A0)`, or use a Hoare triple, or use `=` if claiming the wp is exactly this predicate.

### Issue 3: Zero-displacement in run formula

**ASN-0054, Canonical Decomposition**: "Within a run, for 0 ≤ i < r: `M_{s+i} = a_s ⊕ [0, ..., 0, i]`"

**Problem**: At i = 0, the displacement `[0,...,0,0]` is a zero tumbler. TumblerAdd (ASN-0034) requires `w > 0`; the expression `a_s ⊕ [0,...,0,0]` is undefined. The text says "the base i = 0 is immediate" — correct, since M_s = a_s by definition — but the universally quantified formula literally includes the undefined case. ASN-0036's CorrespondenceRun has the same convention and explicitly notes "At k = 0 ... no displacement, no arithmetic"; this ASN should do likewise.

**Required**: Restrict the ⊕ formula to `1 ≤ i < r` with the base case `M_s = a_s` stated separately, or add the convention that `a ⊕ 0_m` is understood as `a` at i = 0 (matching ASN-0036's treatment).

### Issue 4: COPY absent from preservation section

**ASN-0054, Preservation Under Operations**: "We verify that the FEBE operations preserve A0."

**Problem**: The section covers INSERT, DELETE, and REARRANGE but not COPY (transclusion). The ASN invokes transclusion in A8 and A9 to motivate I-order independence and I-span overlap — these arrangements must satisfy A0. COPY's V-space effect (add positions, shift the rest) is structurally identical to INSERT, so INSERT's analysis subsumes it, but this subsumption is never stated. A reader checking "do all FEBE operations preserve A0?" finds COPY missing.

**Required**: One sentence noting that COPY/transclusion is subsumed by INSERT for V-space purposes (same shift mechanics, different I-address provenance).

### Issue 5: Break causes enumeration incomplete

**ASN-0054, Breaks**: "A break occurs in exactly two circumstances: the I-addresses at consecutive V-positions have different origins ... or they have the same origin but skip at least one element-field ordinal."

**Problem**: A third circumstance exists: same origin but different I-address depths (`#M_{j-1} ≠ #M_j`). By the result-length identity, `M_{j-1} ⊕ u_I(M_{j-1})` has length `#M_{j-1}`; if `#M_j` differs, the successor test fails irrespective of origin or ordinal. This occurs when a document allocates at different element-field depths (child allocators per T10a produce longer tumblers). The formal break predicate (`M_j ≠ M_{j-1} ⊕ u_I(M_{j-1})`) correctly covers all three cases, but the prose claims "exactly two."

**Required**: Either list the third circumstance, or drop "exactly two" and reference the formal predicate as the exhaustive definition.

## OUT_OF_SCOPE

### Topic 1: Formal decomposition of operations into elementary transitions
**Why out of scope**: INSERT, DELETE, REARRANGE are characterized by their net effects on M(d), not decomposed into K.α / K.μ⁺ / K.μ⁻ / K.μ~ / K.ρ sequences. The preservation arguments check A0 consistency with these net effects — appropriate for a structural-characterization ASN. Formal composite definitions (with intermediate-state reasoning and coupling constraints) belong in a future operations ASN.

### Topic 2: Link subspace invariants
**Why out of scope**: The ASN restricts to the text subspace (v₁ ≥ 1) and explicitly lists link subspace invariants as an open question. Link addresses are permanent and admit gaps after deletion — structurally different from the contiguous text domain — requiring separate treatment.

VERDICT: REVISE
