# Channel Assignment — ASN-0119 review-32

**Date:** 2026-06-10 04:58

## Issue 1: P4a case-2 narrows "any other final composite" to K.μ~ — a characterization that is not exhaustive
Reason: The fix is a restructuring of the P4a case analysis — making case 2 range over every non-REARRANGE final composite and naming the combined induction. Both the counterexample (standalone K.μ⁺) and the corrected argument are formal constructions within the ASN-0047 invariant framework the note already imports; the review fully specifies the recast. Whether the case analysis is exhaustive is internal formal reasoning, untouched by design intent or implementation behavior.

## Issue 2: redundant restatement of where the couplings/boundary-properties are evaluated (anti-bloat)
Reason: Pure anti-bloat deletion of a non-advancing sentence; the review identifies the exact sentence and confirms its one residual fact is already implied by the preceding extension sentence. Entirely internal — no channel bears on a redundancy cut.
