# Channel Assignment — ASN-0070 review-74

**Date:** 2026-06-03 03:29

## Issue 1: F-canon-form definition states what a downstream proof *does* instead of stating the shape
Reason: Purely editorial relocation — state the width shape `(s, δ(c, m_S(d)))`, `c ≥ 1` directly in the definition and let the necessity argument live once in F-canonical Step 1, which is already present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: F-subspace Consequence restates its own formula in prose
Reason: Deletion/compression of a redundant prose restatement of equalities already displayed; the L4-admissibility pointer is internal to the ASN. Fully derivable from the ASN's own content.
