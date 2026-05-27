# Review of ASN-0101

## REVISE

### Issue 1: D10 conflates step-level vacuity with composite-level coupling

**ASN-0101, D10 Consequence**: "DEL can be freely interleaved with any other elementary transitions in a ValidComposite★ chain without imposing additional coupling obligations on the composite. The composite's J0/J1★/J1'★ proofs reduce, at each DEL step, to the trivial vacuity arguments above"

**Problem**: ASN-0047's ValidComposite★ defines J0/J1★/J1'★ as composite-level constraints "evaluated only between the initial state Σ and the final state Σ' of the composite as a whole" — not step-by-step. The vacuity argument is step-level. Consider the composite `K.α(a) → K.μ⁺(v ↦ a) → DEL(removes v)`:
- `a ∈ dom(C_3) \ dom(C_0)` (K.α added it)
- No witness in `M_3(d)` (DEL removed it)
- Composite-level J0 fails

DEL can break composite-level J0 by removing the witness for an allocation made earlier in the same composite. The "freely interleaved" language suggests any DEL-containing composite that was valid pre-DEL remains valid; this is not what the proof shows.

**Required**: Restate D10 to distinguish (a) DEL doesn't *create* coupling obligations (correct: it adds nothing to `dom(C')\dom(C)`, `ran(M')\ran(M)`, or `R'\R`) from (b) DEL *can affect satisfaction* of existing obligations (by removing witnesses from `ran(M)`). Acknowledge that a composite containing K.α + K.μ⁺ + DEL on the same address may fail J0 at the composite endpoint, and that this is the composite's problem, not DEL's.

### Issue 2: D7's justification misses the L0 citation for the I-subspace partition

**ASN-0101, D7 Justification**: "The pre-condition `a ∈ ran(M(d))` together with S3★ at the pre-state gives `a ∈ dom(C) ∪ dom(L)`, with the partition determined by S3★: a content-subspace V-position maps into `dom(C)`, a link-subspace V-position maps into `dom(L)`."

**Problem**: D7's statement uses `subspace_I(a)` (I-address subspace), but the justification uses `subspace(v)` (V-position subspace) via S3★. The "Equivalently" clause requires bridging these via L0 (ASN-0093): `a ∈ dom(C) ⟹ subspace_I(a) = s_C` and `a ∈ dom(L) ⟹ subspace_I(a) = s_L`. Only L14 (disjointness) is cited; L0 (the directional claim) is needed to translate from V-subspace to I-subspace partitioning.

**Required**: Add explicit L0 citation, or restate D7 in terms of `subspace(v)` for the witnessing V-position.

### Issue 3: Boundary case enumeration omits the non-degenerate interior case

**ASN-0101, Boundary cases section**: enumerates Empty post-state, Deletion at the start, Deletion at the end, Singleton subspace deletion, Singleton interior deletion.

**Problem**: The most common case — `n > 1`, `1 < p`, `p + n − 1 < n_S` with both `Λ` and `Q` non-empty, both non-singleton — is *not* listed. The worked example exercises this case (`n_S = 4`, `n = 2`, `p = 2`), but the boundary-cases section doesn't trace through it. The closing remark "The remaining three cases instantiate one of these two routes (or the general route) at degenerate parameter values" promises a "general route" that is nowhere explicitly traced.

**Required**: Either add a sixth boundary case ("non-singleton interior deletion") with explicit trace through D8's discharge clauses, or rewrite the closing remark to point to the worked example as the canonical trace of the general case.

### Issue 4: Atomicity argument's "observable intermediate state" is informal

**ASN-0101, The Operation section**: "the composite is therefore observable as two distinct state transitions, not one."

**Problem**: The abstract specification has no notion of "observation." SequentialAtomicTransitions establishes that transitions are atomic and totally ordered, but doesn't define what is "observable." The intermediate state after K.μ~ in the K.μ~ + K.μ⁻ composite is well-formed (satisfies S2, S3★, S8a, D-CTG★, D-MIN★, D-SEQ★ — these are precisely K.μ~'s admissibility preconditions). So the argument that this state is "observable" needs a sharper formulation.

**Required**: Reframe the atomicity argument in terms abstract specification cares about. A precise statement: any predicate on system state that distinguishes the post-K.μ~ intermediate from both endpoints would be "observable"; DEL as elementary guarantees no such intermediate exists in the transition history; DEL as composite would expose this intermediate to any predicate evaluating across transition history. Cite the specific abstract structure (the transition sequence Σ₀ → Σ₁ → ... → Σₙ in SequentialAtomicTransitions) rather than appealing to undefined "observation."

### Issue 5: Reduction argument's m_S = 2 boundary handling is implicit

**ASN-0101, Justification of the reduction**: "We claim `v_j = 1` for every `j` with `2 ≤ j ≤ m_S − 1`. Suppose otherwise..."

**Problem**: When `m_S = 2` (e.g., link subspace per LinkVPositionDepthAxiom), the range `2 ≤ j ≤ m_S − 1 = 1` is empty. The claim is vacuously true, and the conclusion follows immediately from positivity at position 2. The text doesn't explicitly note this. Given that `m_S = 2` is the *standard* case for the link subspace and the worked link-subspace example operates at depth 2, this case deserves explicit acknowledgment.

**Required**: Add a sentence noting "At `m_S = 2` the intermediate range is empty and the claim holds vacuously; the argument reduces directly to `v_2 = p + k` for some `0 ≤ k < n` from the lex-order constraint."

### Issue 6: Worked content-subspace example doesn't address V_2(d) contribution to the projection

**ASN-0101, A worked example, content-subspace projection**: "project(L(ℓ_0).e_1, d, Σ) = V_1(d) = {[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 1, 4]}"

**Problem**: The link-subspace example explicitly notes "Any content-subspace positions of `d` map to I-addresses with `subspace_I = s_C = 1`, which fall outside the link-subspace coverage and so do not enter the projection." The content-subspace example silently assumes `V_2(d)` contributes nothing but doesn't justify this. The reason is symmetric (V_2(d) maps to `dom(L)` per S3★, which by L0 has `subspace_I = s_L = 2`, disjoint from content-subspace coverage). Without this note, a careful reader cannot verify the projection computation.

**Required**: Add the symmetric note to the content example, or explicitly state that the example assumes `V_2(d)` is empty or trivially non-contributing.

### Issue 7: D8 Group (i) S2 functionality proof skips disjointness verification

**ASN-0101, D8 Group (i) Justification**: "S2 holds by the construction of `M'(d)`: the disjoint sources `Λ`, `Q`, and `V_{S'}(d)` for `S' ≠ S` each provide a single value for each position, and they cover disjoint subsets of the post-state domain."

