# Channel Assignment — ASN-0047 review-320

**Date:** 2026-06-02 03:02

## Issue 1: Imprecise foundation citation for `origin`
Reason: The fix is a citation correction internal to the foundation reference — the reviewer already supplies the correct anchor (ASN-0036 S7 defines `origin`, S7a is the allocation axiom), so it is derivable by cross-checking ASN-0036's own structure without design intent or implementation evidence.

## Issue 2: Node-nesting claim duplicated across NodeRootedForest and CrossNodeAccountBase
Reason: Pure deduplication — removing the redundant nesting example from NodeRootedForest requires no external input, only the ASN's own structure since CrossNodeAccountBase already houses the load-bearing analysis.

## Issue 3: Defensive meta-prose in FrontierEquivalence "Freshness discharge" note
Reason: Editorial trim of redundant justification prose; the operative per-`k` content is retained and the change is fully derivable from the ASN's existing text.
