# Channel Assignment — ASN-0040 review-62

**Date:** 2026-05-28 23:06

## Issue 1: B6 necessity proof does not cover the zero-count T4 violation
Reason: The fix adds a proof clause derivable entirely from the ASN's own machinery — TA5(b) position preservation carries the zero count into c₁, B5a adds no zeros, and T4's own `zeros(t) ≤ 3` clause is the bound violated. No design intent or implementation evidence is needed.

## Issue 2: Defensive meta-prose and document-ordering justification in B6 necessity
Reason: Pure editorial restructuring — relocating the existing S2-based disjointness material adjacent to S2 and deleting placement disclaimers/roadmap sentences. No external information required.

## Issue 3: Bop well-definedness re-derives NextAddress; B0b carries a structural-justification sentence
Reason: Pure editorial deduplication — replace the branch re-enumeration with a NextAddress citation plus B_fin discharge, and drop B0b's framing clause. Both cited results are already in the ASN.
