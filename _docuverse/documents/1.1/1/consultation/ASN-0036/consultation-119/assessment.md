# Channel Assignment — ASN-0036 review-119

**Date:** 2026-05-28 21:20

## Issue 1: S7d's rationale paragraph is positioning meta-prose, not content
Reason: Pure deletion of a positioning sentence; the axiom and baptism quote already stand on their own. No design intent or implementation evidence required.

## Issue 2: Operation-preservation deferred in four separate places
Reason: Consolidating redundant deferrals into the single Open Question slot is an internal editorial decision; the content of the deferral is unchanged and derivable from the ASN.

## Issue 3: Within-subspace lemma *Remark* imagines a precondition-excluded case
Reason: The lemma's proof is already complete and S8-depth is a stated precondition; removing duplicated meta-justification needs nothing beyond the ASN's own structure.

## Issue 4: The "Corollary" is embedded inside the S8 proof and duplicates ShiftPreservation
Reason: Relocating a one-line consequence of ShiftPreservation (already proved) out of the proof spine is internal restructuring; all referenced results are present in the ASN.

## Issue 5: ValidInsertionPosition structural claims verified twice
Reason: Choosing whether the shared prose block or the per-predicate contracts carry the postconditions is an editorial dedup; both versions already exist in the ASN and agree.
