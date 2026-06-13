# Channel Assignment — ASN-0130 review-18

**Date:** 2026-06-13 02:37

## Issue 1: wp derivation justified by contrast with a discarded draft
Reason: Internal fix. The positive rationale the review wants is already in the ASN — "POST-ref being a state predicate over Σ' that a *standing* tuple can satisfy ... so a rejecting call (a skip, Σ' = Σ) inherits whatever registration stood." Removing the "unlifted form" meta-commentary and stating the standing-tuple rationale directly draws only on the wp derivation already present; no design intent or implementation evidence is at issue.

## Issue 2: non-load-bearing historical excursion embedded in a normative claim
Reason: Internal fix. The action is purely subtractive — delete the udanax-green excursion the author already declares "not load-bearing." The surviving claim rests on PC3 (ASN-0129, already cited), and the suggested one-liner ("scope is the reader's, fixed per evaluation") restates PR-VIEW's own PC3 reasoning. We are removing the evidence-channel detail, not verifying or expanding it, so Gregory is not needed.

## Issue 3: PS2 re-characterizes ST⁺ already defined in PR5
Reason: Internal fix. Pure de-duplication — the sound-superset / k=0-coincidence characterization lives in PR5; reducing PS2 to "Asserts ST⁺ certification (PR5) of the view-independent expansion at `a`" and cross-referencing PR5 is a structural edit within the ASN's own content. No external channel required.
