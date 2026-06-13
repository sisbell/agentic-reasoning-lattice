# Channel Assignment — ASN-0133 review-5

**Date:** 2026-06-13 11:33

## Issue 1: Q5a drops extinction discipline — its bound is false for an all-SF-but-non-falsifying registry
Reason: Internal. The note's own Q-EXT explicitly carries two antecedents (SF spelling *and* extinction discipline), and Q3 itself names the weak contract `Post_ρ ≡ ⊤` that breaks the bound; Q5a simply must re-state the hypothesis it already depends on. No design intent or implementation fact is in question — the claim is false as written about the note's own abstract rule model.

## Issue 2: the worked example's stratification repair is vacuous for the SF producer, and so fails to exclude the very divergence it diagnoses
Reason: Internal. The note already establishes `T_P` is SF (class check), that SF triggers are re-arm-immune (Q-FLIP: "⊥-stability makes a falsified SF trigger permanent… deposits included"), and that the diagnosed divergence is domain growth, not re-arming (Q5a). Replacing "re-arm" with "enlarge the producer's domain" is forced by the note's own vocabulary.

## Issue 3: H-W is listed as a route to H-RF, but the note's own starvation argument proves H-W unsatisfiable for any working registry
Reason: Internal. The diagnosis is the note's own starvation observation ("an unfair scheduler… drives `|W(σ)| = ∞` whatever the registry's structure") applied to H-W's "every σ" quantifier; H-W, W, H-RF are constructs of this note, not features of Nelson's design or the udanax-green code. The fix is an authorial choice between redefining H-W over fair σ or demoting it to a foil — both resolvable from the note's existing reasoning.
