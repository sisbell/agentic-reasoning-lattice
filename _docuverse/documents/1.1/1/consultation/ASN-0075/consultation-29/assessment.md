# Channel Assignment — ASN-0075 review-29

**Date:** 2026-06-03 00:40

## Issue 1: D-IDENT "Link survival" overstates where link spans anchor
Reason: The fix is a notational/scoping correction: drop the false universal and qualify to spans actually anchored at the content address `a`. The reviewer already supplies the relevant Shared Vocabulary fact (spans may anchor at link addresses), so the correction is derivable from the ASN's own content and foundation citations.

## Issue 2: Foundation predicate `Element` renamed to `IsElement`
Reason: Pure notation alignment with the foundation (ASN-0047 defines `Element(·)`); the fix is to use the foundation's name or cite `T_elem` directly. Fully derivable from existing content.
