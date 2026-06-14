# Channel Assignment — ASN-0133 review-17

**Date:** 2026-06-13 18:05

## Issue 1: Q0's exhaustiveness argument omits the collection behavior atoms, so the "for every registry" claim is unproven for the general heterogeneous-view case
Reason: The fix is internal — it re-applies machinery already defined in the dependency cone: ASN-0129's UV atom list and PC3's cross-view rebuild device, ASN-0086's ActiveSubset, and QD's set-valued closure, extended to `succs`/`sources_to`/`chain`/`stale` (the review even supplies the exact rebuild forms, including the `elems(chain)`/`is_in_chain` route for the sequence-typed atom). No design-intent question (Nelson) and no implementation evidence (Gregory) bears on whether these formal atoms rebuild over the active fixed-view bases.
