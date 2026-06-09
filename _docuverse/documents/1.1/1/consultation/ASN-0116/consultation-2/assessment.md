# Channel Assignment — ASN-0116 review-2

**Date:** 2026-06-08 19:52

## Issue 1: New-block well-formedness is not discharged by the cited ASN-0082 lemmas
Reason: Internal. All needed facts are already present in the ASN — S8a via OrdShiftHom on `p`, depth `#shift(p,k)=m`, single-valuedness from the disjoint gap intervals, and `shift(a,k) ∈ dom(C')` from I-ALLOC. The discharge is a reassembly of the ASN's own machinery, not new design intent or implementation evidence.

## Issue 2: Contiguity is miscited; the lemmas named are contraction lemmas
Reason: Internal. The ASN already contains the load-bearing interval argument (consecutive, disjoint, union `{1,…,N+n}`); the fix is to drop the inapplicable D-*-post citations and reframe that argument as the proof. No external channel resolves a miscitation.

## Issue 3: Precondition permits a subspace mismatch between position and allocation
Reason: Internal. The allocation is K.α, which the ASN already states yields `subspace_I(a) = s_C`; type consistency with the cited S3★ forces `S = s_C`. The constraint follows from material already in the ASN.

## Issue 4: P4's stated resolved-witness set is incomplete
Reason: Internal. The omitted witness classes are exactly the left positions (I-LEFT) and cross-subspace positions (F-SUB), both already established clauses of the Effect/Frame. Correcting the set identity is a bookkeeping fix from the ASN's own content.
