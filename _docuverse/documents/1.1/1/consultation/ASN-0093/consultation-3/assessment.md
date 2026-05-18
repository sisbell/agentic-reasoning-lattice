# Channel Assignment — ASN-0093 review-3

**Date:** 2026-05-18 14:23

## Issue 1: ValidAddress predicate not tied to T4-validity
Reason: Fix is internal — the substrate needs to add an explicit identification `ValidAddress(d) ≡ T4(d)` referencing ASN-0034's T4 definition and use one term consistently. No design intent or implementation evidence required.

## Issue 2: ChainMembershipForOrigin K.σ step proof gap
Reason: Fix is internal — the explicit derivation uses C2/L1a as inductive hypotheses at Σ together with K.σ's precondition `d_new ∉ dom(M)`, all already present in the ASN. No external channels needed.

## Issue 3: "T10a chain-lemma applicability" remark imprecise on T10a.4 dependency
Reason: Fix is internal — the substitute mechanism (TA5a applied inductively from FirstEmission's T4-valid starting point in place of direct T10a.4 invocation) is derivable from ASN-0034's TA5a and FirstEmission's pinned structural form. No design intent or implementation evidence required.
