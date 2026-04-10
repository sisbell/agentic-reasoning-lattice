# Review of ASN-0082

## REVISE

### Issue 1: Arrangement invariants violated by the shift are not documented
**ASN-0082, Structural preservation / Gap and vacated regions**: The ASN derives that S8-depth (I3-VD), S8a (I3-VP), and S3 (I3-S3) are preserved, and notes "That ASN will extend the closed domain... and must re-derive S8-depth and S8a for the complete post-state."
**Problem**: The shift creates a gap in the V-position sequence, violating D-CTG (VContiguity, ASN-0036), D-MIN (VMinimumPosition, when p = min(V\_S(d))), and D-SEQ (SequentialPositions). The worked example confirms: the post-state {[1,1], [1,2], [1,5], [1,6], [1,7]} has a gap between [1,2] and [1,5], breaking contiguity. Insert-at-start (p = [1,1]) vacates the minimum position, breaking D-MIN. The ASN neither notes these violations nor lists D-CTG/D-MIN/D-SEQ among the invariants the INSERT ASN must re-establish.
**Required**: Add a paragraph after the structural preservation derivations explicitly identifying which arrangement invariants are NOT preserved by the shift alone (D-CTG, D-MIN, D-SEQ), and include them in the forward-looking guidance for the INSERT ASN alongside S8-depth and S8a. The reader needs to know the shift's post-state has a well-typed but non-contiguous arrangement.

### Issue 2: I3-VD establishes S8-depth only for subspace S
**ASN-0082, I3-VD derivation**: "We derive that S8-depth and S8a hold for the post-state M'(d)"
**Problem**: I3-VD is quantified over `subspace(v₁) = subspace(v₂) = S`, covering only the affected subspace. S8-depth is a universal property over all subspaces. The cross-subspace case (S' ≠ S) follows from I3-CX — positions in other subspaces are unchanged from dom(M(d)), where S8-depth already holds — but this one-sentence argument is absent.
**Required**: Either extend I3-VD's quantifier to all subspaces, or add a sentence noting that for S' ≠ S, S8-depth is preserved because I3-CX retains exactly the pre-state positions, on which S8-depth holds by hypothesis. As written, the claim "S8-depth holds for the post-state M'(d)" is not fully derived.

### Issue 3: I3-C attribution overstates what S9 provides
**ASN-0082, Post-Insertion Shift**: "The content-store frame (I3-C) makes explicit that the shift is arrangement-only — the content store C is unmodified, as guaranteed by S9 (TwoStreamSeparation, ASN-0036)."
**Problem**: S9 guarantees `dom(C) ⊆ dom(C')` and value preservation for existing addresses — the preservation direction. It does not guarantee `dom(C') ⊆ dom(C)`. I3-C claims `dom(C') = dom(C)`, which additionally requires that no new content is stored during the shift. That reverse inclusion follows from the shift being purely an arrangement operation, not from S9.
**Required**: Adjust the attribution: S9 provides the preservation direction; the equality requires additionally that the shift creates no new content, which is a design property of the operation (arrangement-only), not a consequence of S9. One way: "S9 guarantees existing content is preserved; the shift stores no new content, so dom(C') = dom(C)."

## OUT_OF_SCOPE

### Topic 1: Span denotation equivalence under shift
I3 guarantees point-level preservation; I3-S lifts this to span endpoints. The intermediate property — that the shift bijects depth-m members of ⟦σ⟧ to depth-m members of ⟦σ'⟧ — is not established. This would close the loop between the point-level and span-level views.
**Why out of scope**: A derived span-algebra property building on I3 and I3-S; belongs in the span algebra layer.

### Topic 2: Shift composition for sequential insertions
Two insertions in sequence produce two shifts; the second must account for the first's displacement. TS3 (ShiftComposition) applies at the tumbler level but the arrangement-level composition (with region boundaries changing between steps) is not addressed.
**Why out of scope**: Sequential operation composition is an operation-layer concern; this ASN establishes the single-step property.

VERDICT: REVISE
