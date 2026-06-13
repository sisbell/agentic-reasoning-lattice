# Channel Assignment — ASN-0132 review-3

**Date:** 2026-06-13 04:07

## Issue 1: CN-MONO cites the wrong increment lemma — and does so inconsistently with its own E-INV correction
Reason: This is a pure citation correction internal to the specification. The review itself identifies the exact replacement (K.λ's single-fresh-address effect from ASN-0093; FL-MON/FL-WP(a) from ASN-0121), all of which the ASN already cites in the same paragraph; the increment is a formal cardinality claim, not a matter of design intent, and the citation hygiene concerns the abstract spec's internal structure, not implementation behavior — so neither channel is needed.
