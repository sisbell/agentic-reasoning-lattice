# Review of ASN-0112

This ASN is mathematically careful — the displacement arithmetic (D0/D1 round-trip, the `#origin_d ≤ #reach_d` reach biconditional, the cross-subspace `k=1` overshoot) all check out against the worked examples, and V14's split of permanence into S0/P0 (content) vs L12 (links) is genuinely sound. The findings below are anti-bloat, as the classifier directs.

## REVISE

### Issue 1: Count-coincidence stated three-plus times in one section
**ASN-0112, "The origin is permanent; the extent tracks quantity" and V10**: The insertion paragraph establishes the coincidence — "`extent_d = [0,…,0,n_s]`, whose final component equals `|O(d)| = n_s` exactly, *because* the run is dense (D-SEQ★) and pinned at uniform depth … (D-MIN★, S8-depth)". A few lines later V10's narrative repeats the *same argument*: "the content subspace is the sole occupied subspace, hence dense (D-SEQ★) and depth-uniform (S8-depth), so the count-coincidence (extent's final component `= |O(d)|`) holds in every instance of V10; it fails only in the cross-subspace regime (V6)." The V10 table entry then restates it a third time ("holds throughout this content-maximal case and fails only cross-subspace (V6)"), and Open Question 2 echoes it a fourth.
**Problem**: The identical dense-run/depth-uniform justification and the identical "fails only cross-subspace" caveat appear in two adjacent body sentences plus the table. A reader following V10 reads the same reasoning twice in a row.
**Required**: State the coincidence-and-its-confinement once (the insertion paragraph already does it with the full `because` derivation); have V10's narrative and table reference it rather than re-derive it.

### Issue 2: V6 depth paragraph closes by restating V2/V3's own scoping
**ASN-0112, "Exact cover within a subspace; a bounding box across subspaces"**: "The well-formedness (V2, V17) and covering (V2) claims hold for `m_C ≠ m_L` as well; only the V3 tightness claim is restricted to the same-depth reach the uniform-depth discipline guarantees."
**Problem**: This re-derives nothing. V2 already proves coverage and well-formedness "unconditionally … without assuming level-uniformity," and V3 already restricts tightness to same-depth tumblers. The sentence repeats those scoping decisions in the cross-subspace context where they were already proven to hold generally.
**Required**: Drop the restatement; the preceding sentence ("The covering argument (V2) was proved without any endpoint depth relation and so still holds") already discharges the cross-subspace case.

### Issue 3: Placement-justifying meta-prose on the reach biconditional
**ASN-0112, V2**: "We establish the **reach biconditional** once, here, where D0/D1 live: …"
**Problem**: "once, here, where D0/D1 live" justifies *where* the claim sits rather than advancing it — the kind of document-ordering rationale that accretes across cycles. The biconditional is then correctly referenced three times downstream ("by the V2 reach biconditional"), which is fine; only the placement gloss is noise.
**Required**: State the biconditional without the placement justification ("The reach equals `reach_d` exactly when `#origin_d ≤ #reach_d`: …").

## OUT_OF_SCOPE

None — the note correctly fences per-subspace reporting (ASN-0113), content delivery, and authorization (the BERT session gate is noted as a deployment concern and explicitly excluded from the value precondition), consistent with the scope list.

VERDICT: REVISE
