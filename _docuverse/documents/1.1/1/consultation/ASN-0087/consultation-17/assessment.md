# Channel Assignment — ASN-0087 review-17

**Date:** 2026-06-03 10:24

## Issue 1: First-link V-position depth is not determined by the current state, contradicting the "computed from state" claims
Reason: Choosing among the fix options (input `m`, fix `m=2` by convention, or expose the free parameter) requires knowing whether link V-positions sit at a canonical/fixed depth — design intent (Nelson) and what the implementation actually does (Gregory) determine which reconciliation is correct rather than merely internally consistent.
Nelson question: Did the design intend links to occupy a canonical depth within a document's link subspace, or is the depth at which a document's first link is placed semantically arbitrary?
Gregory question: When udanax-green places the first link in a document's link subspace, does it fix the V-position to a particular depth, and if so, what depth and is it constant across documents?
