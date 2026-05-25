# Channel Assignment — ASN-0075 review-5

**Date:** 2026-05-25 14:30

## Issue 1: D-EXH mutual exclusion not derived
Reason: The fix is a proof-structure expansion using only the definitions of CURRENT, DELETED, NEVER_INCLUDED already present in the ASN. No design intent or implementation evidence is required to enumerate per-row label assignments.

## Issue 2: D-ACT "and conversely" leaves the converse implicit
Reason: The fix is a clarification of intended meaning using notions (V-adjacency, I-adjacency, origin) already defined in the ASN and its foundation. No external evidence needed to write the explicit converse.

## Issue 3: D-EXH "impossible row" argument requires the lemma's hypothesis to discharge L14
Reason: The fix is a routing choice between two foundation-provided paths (L14 from `a ∈ dom(C)`, or L0 + SC-NEQ from `subspace_I(a) = s_C`); both routes use lemmas already cited from ASN-0036/ASN-0047. No external channels needed.
