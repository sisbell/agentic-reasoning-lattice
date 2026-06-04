# Channel Assignment — ASN-0087 review-36

**Date:** 2026-06-03 23:29

## Issue 1: Atomicity section restates "allocated but unplaced" three times
Reason: Pure deduplication of a fact already established within the section; no design intent or implementation evidence is required to delete two restatements.

## Issue 2: M-DepthConv introduced with why-needed justification rather than content
Reason: The normative commitment (`m = 2`, then S8-depth pins `m_L(d) = 2`) is already present in the ASN; trimming the necessity rationale is an internal editorial fix.

## Issue 3: "Discoverability Is Symmetric" restates the close of "What Is Indexed?"
Reason: Folding the "no privileged home document" emphasis into existing text and deleting the redundant section is derivable from the ASN's own content and M-DiscSymmetry claim.
