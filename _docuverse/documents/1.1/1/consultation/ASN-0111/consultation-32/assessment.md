# Channel Assignment — ASN-0111 review-32

**Date:** 2026-06-08 13:11

## Issue 1: RL-REP is downstream use-site inventory, not a guarantee about the read
Reason: The fix is internal. Removing RL-REP follows directly from the ASN's own content: RL1 establishes the read returns exact endsets (not coverage), and RL5 already carries the coverage-interpretation content via L8. The required excision needs no design intent (Nelson) or implementation evidence (Gregory) — it is a structural cleanup justified by claims already present.
