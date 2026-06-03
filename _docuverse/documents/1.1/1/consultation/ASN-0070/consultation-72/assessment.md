# Channel Assignment — ASN-0070 review-72

**Date:** 2026-06-03 03:15

## Issue 1: F0 closing paragraph restates itself and foreshadows named claims
Reason: Pure prose deduplication — collapse the two equivalent sentences and drop a foreshadowing clause that F-empty already owns. No design intent or implementation evidence is at stake; the fix is entirely internal to the ASN's own text.

## Issue 2: F-multi carries subspace generality that CL-UNIQ already excludes, then explains the exclusion in a Remark
Reason: Scoping the postcondition to `s_C` and trimming the Remark follows from claims already cited in-ASN (CL-UNIQ's injectivity on `dom_L`, K.μ⁺'s lack of an injectivity constraint). The vacuity of the `s_L` branch and the surviving realisability witness are both derivable from existing dependencies — no channel needed.
