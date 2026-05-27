# Channel Assignment — ASN-0099 review-28

**Date:** 2026-05-27 03:47

## Issue 1: A1's load-bearing convention should be more sharply distinguished from substrate axiom inheritance
Reason: The fix is structural/presentational — splitting A1 into a/b sub-lemmas or relabeling to surface the convention-grounded vs. frame-derived distinction can be done from existing ASN material. Both Nelson design intent and Gregory implementation evidence supporting the closed-world reading are already cited in A1's body.

## Issue 2: F4's "unique match predicate" claim conflates definitional and operational uniqueness
Reason: The framing paragraph already supplies the operational qualifier; the fix is to propagate that qualifier into F4's claim statement and the claims table entry. Purely presentational refinement of existing content.

## Issue 3: The case (ii)→case (i) lifting in F10's version-extension derivation deserves a citation handle
Reason: The lifting argument is already worked through explicitly for d_a/d_v in the F10 verification paragraph; extracting it as a named lemma (e.g., F10a) or adding explicit citations to the version-extension paragraph is a structural refactor of existing content.

## Issue 4: F2-V ∧ F3-V's derivation from F2 ∧ F3 conflates two conformance models
Reason: The ASN already notes both readings (derived for factoring implementations, independent for direct-surface implementations); the fix is to formalize this disjunction at the claim level — a presentation choice within the ASN's own conformance model, requiring no external design intent or implementation evidence.

## Issue 5: F4's "any other refinement" universal closure leans on undischarged reachability
Reason: The general argument that single-canonical-span witnesses suffice to defeat every F1-strengthening is derivable from F1's existential structure (the minimal singleton-overlap shape is universally available) and the existing K.λ realizability machinery. The fix — either strengthening the universal closure or explicitly bounding it to the enumerated witness shapes — is internally derivable.
