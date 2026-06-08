# Channel Assignment — ASN-0102 review-37

**Date:** 2026-06-07 22:47

## Issue 1: Superfluous V-adjacency argument in X8's within-reference case
Reason: Purely internal editorial fix — the conclusion already follows from non-I-adjacency via M7 (both ASN-0058 M7/M12 and the construction `c_{j+1} = c_j + n_j` are present in the ASN), so the source-contiguity sub-argument is dropped using only material already cited here.

## Issue 2: The Σ.R-vs-Contains_C distinction is drawn twice
Reason: Purely internal deduplication — both passages are within ASN-0102; state the distinction once at the Definition's provenance effect and have X14 reference it. No design intent or implementation evidence bears on where the prose lives.
