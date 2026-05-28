# Channel Assignment — ASN-0077 review-22

**Date:** 2026-05-27 19:38

## Issue 1: O0 step (b) closure relies on implicit closed-world reading rather than a discharged premise
Reason: The fix is a foundation citation — invoke a labeled invariant (e.g., L12 from ASN-0043 as cited by ASN-0047's P3) establishing link-store append-only behavior. The required reference exists within the foundation ASN ecosystem; no design intent or implementation evidence is needed.

## Issue 2: Singleton I-span argument for case #b < #a omits the trichotomy step that excludes b < a
Reason: Pure proof-step insertion using T12's denotation definition and T1 trichotomy, both already cited in the ASN. The fix is mechanical and derivable from ASN-0034 content already in scope.

## Issue 3: O11 sub-case (a) cross-state depth identification assumes subspace preservation under K.μ⁺ implicitly
Reason: The fix makes explicit that `subspace(v) = v₁` is a state-independent structural projection (per T4b of ASN-0034). This is a foundation-level clarification derivable from existing tumbler-projection definitions.
