# Channel Assignment — ASN-0093 review-15

**Date:** 2026-05-18 21:34

## Issue 1: FirstEmissionFreshness's link case left as "symmetric"
Reason: Purely a proof-presentation gap. The content case is fully stated; the link case requires only the C↔L substitution with the named lemma swaps (dom(L)↔dom(C), SC-NEQ direction reversed). Derivable from the ASN's existing content.

## Issue 2: ChainPrefixExtension's inductive step for link case
Reason: Same shape as Issue 1 — the content case's step uses ChainUniformLength, ChainElementT4Validity, TA5-SigValid, TA5(b)/(c) on `b_C(d)`; the link case substitutes `b_L(d)` and `A_L(d)` using the same lemmas. Internal fix.

## Issue 3: DisjointSubAllocatorChains' implicit induction
Reason: The required structuring is mechanical — FirstEmission supplies the base; TA5-SigValid + TA5(b) at `k = 0` supplies the step preserving position `#d + 2`. All cited lemmas already appear in the ASN. Internal fix.

## Issue 4: Sub-case B.i with strict inequality not exercised in worked example
Reason: The worked-example pattern is established (Steps 5 and 9 verify other sub-cases); adding a fourth document with prefix-incomparable structure and `#d_1 < #d_2` (e.g., `d_alt' = [3, 0, 7]` with `#d_alt' = 3 < 5 = #d`) follows the same exhibition format. Derivable from the lemma proof and existing worked-example pattern.

## Issue 5: Frame quantifier range underspecified
Reason: Pure notational fix. The intended semantics is already clarified parenthetically below the frame clause; folding `M' = M` (or `d' ∈ dom(M)`) into the clause itself is editorial. Internal fix.

## Issue 6: SubAllocatorAxiom.Exists's "permanence" argument relies on circular-feeling discharge
Reason: The simultaneous-induction framing is already stated in the discharge section; the fix is to align the SubAllocatorAxiom.Exists prose to refer to that framing explicitly rather than treating permanence as a post-hoc corollary requiring M1 in scope. Derivable from the ASN's own framing.
