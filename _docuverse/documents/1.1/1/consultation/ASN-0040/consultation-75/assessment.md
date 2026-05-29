# Channel Assignment — ASN-0040 review-75

**Date:** 2026-05-29 00:46

## Issue 1: The necessity of condition (i) misses the real structural reason — stream aliasing
Reason: Fully internal — S2, B7, and B8 are all present in the ASN; the fix is to chain the existing aliasing identity (S2) to the existing disjointness/uniqueness properties. No design intent or implementation evidence is needed.

## Issue 2: The necessity claim for (i) is of a different kind than for (ii)/(iii), and the framing conflates them
Reason: Fully internal — distinguishing stream-T4 necessity from non-aliasing necessity is a restructuring of claims already proved in sub-cases (a), (b), and Issue 1, with no appeal to external sources.

## Issue 3: Reviser-drift duplication and overstated cross-reference
Reason: Fully internal — deduplication is editorial, and the B0/T8 relationship is already flagged as an open question within the ASN, so the corrected wording is derivable from the ASN's own stated scope.