**Problem**: The disjointness claim is stated but not justified. The non-trivial disjointness is `Λ ∩ Q = ∅` — these are both subsets of the same subspace `S` and could conceivably overlap. The argument requires: `Λ` has last component in `{1, ..., p − 1}`, `Q` has last component in `{p, ..., n_S − n}`; these ranges are disjoint because `p − 1 < p`. Cross-subspace disjointness (`Λ ∩ V_{S'}(d) = ∅`, `Q ∩ V_{S'}(d) = ∅`) is trivial by first-component (subspace) difference.

**Required**: Provide a one-line discharge of `Λ ∩ Q = ∅` via last-component range disjointness, and note that cross-subspace disjointness is by first-component difference.

### Issue 8: D9 second bullet uses asymmetric notation V_{S'}(M'(d)) vs V_{S'}(d)

**ASN-0101, D9 second bullet**: "If `d'' = d`, restricted to subspace `S' ≠ S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(M'(d)) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)`."

**Problem**: The LHS uses `V_{S'}(M'(d))` and RHS uses `V_{S'}(d)`. These are equal by D6, but the asymmetric notation can mislead. The same set appears on both sides; consistency would clarify.

**Required**: Use `V_{S'}(d)` consistently (or `V_{S'}(M(d))`), with a footnote noting that D6 makes them equal.

## OUT_OF_SCOPE

None. The ASN stays within DELETE's specification scope; references to versioning (J4 ForkComposite) and other operations are contextual, not specifying. The discussion of stale auxiliary indices and tree-height invariance correctly identifies these as outside abstract specification.

VERDICT: REVISE
