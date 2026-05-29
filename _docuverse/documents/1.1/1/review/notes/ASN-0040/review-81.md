# Review of ASN-0040

## REVISE

### Issue 1: S0 overlap note is citation-organization meta-prose
**ASN-0040, S0 (StreamOrdering)**: "We do not, however, *invoke* T10a.7 as a foundation citation, because identifying S(p, d) with an allocator domain presupposes the alignment of the baptismal registry with allocator discipline ... the reasoning is verbatim T10a.7's and the overlap is deliberate, not an oversight."
**Problem**: This is defensive justification about a *non-citation*, not reasoning that advances S0. The proof below it is self-contained from TA5(a) + T1 transitivity and needs no such preamble. "the overlap is deliberate, not an oversight" is precisely the reviser-drift pattern (prose explaining why a citation was withheld so a future reader won't "fix" it) — that belongs in a commit message or design note, not the ASN.
**Required**: Cut to at most a one-clause note ("S0 mirrors T10a.7; re-derived here pending the `allocated(s) ⊆ s.B` alignment") or remove entirely and let the Open Question carry the alignment caveat.

### Issue 2: B7 overlap note repeats the same foundation-deferral
**ASN-0040, B7 (Namespace Disjointness)**: "This disjointness is related to T10a.5 ... and T10a.6 ... B7 is not strictly subsumed by them ... We therefore prove B7 independently while noting the foundation overlap."
**Problem**: Same pattern as Issue 1, in a second section, deferring to the same downstream construct (the T10a family). Two sections now editorialize about the T10a relationship; this is the compounding "multiple paragraphs defer to the same location" pattern the anti-bloat pass is meant to catch. The independent proof stands on its own — the reader does not need to be told it is independent or why.
**Required**: Remove the editorial paragraph; the proof and its *Depends* list already establish self-containment.

### Issue 3: B6(i) forward pointer duplicates content fully developed at B7
**ASN-0040, B6 (Valid Depth)**: "Condition (i) does more than supply a T4-valid parent ... it also disambiguates parent-depth pairs, which is what makes namespace disjointness (B7) well-posed. We exhibit the aliasing it rules out at B7."
**Problem**: This sentence forward-points to B7, where the same point is then made concretely ("B6(i)'s role is visible in the unequal-length case ... ([1, 0], 1) and ([1], 2) both produce {[1, 0, n] : n ≥ 1}"). The B6 sentence advances nothing the B7 paragraph doesn't deliver in full; it is a forward pointer to its own duplicate.
**Required**: Delete the B6 forward-pointer sentence. The role of (i) is explained at its use site (B7), which is sufficient.

## OUT_OF_SCOPE

### Topic 1: Whether S(p,d) should be unified with the T10a allocator domain
**Why out of scope**: The ASN openly notes S(p,d) "has exactly the shape of a T10a child allocator domain," and S0/B7/B1-contiguity re-walk T10a machinery. Collapsing the duplication depends on resolving `allocated(s) ⊆ s.B`, which is already logged as an Open Question. This is future alignment work, not a defect in this ASN — the baptism operation, registry state, ghost-element model, and high-water-mark reduction are genuinely new content that justify the standalone note.

The proofs themselves (S0, S1, B5, B5a, B6 sufficiency/necessity, B7 length/equal/unequal cases, B1 induction, B2, B8 both cases, B9 construction, B10) are complete, case-exhaustive, and check out against the traced examples. The findings are confined to accreted meta-prose around foundation overlap and one self-duplicating forward pointer.

VERDICT: REVISE
