# Channel Assignment — ASN-0053 review-36

**Date:** 2026-05-28 20:12

## Issue 1: Exhaustiveness preamble in SC is meta-prose about clause phrasing
Reason: Pure editorial deletion of meta-prose about clause wording; the constructive WLOG comparison that remains is self-contained within the ASN. No design intent or implementation evidence bears on whether the preamble stays.

## Issue 2: "Denotation, not encoding" is a standalone disclaimer that establishes no property
Reason: Removing a scope disclaimer (or folding it into Open Questions) is an internal structural decision; the T3 reference and denotation framing are already established within this ASN and ASN-0034.

## Issue 3: S6 flat-address-space parenthetical is essay content
Reason: Deleting a hypothetical-world aside while keeping the concrete `[1,3,0,1]` divergence example is purely internal; the example already demonstrates what level_compat excludes.

## Issue 4: Nelson "no choice as to what lies between" quoted redundantly
Reason: De-duplicating an LM 4/25 quote already present in two places is an internal editorial choice about citation placement; no new evidence from Nelson is required to decide which instance to keep.

## Issue 5: "Properties Introduced" table omits load-bearing cited foundation deps
Reason: D2 and TA-assoc are already cited and used in the proofs (WR, S4a, S5, S9, S11); adding their rows is a bookkeeping fix derivable from the ASN's own dependency usage and ASN-0034 labels.
