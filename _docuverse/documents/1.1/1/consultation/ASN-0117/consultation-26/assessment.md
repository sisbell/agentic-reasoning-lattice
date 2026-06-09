# Channel Assignment — ASN-0117 review-26

**Date:** 2026-06-09 10:49

## Issue 1: Per-state invariant accounting omits S8★ (and other extended-state invariants the contraction touches)
Reason: The fix is a citation/consistency matter internal to the formal scaffolding the note already invokes — uniformly invoking ExtendedReachableStateInvariants (ASN-0047) for DELETE as a valid composite of elementary K.μ⁻/K.μ⁺ steps, or adding the S8★/S3★-aux/CL-OWN/CL-UNIQ clauses. No design intent or implementation evidence is needed; the invariant family and its preservation under valid composites are already defined in the cited foundation ASNs.

## Issue 2: Rationale-of-importance prose and repeated restatement of the non-destruction message (anti-bloat)
Reason: This is a pure editorial consolidation — removing meta-prose and de-duplicating the non-destruction motif across sections. It is derivable from the note alone; no external channel bears on what to cut.
