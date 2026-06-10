# Review of ASN-0116

This is a careful, heavily-refined note. I checked the composite construction step-by-step, the coupling discharge (J0/J1★/J1'★), every boundary (empty subspace, append, front insertion with `n'_{s_C}=0`, full-clearance re-insertion, large-`n` block overrun), the gap-free tiling argument for I-DOM, the forward/backward I-merge analysis in IP1 including the recently-closed transclusion regime, and the wp computation in IP6. The technical content holds up: the K.μ⁻→K.μ⁺ ordering is correctly forced, the gapped/filled bridge is sound, the forward-merge impossibility (`shift(a,n) ∉ dom(C')` vs `M(d)(q_J) ∈ dom(C)`) is origin-independent and airtight, and the four-part witness decomposition in IP4 is exhaustive, disjoint, and the bijection/count is rigorous. All cross-references are to foundation ASNs; no notation is reinvented.

I found one genuine defect.

## REVISE

### Issue 1: Partial function `C` applied outside its domain in IP0

**ASN-0116, "What is allocated, and why it must be fresh" — IP0 (OriginIdentity)**: "For each `k` with `0 ≤ k < n`, `shift(a, k) ∉ dom(C)`, and `shift(a, k)` is distinct from every I-address in `dom(C)` regardless of whether `C(shift(a, k))` equals the content stored at any existing address."

**Problem**: The same sentence asserts `shift(a, k) ∉ dom(C)` and then writes `C(shift(a, k))`. Since `C : T ⇀ Val` is partial with `dom(C)` the pre-state store, `C(shift(a, k))` is undefined for a freshly-allocated address. The intended quantity is the post-allocation value `C'(shift(a, k)) = w_k`. This is inconsistent with the note's own `C`/`C'` convention, which it uses precisely elsewhere — e.g. I-ALLOC in the same section writes `C'(shift(a, k)) = w_k`, and IP5 correctly guards `C(M(d')(v'))` by `M(d')(v') ∈ dom(C)` (S3★).

**Required**: Replace `C(shift(a, k))` with `C'(shift(a, k))` (the freshly written value `w_k`), or rephrase to avoid applying `C` outside its domain — e.g. "regardless of whether the content `w_k` stored at `shift(a, k)` equals `C(b)` for any existing `b ∈ dom(C)`." The substance of IP0 (origin-based, value-independent identity, restating S4) is correct; only the symbol is wrong.

## OUT_OF_SCOPE

None. The four Open Questions (insertion at a transcluded position, concurrent freshness without a serializing authority, provenance under transclusion, post-fragmentation obligations) are posed as questions, not as claims, and correctly defer transclusion/concurrency/fragmentation to future notes. The note's references to K.μ~ (reordering) and K.μ⁻ (contraction) are used only to characterise reachable *pre-states*, not to define REARRANGE or DELETE, so they are not out-of-scope claims.

Anti-bloat: I looked specifically for accreted meta-prose around the forward references (I3, the K-vocabulary, ExtendedReachableStateInvariants) and did not find flaggable instances — shared facts (block-disjointness, gapped/filled bridge) are stated once and referenced, the "four atomics / arrangement change is not itself an atomic" paragraph is a substantive statement of what K.μ⁺/K.μ⁻/K.μ~ do and do not do (not meta-prose), and the problem-framing prose stays in its section without interrupting any claim. No duplicate paragraphs, deferral chains, or downstream-consumer inventories surfaced.

VERDICT: REVISE
