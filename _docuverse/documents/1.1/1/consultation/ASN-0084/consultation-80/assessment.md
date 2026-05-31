# Channel Assignment — ASN-0084 review-80

**Date:** 2026-05-30 17:19

## Issue 1: R-PIV / R-SWP cite R-NS for a fact that needs only the frame condition, importing an unnecessary forward reference
Reason: Pure citation-hygiene fix internal to the ASN — swap the R-NS citation for the already-present R-FRAME-P(a)/R-FRAME-S(a) frame condition, which the ASN itself flags as equivalent. No design intent or implementation evidence bears on which lemma label discharges a non-S value fact.

## Issue 2: R-COMM proves a non-S (and subspace-S exterior) case that no consumer uses
Reason: Scope-trimming choice derivable from the ASN's own dependency structure — either narrow R-COMM to α/μ/β or add a one-line note at the R-BLK Phase 3 consumption site. The set of consumers and what each branch licenses is fully visible in the ASN; no external channel is needed.
