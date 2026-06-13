# Channel Assignment — ASN-0130 review-11

**Date:** 2026-06-12 23:46

## Issue 1: Use-site inventory in "Discipline and uniqueness"
Reason: Pure structural deletion — removing a redundant forward-pointer catalog whose content is already stated at each downstream site. No design intent or implementation evidence bears on whether to delete a duplicative sentence; the fix is internal to the note's own structure.

## Issue 2: `register_pred` is undefined on empty `A_def`
Reason: The fix is fully determined by the note's own machinery — PR-ENC already fixes `n ≥ 1` for the artifact, and PR0 already establishes the enforce-by-rejection stance for every validation failure, so adding `A_def ≠ ∅` as a precondition or validation condition (0) is internal. An empty run is incoherent by PR-ENC's own definition of an artifact, not an open question of designer intent or implementation behavior.

## Issue 3: The "bare Multi gate" rationale is stated twice, and the off-discipline failure is narrated four times
Reason: Deduplication and forward-pointer trimming across PR-SIG, PR-ENC, and the seal paragraph — purely a matter of where the note states each argument. No external evidence is needed to consolidate prose the note already contains.

## Issue 4: Essay framing in structural slots
Reason: Editorial removal of appraisal language ("nearly free," "central move") and a defensive opener, plus condensing PR0's division-of-labor paragraph to its factual core — all derivable from content already present in the note. No design intent or implementation question is involved.
