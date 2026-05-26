# Channel Assignment — ASN-0094 review-90

**Date:** 2026-05-25 21:34

## Issue 1: Multi-paragraph defensive prose for each commitment in Scope section
Reason: Editorial cleanup — removing justification/out-of-scope prose around commitments. The commitments themselves remain unchanged; what's stripped is essay-style explanation of why each exists. Derivable from the ASN.

## Issue 2: ShapeRegistry's lifetime-constancy justification paragraph
Reason: Editorial cleanup — strip downstream-consumer rationale and "what would invalidate" hypothetical. The property statement is unchanged. Derivable from the ASN.

## Issue 3: FDD's "Strictly stronger than Sh4" paragraph
Reason: Editorial cleanup — motivation prose preceding a corollary. The corollary (Sh4HoldsAtFDDRegisteredK) and the structural fact C ⊆ C_fd are already stated. Derivable from the ASN.

## Issue 4: SHCD's "Unlike the Sh4/FDD contracts" comparison paragraph
Reason: Editorial cleanup — meta-commentary comparing contracts. Clause (i)–(ii) of the single-home commitment already state the behavior. Derivable from the ASN.

## Issue 5: "Standalone admissibility" defensive note for Resolution
Reason: Editorial cleanup — Sh0–Sh4 already quantify over every K ∈ T_cat, so the note defends against a non-issue. Derivable from the ASN.

## Issue 6: Cross-`~`-class concurrency sentence in Sh4 contract
Reason: Editorial cleanup — single-sentence comment on a non-concern, already excluded by the single-process scope clause. Derivable from the ASN.

## Issue 7: Citation-guidance commentary after Sh4HoldsAtFDDRegisteredK
Reason: Editorial cleanup — meta-commentary about citation practice. Derivable from the ASN.

## Issue 8: "This is the only correctness fact..." meta-sentence in Sh4 contract correctness
Reason: Editorial cleanup — terminal meta-sentence about downstream use. Derivable from the ASN.

## Issue 9: Empty-G semantics interpretive paragraph for BundledDirectedPair
Reason: Editorial cleanup — layer-choice style guidance the framework does not enforce. Derivable from the ASN.

## Issue 10: Distinction-from-Resolution comparison paragraph
Reason: Editorial cleanup — style-guide "use X when..." content; the shape registry's tuple components already encode the distinction. Derivable from the ASN.

## Issue 11: Duplicate "Note on `pair_K`'s set-equality argument"
Reason: Editorial cleanup — two paragraphs say the same thing across walkthroughs. Both defend against a hypothetical redundancy. Derivable from the ASN.

## Issue 12: Inline Observe_K semantics re-derivation in Sh4 contract clause (i.a)
Reason: Editorial cleanup — Observe_K is a foundation Definition in ASN-0086 cited within the same ASN. Replace with a one-sentence citation. Derivable from the ASN and its foundation citation.

## Issue 13: Sh-conf Rejection Pattern 1's out-of-scope defensive prose
Reason: Editorial cleanup — imagines a case the Emit_K routing commitment already excludes. Derivable from the ASN.

## Issue 14: Consequences section reads as essay content
Reason: Editorial cleanup — items (b) and (d) explicitly disclaim what they cover, and (a) recapitulates the catalog. Movable to Open Questions or deletable. Derivable from the ASN.

## Issue 15: Initial-State Baseline duplicates Empty-baseline commitment
Reason: Editorial cleanup — first sentence restates the Empty-baseline commitment from the Scope section. The unique load-bearing content (Σ_0 convention, dom(Σ_init.L) = ∅) remains. Derivable from the ASN.

## Issue 16: TypedRelationCatalog's lifetime-constancy duplication
Reason: Editorial cleanup — lifetime constancy is stated both in TypedRelationCatalog and ShapeRegistry. Consolidate to one site. Derivable from the ASN.

## Issue 17: Per-class registration discipline paragraph
Reason: Editorial cleanup — strip the "Since..." motivation and "break preservation" hypothetical; first sentence states the discipline. Derivable from the ASN.

## Issue 18: Sh4 contract's atomicity scope paragraph
Reason: Editorial cleanup — multi-process out-of-scope is already flagged in Open Questions; reduce to one sentence. Derivable from the ASN.

## Issue 19: Multi-paragraph proof inside CaseAClosureForLK and CaseAClosureForAK
Reason: Editorial cleanup — the lemmas exist to factor out Sh0–Sh4's Case-A dispatch, but the proof prose and Sh0–Sh4's Case-A bullets both restate the dispatch. Reconcile by picking one site. Derivable from the ASN.

## Issue 20: NonRSeparation proof attribution
Reason: Editorial cleanup — terminal sentence describes downstream consumers, not the lemma. Derivable from the ASN.
