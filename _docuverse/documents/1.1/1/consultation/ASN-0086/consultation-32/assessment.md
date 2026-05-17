# Channel Assignment — ASN-0086 review-32

**Date:** 2026-05-17 05:51

## Issue 1: "Uniform argument" for ASN-0036/0034 invariants is invoked twice without being a named lemma
Reason: The fix is purely structural refactoring — lifting an already-derived prose argument into a named lemma and citing it at both sites. No design intent or implementation evidence is needed; the lemma's content is already discharged in the ASN.

## Issue 2: Definition of nullified silently encodes a directional convention that L7 disclaims
Reason: The fix is labeling a convention already implicit in the Definition (G' is consulted, not F') and in Nullify's argument shape. L7 already places directional interpretation under "link type defines directionality," so this note is free to declare its own convention for the R type it introduces — no external channel needed to add the label.

## Issue 3: A_K's non-monotonicity is never stated explicitly
Reason: The non-monotonicity is a direct consequence of R3 (L_K monotone) combined with R6's set-difference Definition and the shrinkage already exhibited in Worked Sketch Step 1. The consequence is derivable from the ASN's own content.

## Issue 4: R6c-Corollary Step 5.2 in the Worked Sketch lifts to ⊑̂ via an abstract transition
Reason: The fix is tightening a disclaimer to make the asymmetry between concrete dom-extending steps and the abstractly-justified arrangement-modifying step explicit. The justification (R6c-Corollary depends only on the frame) is already present in the ASN.

## Issue 5: Substrate primitive permits broader addresses than R0 Step 2 produces
Reason: The clarifying sentence to add at Emit_K's Definition restates content already present in the "Breadth of the primitive vs. the discipline R0a names" paragraph and in the Hypothesis dependency table — purely a surfacing fix internal to the ASN.
