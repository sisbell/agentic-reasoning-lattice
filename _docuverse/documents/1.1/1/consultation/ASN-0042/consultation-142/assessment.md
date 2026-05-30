# Channel Assignment — ASN-0042 review-142

**Date:** 2026-05-30 10:07

## Issue 1: Multi-node bootstrap illustration duplicated between O14 commentary and the Worked Example
Reason: This is an editorial deduplication choice between two passages that already exist in the ASN; the fix consists of deleting one redundant clause-by-clause O14 verification and assigning the multi-node check a single owner. No design intent or implementation evidence is needed.

## Issue 2: Redundant restatement of O6 wedged between its two corroborating citations
Reason: The fix removes a sentence that merely restates O6's own theorem statement, already established within the ASN; the surrounding Nelson quote, Gregory confirmation, and the `pfx(ω(a)) ≼ acct(a)` corollary all remain intact. Fully internal to the ASN.
