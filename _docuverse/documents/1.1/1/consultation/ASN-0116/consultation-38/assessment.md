# Channel Assignment — ASN-0116 review-38

**Date:** 2026-06-09 11:00

## Issue 1: Clause-1 freshness discharge omits the first-emission branch
Reason: Internal fix. The ASN already cites both FirstEmissionFreshness and SubsequentEmissionFreshness (in "What is allocated") with their exact applicability conditions, and K.α's two freshness branches come from ASN-0093 already in scope; the repair is to mirror that case-split into the formal clause-1 discharge and add the first-emission start address to the empty-subspace example. No design-intent or implementation evidence is needed.
