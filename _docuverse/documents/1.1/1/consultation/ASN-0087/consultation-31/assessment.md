# Channel Assignment — ASN-0087 review-31

**Date:** 2026-06-03 22:53

## Issue 1: The v_ℓ freshness argument is given twice
Reason: Purely structural de-duplication — consolidate the two-part freshness argument into S2 and reduce the freshness section to a cite. No design intent or implementation evidence needed; the argument is already fully present in the ASN.

## Issue 2: "Transfers verbatim" meta-prose narrating non-derivation, repeated
Reason: The fix replaces meta-narration with bare cites to named ASN-0093 lemmas already referenced in the ASN. Internal editorial change; the cited lemmas are identified within the text.

## Issue 3: M-DepthConv carries rationale prose about a sibling primitive
Reason: Dropping a trailing justification clause and restating the commitment — purely a prose trim. The convention's content is fully specified in the ASN.

## Issue 4: Defensive "not over dom(C)" prose on S7d
Reason: Reduces a relocated-correction clause to a one-line inheritance statement; the dom(M)-unchanged fact is already established in the ASN. Internal edit.

## Issue 5: Repetitive frame-inheritance justification across many invariants
Reason: Grouping a dozen identically-justified conjuncts into one statement, preserving all names. Pure consolidation, fully derivable from the existing frame facts in the ASN.
