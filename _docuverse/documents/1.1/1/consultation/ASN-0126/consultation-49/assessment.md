# Channel Assignment — ASN-0126 review-49

**Date:** 2026-06-09 11:52

## Issue 1: Essay content in "App-side obligations"
Reason: Pure deletion plus relocation of the "app registers R" obligation, which is already stated in the note (precondition (i) of `K.λ_sh`, and the R-registration is introduced in the retraction paragraph). No design intent or implementation evidence is at stake — the fix is internal editing.

## Issue 2: "Why the precondition is needed" prose around arity-3
Reason: The retained one-sentence claim (that (0) forces arity 3 so `{e₁,e₂}` is content-exhaustive) is already present; cutting the counterfactual and e₄ excursus removes justification prose without altering any technical claim. Derivable from the ASN alone.

## Issue 3: Philosophical closer in Registry permanence
Reason: Pure deletion of interpretive prose; P1 already establishes the invariance formally. No external input needed.

## Issue 4: Span-count-vs-coverage explained twice, plus app-responsibility prose
Reason: Consolidation of a point stated twice and reduction of responsibility framing; the genuine technical fact (span-count is coverage-variant) is already in the note. The coverage/span-count distinction rests on ASN-0043's `Endset`/`PrefixSpanCoverage` definitions already cited — internal.

## Issue 5: Multiple deferrals to the same downstream proof
Reason: The discharge `coverage(K) = coverage(K_j) ≠ ∅ ⟹ K ∈ T_admissible` is already fully written in P5's proof; the fix just inlines that single line at first use and drops the forward pointer. Entirely derivable from the note's own content.
