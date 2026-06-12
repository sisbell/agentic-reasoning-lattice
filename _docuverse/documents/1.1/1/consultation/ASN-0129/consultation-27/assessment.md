# Channel Assignment — ASN-0129 review-27

**Date:** 2026-06-12 01:09

## Issue 1: PD0's aggregate clause contradicts itself on which class `count(D) ≤ c` inhabits
Reason: The fix is internal — the correct classification is already fully determined by PD0's own rules and proof (a count over a growing set never decreases, so `≥ c` is ⊤-stable and `≤ c` is ⊥-stable); only the headline sentence misstates what the rules grant. No design-intent or implementation question bears on rewording a classification the note itself already proves.

## Issue 2: Conjecture cross-pointer accretion across PC6, C-emit, QD-audit, and Open Question 6
Reason: The fix is internal — it is a prose consolidation problem (state the age-bearing obligation once, strip self-locating parentheticals, reduce QD-audit's deferral to the bare fact plus pointer), and every fact being relocated already exists in the ASN's own text. Neither channel can inform where redundant cross-references should live.
