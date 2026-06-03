# Channel Assignment — ASN-0071 review-29

**Date:** 2026-06-03 07:46

## Issue 1: Depth-wise/breadth-wise discrimination stated three times, then deferred to the worked scenario
Reason: Pure editorial collapse — the PC proof already in the ASN establishes that `actionPoint(ℓ) = #u` confines `⟦σ⟧` to component `#u` and deeper, so the single replacement sentence is derivable from existing content. No design intent or implementation evidence needed.

## Issue 2: The extent/occurrence-recovery recipe is duplicated verbatim across two sections
Reason: Removing one of two verbatim restatements of a recipe already stated in the ASN; no external information required.

## Issue 3: Derivation-provenance meta-prose around the ContentReference relaxation
Reason: The PC argument already stands independently in the ASN; trimming the "cannot borrow C0a / must argue directly" framing is internal editing that leaves the self-contained proof intact.

## Issue 4: The depth-1 anchor exclusion is re-justified at each use site
Reason: The `u=[1], ℓ=[2]` exhibit is fully worked in *The query*; replacing later re-narrations with a by-name invocation of `actionPoint(ℓ) ≥ 2` is purely internal cross-reference cleanup.
