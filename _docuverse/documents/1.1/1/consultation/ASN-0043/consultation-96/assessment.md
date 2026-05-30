# Channel Assignment — ASN-0043 review-96

**Date:** 2026-05-30 12:43

## Issue 1: FSP's producibility hypothesis is weaker than the L1c contract it claims to discharge
Reason: Internal — the gap is closed by the ASN's own formal machinery: L1c's chain form, TA5(c)'s length-preservation of `inc(·,0)`, and the fact that moving `zeros` from 2 to 3 forces the first operative step to be the `k'=2` separator-seating descent. The "seed = home(a)" constraint forbidding a document-level sibling step is derivable from definitions already present.

## Issue 2: The "L3 non-emptiness binds slot 3 only" fact is restated three times
Reason: Internal — pure editorial deduplication of a structural fact about L3 already stated in the ASN; no design intent or implementation evidence is at issue.

## Issue 3: L1b is asserted without grounding or derivation, yet is load-bearing
Reason: Gregory is needed to supply the same kind of implementation grounding that L0/L1/L1a carry — confirming that link addresses are allocated with an element field of depth ≥ 2 (subspace identifier plus a within-subspace ordinal), which is what justifies depth 2 over depth 1.
Gregory question: When `findisatoinsertmolecule` allocates a link address under the `LINKATOM` hint, does the resulting element field carry both a fixed link-subspace component and a separate within-subspace ordinal — i.e., is the element-field depth always at least 2?
