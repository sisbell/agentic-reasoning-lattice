# Channel Assignment — ASN-0119 review-42

**Date:** 2026-06-10 08:14

## Issue 1: the value-dependent link invariants are discharged once but bracketed by a forward and a backward signpost
Reason: Purely an editorial consolidation — the discharge of CL-OWN/CL-UNIQ already exists in the S8★ paragraph; the fix only removes the redundant "discharged below"/"already discharged above" signposts. No design intent or implementation evidence bears on prose organization.

## Issue 2: RA6 is cited before it is introduced
Reason: A label-ordering fix internal to the ASN — the fact `Σ'.L = Σ.L` already appears unlabeled in "The two streams," so attaching the RA6 label there (or before the closure rule that consumes it) is derivable from the note's own content with no external input.
