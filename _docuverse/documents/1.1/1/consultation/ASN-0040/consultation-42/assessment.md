# Channel Assignment — ASN-0040 review-42

**Date:** 2026-05-28 20:21

## Issue 1: First-child increment is k=1, not the unconditional k=0 case
Reason: The fix is internal — TA5a's exact conditioning (k=1 requires zeros(p) ≤ 3) is already cited from the foundation in the ASN, and the reviewer states the correct rule; restating the sufficiency prose to match needs no design intent or implementation evidence.

## Issue 2: Notation reinvents the foundation's transition vocabulary
Reason: Pure notational alignment with ASN-0034's already-known `s`/`𝒮`/`Σ` convention; choosing a non-colliding state symbol is derivable from the foundation's published vocabulary without consulting either channel.

## Issue 3: B_type is a redundant restatement carrying only document-ordering prose
Reason: Internal editorial cleanup — `Σ.B ⊆ T` is already in the registry definition and follows from B10, both present in the ASN; no external input needed.

## Issue 4: Derivations placed before their statements with ordering justification
Reason: Reordering of self-contained prose (state B0/B0a first, then derive); the logical content is entirely within the ASN.

## Issue 5: Repeated deference to the same downstream ("activation-discipline ASN")
Reason: Consolidation of repeated forward-references into one statement is structural; the `allocated(Σ) ⊆ Σ.B` relationship is already articulated in the ASN, so no channel is required.

## Issue 6: B4 atomicity content duplicated across the document
Reason: De-duplication of B4's already-stated semantics, replacing restatements with label citations — entirely internal.

## Issue 7: Defensive frame prose that does not advance the proof
Reason: Deletion of a non-load-bearing sentence whose claim is already covered by the Bop frame; no external evidence or intent needed.

## Issue 8: Redundant restatement of B1's conclusion
Reason: Straight deletion of an orphaned sentence restating an already-proved invariant; internal.
