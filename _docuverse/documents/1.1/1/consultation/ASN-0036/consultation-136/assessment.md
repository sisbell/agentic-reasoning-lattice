# Channel Assignment — ASN-0036 review-136

**Date:** 2026-05-29 00:14

## Issue 1: Triple-repeated maximal-run disclaimer in the worked example
Reason: Purely editorial deduplication — the singleton-vs-maximal distinction already lives in S8's postcondition and Open Questions; removing the repeated gloss requires no design intent or implementation evidence.

## Issue 2: S5 cross-document construction over-justifies witness validity, contradicting its own frame
Reason: Internal proof hygiene — S5's own frame disclaims later-invariant validity, and the needed distinctness argument (distinct last components ⇒ T3) is already present; trimming the unused T4/NAT-closure justification is derivable from the ASN alone.

## Issue 3: S7b depends on S0 with a cross-transition persistence rationale it does not need
Reason: Internal consistency fix — S7b is a per-state axiom, so the cross-transition S0 rationale is self-evidently superfluous from S7b's own statement; no external channel needed.

## Issue 4: S8-depth inline notation is ambiguous
Reason: Pure notation fix — renaming bound variables or using the unambiguous `subspace(·)` already adopted in the formal contract; derivable from the ASN alone.
