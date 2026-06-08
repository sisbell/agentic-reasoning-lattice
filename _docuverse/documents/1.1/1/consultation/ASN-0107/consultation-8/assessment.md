# Channel Assignment — ASN-0107 review-8

**Date:** 2026-06-07 22:31

## Issue 1: A2 invokes document "subspaces" that the model does not define
Reason: The fix is purely a restatement using vocabulary the model already supplies — the two-subspace convention (SubspaceConventionAxiom) and the slot/region distinction are both already cited in the ASN, so the correction is derivable internally with no design intent or implementation evidence required.

## Issue 2: The worked example's type position violates referential integrity
Reason: The fix is mechanical — pick a construction (declare `τ ∈ dom(Σ.L)` with `origin(τ)=d` via L4(c), or relocate the type position to the content subspace and adjust retention) and discharge S3★/CL-OWN, all of which are foundation invariants already referenced in the ASN; no design intent or code evidence is needed to choose a valid witness.
