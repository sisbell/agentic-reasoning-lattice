# Review of ASN-0047

## REVISE

### Issue 1: D-CTG and D-MIN absent from pre-extension transitions and ReachableStateInvariants

**ASN-0047, Elementary transitions / Arrangement invariants lemma / Reachable-state invariants**: The original K.μ⁺ precondition lists S8a, S8-depth, S8-fin but not D-CTG or D-MIN. The original K.μ⁻ claims invariant preservation "by restriction of M(d)." The arrangement invariants lemma says "Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin." The ReachableStateInvariants theorem lists "P4, P6, P7, P7a, P8, S2, S3, S8a, S8-depth, and S8-fin."

**Problem**: D-CTG and D-MIN are foundation invariants from ASN-0036, tagged `INV, predicate; design constraint`. Neither is maintained by the pre-extension transition definitions, included in the arrangement invariants lemma, or listed in ReachableStateInvariants.

This is not merely an omission from the theorem statement — the pre-extension transitions are genuinely too permissive. K.μ⁺ without the amendment can place V-positions with gaps (adding `[1,1]` and `[1,3]` without `[1,2]` violates D-CTG) or fail to start from the minimum (adding `[1,3]` to an empty arrangement violates D-MIN). K.μ⁻ without the amendment can remove an interior position from a contiguous range, breaking D-CTG. The claim that "K.μ⁻ preserves them by restriction of M(d)" is correct for S2/S3/S8a/S8-depth/S8-fin but false for D-CTG — restricting a contiguous range by removing an interior element does not yield a contiguous range.

The amendments introduced later (in the extended-state context) add D-CTG/D-MIN postconditions to K.μ⁺ and K.μ⁻, and ExtendedReachableStateInvariants includes D-CTG/D-MIN. But the pre-extension analysis leaves a window where foundation invariants are not maintained.

**Required**: Include D-CTG and D-MIN postconditions in the original K.μ⁺ and K.μ⁻ definitions. Add D-CTG and D-MIN to the arrangement invariants lemma and to ReachableStateInvariants. The amendments then refine the existing postconditions (adding subspace scoping) rather than introducing D-CTG/D-MIN for the first time.

### Issue 2: Temporal decomposition omits the link store

**ASN-0047, Temporal decomposition**: "The state Σ = (C, E, M, R) decomposes into three temporal layers"

**Problem**: By this point in the ASN, the extended state Σ = (C, L, E, M, R) is the operative state model — P3★ and P5★ (which include L) have already been stated, and ExtendedReachableStateInvariants is the governing theorem. The temporal decomposition references the four-component state and omits L entirely: the existential layer lists only (C, E); the table omits K.λ and K.μ⁺_L; the bridge-invariant analysis does not mention L0, L1a, L12, or L14.

L has the same permanence contract as C — append-only with immutable values (L12). It belongs in the existential layer. K.λ is an existential transition. K.μ⁺_L is a presentational transition. The bridge analysis should note: S3★ bridges M → {C, L} (presentational → existential); L1a is the link analog of P6 (intra-existential); L14 is an intra-existential disjointness constraint.

Since the temporal decomposition is positioned as "the structural insight underlying the entire design," omitting a state component weakens the result.

**Required**: Update the temporal decomposition to cover Σ = (C, L, E, M, R). Place L in the existential layer alongside C and E. Add K.λ to the existential row of the table and K.μ⁺_L to the presentational row. Extend the bridge-invariant analysis to cover L-related invariants.

### Issue 3: Completeness argument not extended to five-component state

**ASN-0047, Elementary transitions**: "Five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ — are complete. The argument is structural: the four-component state (C, E, M, R) admits exactly one growth mode for C (K.α), one for E (K.δ), one for R (K.ρ), and two independent mutation modes for M..."

**Problem**: The extended state (C, L, E, M, R) has seven transition kinds — K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — plus the distinguished composite K.μ~. ValidComposite★ enumerates them but makes no completeness claim. The structural argument should extend: L admits one growth mode (K.λ); M's growth now partitions by subspace (K.μ⁺ for content, K.μ⁺_L for links). This gives seven elementary kinds, and the same "any modification decomposes into additions and removals" argument applies per-component.

**Required**: State and argue completeness for the extended transition set, paralleling the four-component argument.

### Issue 4: Open question resolved within the ASN

**ASN-0047, Open Questions**: "Must arrangement reordering respect subspace boundaries within a document (text content at element subspace 1, link references at element subspace 2)?"

**Problem**: This question is answered by the link-subspace fixity analysis. The proof that K.μ~ preserves link-subspace mappings identically — derived from S3★, S3★-aux, L14, and the K.μ⁺ amendment — establishes that reordering respects subspace boundaries: link-subspace positions are fixed, and content-subspace positions rearrange independently. The question should be removed or replaced with a citation to the fixity result.

**Required**: Remove the open question or replace it with a reference to the fixity derivation.

## OUT_OF_SCOPE

### Topic 1: Link-subspace provenance
**Why out of scope**: The ASN deliberately excludes link addresses from provenance (J1★/J1'★ are content-subspace-scoped; P7 requires dom(C) membership). Whether a link-specific provenance relation is architecturally necessary — tracking which documents have ever arranged which links — is a distinct question that belongs in a future ASN on link lifecycle.

### Topic 2: Intermediate containment within composites
**Why out of scope**: Coupling constraints (J1, J1') are evaluated at composite boundaries. A composite that places content in document d₁ and then removes it before the boundary does not record provenance for d₁. Whether intermediate containment should be tracked is a design question about provenance completeness, distinct from the soundness properties (P4, P4a) established here.

VERDICT: REVISE
