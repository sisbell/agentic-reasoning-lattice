# Channel Assignment — ASN-0086 review-156

**Date:** 2026-06-01 05:03

## Issue 1: R0's formal statement omits the post-state conformance its proof establishes and downstream lemmas rely on
Reason: The fix is internal — R0's proof already discharges the full state-local L/S-invariant catalog at the fresh key conjunct-by-conjunct, and R5 Steps 3–4 already cite "conforming post-state." Surfacing this in the formal conclusion and Properties table row is a contract/proof alignment task derivable entirely from the ASN's existing content; no design intent or implementation evidence is required.
