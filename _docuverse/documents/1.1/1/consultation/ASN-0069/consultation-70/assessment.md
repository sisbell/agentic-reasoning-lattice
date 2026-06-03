# Channel Assignment — ASN-0069 review-70

**Date:** 2026-06-02 23:24

## Issue 1: Composite verification re-derives freshness that foundation lemmas supply directly
Reason: Internal. The review names the two foundation lemmas (ChildSpawnFreshness, FrontierEquivalence) and their statements; the fix is to replace the (i)–(iii) re-derivations with one-line citations connecting each lemma to the sub-case predicate already stated in the ASN. No design-intent or implementation evidence is required — only restructuring against foundation results the review has identified.

## Issue 2: "Correspondence triple" notation overloads the S8/S8★ run structure
Reason: Internal. The fix is a rename — the object is a cross-document V-position alignment `(v_src, v_new, length)`, distinct from S8's I-address-keyed run, and the ASN already supplies all the structure needed to relabel it without consulting design intent or the implementation.
