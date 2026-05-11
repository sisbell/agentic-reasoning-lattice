# Channel Assignment — ASN-0036 review-80

**Date:** 2026-05-11 01:24

## Issue 1: S7a Formal Contract misattributes T4c
Reason: Pure citation correction — the body of the ASN already cites T4b (UniqueParse) correctly for the projections. The fix is internal consistency between the body and the contract; no design intent or implementation evidence is needed.

## Issue 2: S8 dependency list omits used premises
Reason: The body proof of S8 explicitly invokes S3, S7b, and S7c (all properties defined within this same ASN). The fix is mechanical — add the cited premises to the dependency list. Derivable from the ASN alone.

## Issue 3: S7 Preconditions list omits T4b
Reason: Internal inconsistency — the Properties Introduced table already cites T4b for S7, and the body proof uses T4b's projections explicitly. Just add T4b to the Preconditions list. No external input needed.

## Issue 4: D-CTG dependency lists are inconsistent between body and table
Reason: The review identifies the body's list (S8a, S8-depth, T1) as correct for D-CTG's statement; T0(a) and T3 belong to D-CTG-depth's proof. The fix is internal reconciliation of two lists within the ASN.

## Issue 5: S8a Preconditions cite S7b without explaining its role
Reason: Whether S7b is load-bearing for S8a's conjuncts is determined by reading S8a's own proof — the three conjuncts follow from T4 and T0 plus the axiomatic commitment, with S7b serving only as architectural parallel. The choice between removing S7b or reframing the precondition is internal to the ASN.

## Issue 6: D-CTG-depth dependency list omits S8a
Reason: The proof of D-CTG-depth uses S8a's commitment that v₁ is the subspace identifier when deriving `subspace(w) = w₁ = (v₁)₁ = 1`. The fix is to add S8a to the dependency list — purely mechanical cross-reference repair.
