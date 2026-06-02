# Channel Assignment — ASN-0098 review-45

**Date:** 2026-06-02 15:28

## Issue 1: LP-Fin discharges a case by "applied symmetrically" across a differing index bound
Reason: The fix is a proof-internal expansion — the `#d ≤ #d_0` case uses the same T1 case (i) divergence machinery already present in sub-case (ii), just re-indexed over `1 ≤ j ≤ #d`. All ingredients (T1, structural form of `s`/`s ⊕ ℓ`, prefix-copy region) are in the ASN.

## Issue 2: project-definition prose pre-states LP6, LP7, LP8 as hand-waves
Reason: Pure deletion of a redundant preview; LP6/LP7/LP8 carry the statements rigorously later. No external input needed.

## Issue 3: "Working reference frame" note is a use-site operation inventory
Reason: Editorial compression — the frame identification (ASN-0047 over ASN-0093) is already in the ASN; only the operation roll-call is dropped.

## Issue 4: LP13 aftermath paragraph restates the storage/navigability split as essay and forward-references LP17
Reason: The consequence (LP13 is independent of every `Σ.M` term) is already the formal content of LP12 vs LP13; compressing to one sentence and removing the forward pointer is internal editing.

## Issue 5: Boundary section justifies lemma scope rather than advancing it
Reason: The decidability fact LP-Fin needs (finite interval ⇒ decidable tightness predicate) is already established; dropping scope-justification and naive-formulation rationale is editorial.

## Issue 6: Trace "branch point" carries bookkeeping prose disproportionate to its content
Reason: Straightforward prose replacement with a single sentence; the state transitions themselves are unchanged and fully specified in the ASN.
