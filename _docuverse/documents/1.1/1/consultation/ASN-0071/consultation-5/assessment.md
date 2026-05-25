# Channel Assignment — ASN-0071 review-5

**Date:** 2026-05-25 12:51

## Issue 1: Symbol `v_A` overloaded in worked example
Reason: Pure notational disambiguation — rename the content value to avoid clashing with the V-position symbol. Fix is internal to the ASN; no design intent or implementation evidence required.

## Issue 2: "By trichotomy" — which trichotomy?
Reason: Citation precision fix — the correct axiom (NAT-order trichotomy on ℕ) is already identified by the reviewer and the proof structure is in place. Fix is derivable from the ASN's own foundation citations.

## Issue 3: `iaddrs` codomain notation hides state dependence
Reason: Notational fix to make state-dependence of `dom(C)` explicit, matching the prose's treatment of other state-dependent operators. Fix is internal; no external input needed.

## Issue 4: F-FIN's appeal to "the sequential-transition discipline" is too loose
Reason: Citation correction — the reviewer has already identified the correct axiom (ExtendedReachableStateInvariants in ASN-0047) that supplies finite ancestry. Fix is derivable from the existing foundation without further consultation.
