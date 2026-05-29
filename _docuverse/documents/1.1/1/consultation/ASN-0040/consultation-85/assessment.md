# Channel Assignment — ASN-0040 review-85

**Date:** 2026-05-29 02:08

## Issue 1: "Correspondence to the allocator framework" paragraph is unused scaffolding
Reason: Pure deletion of an unused paragraph that the ASN itself states advances no downstream reasoning (S0, B7, B1, B10 all prove directly from TA5/TA5a). No design intent or implementation evidence is needed to remove dead scaffolding.

## Issue 2: B7 proof opens with a defensive justification of its own method
Reason: Removing meta-prose about why T10a.6 is not used; the direct contradiction argument already present in the proof stands alone. Fully internal editorial fix.

## Issue 3: Max-existence well-definedness is re-derived verbatim in Bop
Reason: The duplicated max-existence fact is already established in NextAddress's well-definedness justification within this same ASN; replacing the re-derivation with a citation is internal.

## Issue 4: S0 proof carries a scope-defending clause that is argument-external
Reason: The domain is already fixed by the S0 contract's preconditions (p ∈ T, d ≥ 1); dropping the redundant scope-defending clause is derivable from the ASN's own contract.
