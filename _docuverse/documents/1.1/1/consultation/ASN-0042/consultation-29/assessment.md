# Channel Assignment — ASN-0042 review-29

**Date:** 2026-05-14 00:35

## Issue 1: FirstDelegatorIsπ inductive step has a gap when π already has sub-delegates in Π_Σ
Reason: This is a proof-structural gap that requires either restricting the sub-lemma's hypothesis to states with empty S_π(Σ) or rewording the chain-conclusion clause to permit pre-Σ delegation links. Both repairs are internal logical operations on the existing proof; no design intent or implementation evidence is needed.

## Issue 2: AccountField decidability is misattributed to T6
Reason: Pure citation correction within the foundation reference set. The reviewer has already identified T4(b) (UniqueParse) as the correct decidability witness; the fix is replacing the T6 citation with T4(b), derivable from the foundation work already present in ASN-0034.

## Issue 3: O7 Postcondition (c) overstates recursive delegation as unconditional
Reason: Contract wording precision issue. The conditionality is already present in condition (ii) of the existing `delegated` relation in this ASN; the fix is making that conditionality explicit in the postcondition language, fully derivable from the ASN's own content.

## Issue 4: Several "By T4" citations conflate distinct sub-claims of the foundation
Reason: Foundation cross-reference precision. The reviewer specifies the target sub-claims (T4(b), T4a, T4(c)); the fix is replacing bare "By T4" with the specific sub-claim at each citation site, derivable from ASN-0034's already-formalized structure without external input.
