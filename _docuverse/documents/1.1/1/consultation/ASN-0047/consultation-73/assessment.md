# Channel Assignment — ASN-0047 review-73

**Date:** 2026-05-17 04:41

## Issue 1: Notational category-mismatch for `parent(A_v(t))` / `parent(A_c(t))` in K.δ section
Reason: Pure notational fix internal to the ASN — T10a (ASN-0034) defines `parent(A) ∈ 𝒯` and the ASN's own "Characterization of `parent(A_v(t))`'s tracked domain" paragraph already identifies the correct allocator (`A_doc(parent(t))`). No design intent or implementation evidence needed; fix is mechanical alignment with existing definitions.
