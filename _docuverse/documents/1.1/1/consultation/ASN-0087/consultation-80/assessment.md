# Channel Assignment — ASN-0087 review-80

**Date:** 2026-06-04 13:10

## Issue 1: "Permanence of the Binding" restates the same conclusion redundantly
Reason: Pure prose-redundancy edit — dropping a restatement of the clause-(v) derivation that is already present in the section. No design intent or implementation evidence is involved; the fix is internal to the ASN.

## Issue 2: "discoverability is a derived property of (L, M)" duplicated across sections
Reason: De-duplication of an insight already stated in *What Is Indexed?* and the M-NoIndexState row; reordering *Side Effects* to open with the LP12 delta. The load-bearing content (LP12, the `ran` delta) is already in the ASN, so the fix is internal.
