# Channel Assignment — ASN-0082 review-32

**Date:** 2026-05-15 11:51

## Issue 1: PositiveOffsetExceeds derivation invokes commutativity not present in the foundation
Reason: Pure formalization issue internal to the ASN — concerns whether a derivation step is sound against ASN-0034's NAT-* axioms. The reviewer has already supplied the foundation-derivable replacement chain (NAT-addbound right-dominance + NAT-cancel mirror form + NAT-order). No design intent or implementation evidence bears on whether commutativity is derivable from the cited axioms; this is verified by inspecting ASN-0034 directly.
