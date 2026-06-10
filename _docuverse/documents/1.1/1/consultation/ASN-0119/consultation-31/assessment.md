# Channel Assignment — ASN-0119 review-31

**Date:** 2026-06-10 04:39

## Issue 1: The P4a trace argument asserts a universal the ASN itself refutes
Reason: Internal fix. The repair is a pure logical scoping change — restrict the decomposition claim to REARRANGE-ending traces and note that other-route traces are discharged by their own final operation within ASN-0047's P4a induction. The counterexample route (K.μ~) is already flagged by the ASN itself, and P4a's inductive structure is in the already-cited ASN-0047; no design intent or implementation evidence is needed.

## Issue 2: Forward-reference / document-structure meta-prose (anti-bloat)
Reason: Internal fix. Purely an editorial removal of signposting and justification clauses ("reconstructs ... rather than citing them", "for use below", the forward pointer to RA7a); no design intent or implementation evidence is involved.
