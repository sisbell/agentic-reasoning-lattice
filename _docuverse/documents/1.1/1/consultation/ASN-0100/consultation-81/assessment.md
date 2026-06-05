# Channel Assignment — ASN-0100 review-81

**Date:** 2026-06-05 05:18

## Issue 1: Fresh-address invariant discharge is scattered across sections, each deferring to §Atomicity
Reason: Pure restructuring — the consolidated argument already exists in §Atomicity; the fix only deletes forward-pointer sentences. Derivable from the ASN alone.

## Issue 2: §Position Constraints restates region-emptiness already established three times over
Reason: Editorial reduction — the region-emptiness split is already established in (INS.μ⁻-fires), §Effect Three, and the worked examples; the fix trims duplication. Derivable from the ASN alone.

## Issue 3: Pre-state composite-boundary status is an unstated precondition
Reason: The fix adds a standing precondition (Σ is a composite boundary) so pre-state P4★/P4a/P7a are available; the boundary semantics come from ASN-0047, already cited, and the requirement is internal to the proof's own logic. Derivable from the ASN alone.

## Issue 4: Defensive allocation-history paragraph in the empty-document example
Reason: Editorial trim — the example's own stipulation fixes the first-emission branch, and the keying-on-dom(C) fact is already in INS.alloc. Derivable from the ASN alone.
