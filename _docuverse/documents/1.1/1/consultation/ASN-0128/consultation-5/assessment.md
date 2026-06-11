# Channel Assignment — ASN-0128 review-5

**Date:** 2026-06-10 19:11

## Issue 1: I1a's step case asserts a false frame for K ~ R deposits
Reason: The fix is a proof repair fully derivable from the ASN: the case split (K ≁ R untouched frame; K ~ R may nullify, which shrinks a class) uses only the note's own machinery (R6b-style retraction-of-retraction, the shrinking observation already made for non-K deposits). No new intent or evidence is needed.

## Issue 2: DR's wp equivalence is false without the attainability convention, which this note never declares
Reason: The fix is to import a convention ASN-0126 already declares ("attainability reading in force") and supply a necessity argument per precondition using material already in DR and the wrapper contract. Both the convention and the counterexample analysis are internal to the corpus's own formalism.

## Issue 3: The extended-record `Σ_init` is used but never constructed
Reason: The fix is a definitional sentence mirroring ASN-0126's own construction — adjoin the validated extended-record registry to ASN-0086's three initial components unchanged — which is fully determined by the dependency chain the note already cites. No design intent or implementation evidence bears on it.

## Issue 4: I0's bounded-loss claim asserts a multi-step identity without derivation
Reason: The required two-direction derivation is pure order theory over `≼` and PrefixSpanCoverage, both already in the corpus; the review itself sketches both directions. Entirely internal proof work.

## Issue 5: S1 overloads the note's own technical term "active"
Reason: This is a wording fix whose semantics are already pinned by BH1's rewrite scope and the note's own example paragraph; the review supplies a workable replacement. No external consultation needed.
