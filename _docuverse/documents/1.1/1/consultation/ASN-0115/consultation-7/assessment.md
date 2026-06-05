# Channel Assignment — ASN-0115 review-7

**Date:** 2026-06-05 06:22

## Issue 1: R9 origin-traceability cites S7 for positions S7 does not cover
Reason: Purely formal scope fix — restrict the quantifier to content positions or invoke the link-address provenance machinery (ASN-0043 L1a, ASN-0086 HomeOriginCoincidence) the reviewer already names; both are established formal claims in the substrate, and R10's content/link split is already present in this ASN, so the correction is internally derivable without design intent or implementation evidence.

## Issue 2: R8 omits the content-position hypothesis its proof depends on
Reason: Purely formal fix — add `subspace(v) = s_C` (equivalently `a ∈ dom(Σ.C)`) as a hypothesis, or add the link-share sub-case; SD (store disjointness), already cited in this ASN, forces both positions into one subspace once they share `a`, so the patch follows from definitions and claims already present.
