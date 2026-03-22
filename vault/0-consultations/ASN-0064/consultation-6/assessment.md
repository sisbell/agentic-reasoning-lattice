# Revision Categorization — ASN-0064 review-6

**Date:** 2026-03-21 20:19



## Issue 1: F1 proof — incorrect claim about element-level members of I-span denotation
Category: INTERNAL
Reason: The fix involves correcting or qualifying a factual claim about span denotation membership, using only definitions already present in ASN-0034 (T4, element-level) and ASN-0053 (span denotation). No design intent or implementation evidence needed.

## Issue 2: F4 labeled INV — should be LEMMA
Category: INTERNAL
Reason: The fix is a label change from INV to LEMMA, justified entirely by the ASN's own definitions (F4 is a definitional consequence of findlinks, F11 establishes purity). The labeling convention is internal to the foundation ASN framework.
