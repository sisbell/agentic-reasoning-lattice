# Revision Categorization — ASN-0043 review-24

**Date:** 2026-03-23 18:46



## Issue 1: home(a) domain extension
Category: INTERNAL
Reason: The fix is entirely derivable from existing definitions — T4 (HierarchicalParsing) is defined for all tumblers regardless of subspace, and the field-extraction formula is already stated in the ASN. Either option (a) or (b) requires only reorganizing definitions already present.

## Issue 2: GlobalUniqueness scope extension
Category: INTERNAL
Reason: The ASN already identifies the exact properties needed (T9, T10, T10a) and already states that they depend on tumbler arithmetic rather than subspace identity. The fix is to make this observation explicit in the proof text — no external evidence is required.
