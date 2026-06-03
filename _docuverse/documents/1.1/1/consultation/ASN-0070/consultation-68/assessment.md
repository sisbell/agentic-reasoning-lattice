# Channel Assignment — ASN-0070 review-68

**Date:** 2026-06-03 02:51

## Issue 1: F-canonical and F-empty rely on the vacuous-subspace convention without dispatching it in the proofs
Reason: The fix is purely internal — the Vacuous-subspace convention (`⟦⟨⟩⟧_V := ∅`, unique `⟨⟩` representative) is already stated in F-canon-form and the V-Restricted Denotation section. The revision only restructures the proofs to add an explicit base case and adjust F-empty's citation; no design intent or implementation evidence is required.
