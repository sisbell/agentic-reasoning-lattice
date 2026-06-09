# Review of ASN-0117

## REVISE

### Issue 1: P5 (DocumentIsolation) asserts every other document's V-positions resolve into the content store — false for any document with links

**ASN-0117, "Invariants the operation must preserve" / Claims table**: "P5 (DocumentIsolation). *For every `d' ≠ d`: `M'(d') = M(d')`, and for every `v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`.*"

**Problem**: The resolution clause is quantified over *every* V-position of `d'`. But by S3★ (GeneralizedReferentialIntegrity, ASN-0047), a link-subspace position `v'` of `d'` (subspace `s_L`) maps into `dom(L)`, not `dom(C)`. For such a `v'`, the assertion `M'(d')(v') ∈ dom(C')` is false, and `C'(M'(d')(v'))` is undefined (the content store is a partial function undefined on link addresses, which are disjoint from `dom(C)` by SD, ASN-0093). This is exactly the error the ASN itself flags and avoids in "The document remains one coherent sequence": *"Stating the whole range as `ran(M'(d)) ⊆ dom(C')` would be false for any document containing a link."* P5 commits that very error for `d'`, making the note internally inconsistent. The worked transclusion example does not expose it because there `d'` happens to have only text positions.

**Required**: Restrict P5's resolution clause to content-subspace positions of `d'` (`subspace(v') = s_C ⟹ M'(d')(v') ∈ dom(C') ∧ C'(M'(d')(v')) = C(M(d')(v'))`), or state it across both stores using `dom(C') ∪ dom(L')` with P0 + DEL-LIMM jointly fixing the resolved content of every position.

### Issue 2: Post-state range decomposition restated in two sections (anti-bloat)

**ASN-0117, "Link survival…" (P4) and "A weakest precondition…"**: both sections independently restate the three-way decomposition `ran(M'(d)) = M(d)(L) ∪ M(d)(R) ∪ ran(M(d)↾V_{s_L}(d))`.

**Problem**: P4 derives the subset relation `ran(M'(d)) ⊆ ran(M(d))` from this decomposition; the wp section re-derives the same decomposition to obtain the exact form `ran(M'(d)) = ran(M(d)) \ A_del^{excl}`. The equality subsumes the subset, so the decomposition step is computed twice in different words. Under the note's `review-mode.anti-bloat` classifier this is the "two paragraphs say the same thing" pattern.

**Required**: Establish the decomposition (and the exact `A_del^{excl}` form) once, and have the other site cite it — e.g. P4 invokes the wp section's range identity, or the wp section references P4's decomposition and only adds the `A_del^{excl}` refinement.

## OUT_OF_SCOPE

### Topic 1: Deletion at general V-position depth `m ≥ 3`

**Why out of scope**: DELETE is restricted to depth-2 text positions (`m = #p = 2`) because every ASN-0082 displacement clause it cites (D-SHIFT, D-SEP, D-BJ, D-DOM) carries the `#p = 2` precondition. General-depth deletion must wait on a general-depth foundation contraction; it is new territory, not an error here. The restriction is stated honestly in the precondition.

### Topic 2: Reconstructibility of prior arrangements (backtrack)

**Why out of scope**: The note correctly establishes that deleted bytes persist in `C`, but the state needed to *reconstruct* a prior arrangement (beyond the content store) is raised in the Open Questions and belongs to a future ASN on historical backtrack.

VERDICT: REVISE
