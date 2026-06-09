# Review of ASN-0117

This is a strong, well-grounded note. The two-layer separation is handled correctly, the composite/elementary case split on `R = ∅` is sound, the wp analysis is genuinely non-trivial with correct per-link (not per-slot) quantifier reasoning, and the boundary cases (suffix-delete, delete-everything, leading-span, multi-position shift, within-document sharing, cross-document transclusion) are all exercised against concrete arithmetic. The frame discharge (J0/J1★/J1'★ vacuity, E/R/L frames via the component-step frames) checks out, and the bridge from ASN-0082's displacement to ASN-0047's transition vocabulary is legitimate because both produce the identical `M'(d)`. I found no correctness defect.

The note carries the anti-bloat classifier, and the findings below are placement/density issues, not logic errors.

## REVISE

### Issue 1: Discursive justification embedded in a structural effect-clause
**ASN-0117, DELETE Effect list, (DEL-REMOVE)**: the clause expands into a ~200-word paragraph arguing why removal is stated as a count-plus-label-vacancy rather than per-pair absence, walking through within-document sharing and S5/M13.
**Problem**: The content is load-bearing and correct — but it is a discursive remark sitting inside a structural effect-bullet, where every sibling clause (DEL-SHIFT, DEL-LEFT, DEL-DOM, DEL-CIMM) is a one-line statement-plus-citation. The asymmetry forces the reader to parse an essay to extract the clause. Per the anti-bloat guidance, flag the placement, not the existence.
**Required**: Reduce DEL-REMOVE to its statement (the count `N − c` plus top-`c` label vacancy, with "deleted I-addresses persist in `C`"), and relocate the count-vs-per-pair rationale to a short standalone remark adjacent to P1 — where P1 already points to it.

### Issue 2: Essay restatement in "A span, not a position: binding versus being"
**ASN-0117, §"A span, not a position"**: the section runs several paragraphs of metaphorical framing ("the seam between binding and being," "an arrangement feature and an existence fact," "what witnesses that the seam is real") around facts already established as P0/P1/P4/P5.
**Problem**: The one substantive derived claim — that only a span (having extent) exposes the binding/existence separation, whereas a position binds nothing — is stated and then re-stated three times in different words. The surrounding paragraphs advance no reasoning beyond P0–P5; they restate them in prose. This is essay content occupying a structural slot.
**Required**: Compress to the single derived point (a span carries both an arrangement feature and an existence fact; deleting it separates them — DEL-REMOVE strips the binding while P0 keeps the bytes), 2–3 sentences. Drop the repeated metaphor passes.

## OUT_OF_SCOPE

### Topic 1: Deletion spanning below the document origin
The first open question (a span beginning before the first arranged position) is correctly excluded by the precondition (`p = q_J`, `J ≥ 1`, `p ∈ V_S(d)`) and properly deferred. Not an error here.

### Topic 2: Concurrent operations without a serializing authority; backtrack reconstruction; content-index invariants; cross-document orphan obligations
The remaining open questions (concurrency, backtrack-state requirements, discovery-index relationships, orphan-link obligations across sharers) are new territory appropriately left to future ASNs.

VERDICT: REVISE
