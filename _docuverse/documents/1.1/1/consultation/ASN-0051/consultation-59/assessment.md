# Channel Assignment — ASN-0051 review-59

**Date:** 2026-05-16 09:08

## Issue 1: SV6 sub-claim (ii)(b) — implicit case for `t ≠ s` with proper-prefix relationship
Reason: The fix is a proof case-split using T1's trichotomy already in scope (T1(i) component-wise divergence vs T1(ii) proper-prefix relationship) and T12's `actionPoint(ℓ) ≤ #s`. All required machinery is internal to the ASN's cited foundations.

## Issue 2: SV11 attainment for (m ≥ 2, p ≥ 3) marked conjectural
Reason: Resolving attainment at (m ≥ 2, p ≥ 3) requires constructing a witness (or proving non-attainment) using ASN-0058's M7/M12 block-merging discipline and ASN-0053's span algebra — purely formal machinery within the ASN's foundations. No design intent or implementation evidence is required to settle the math.

## Issue 3: SV11 attainment biconditional — disjoint-pair argument relies on undefended geometric claim
Reason: The fix is either scoping the disjoint-pair argument to p = 2 or extending it with a T-betweenness lemma using S0 convexity and ASN-0058's block-ordering properties. All machinery is internal.

## Issue 4: π versus locate terminology drift in SV10 discussion
Reason: The mismatch is between the property name chosen by the ASN author and the formal statement also authored within this ASN; resolving it is a naming/formalisation choice using the projection and resolution definitions already introduced. Internal editorial decision.

## Issue 5: SV13(e) reordering clause overloads "preserves π exactly"
Reason: The fix is to align SV13(e)'s synthesis prose with SV5's existing composite-endpoint scope note — purely an editorial qualifier drawn from material already present in the ASN.
