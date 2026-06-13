# Channel Assignment — ASN-0133 review-1

**Date:** 2026-06-13 10:30

## Issue 1: Extinction discipline does no deductive work in Q5/Q6, and the hypothesis-independence claim is false
Reason: Pure proof-correctness issue internal to the note — the definitions of `W(σ)`, H-W, extinction discipline, Q-EXT, and Q5a are all present, and the fix (attribute Q5's injectivity to the step index, restate Q5/Q6 under H-W alone, relocate extinction's role to Q-EXT/Q5a, repair the independence paragraph) is derivable by formal reasoning over the note's own content. No design intent or implementation evidence is at stake.

## Issue 2: The worked composition mis-classifies the producer trigger as an SF spelling
Reason: The class assignment is governed entirely by ASN-0129's PD0 quantifier/Boolean rules (a cited dependency), and the cleanest fix — moving `needs_attention(t)` into the QD domain so `T_P` becomes a genuine negated existential — is a structural correction to the note's own illustration. `needs_attention` is an abstract environment predicate in the worked example, not a Xanadu operation, so neither Nelson's intent nor Gregory's code bears on it.

## Issue 3: Q0's "quiescent_R ∈ PL" under-justifies the outer quantifier and ignores view heterogeneity
Reason: Entirely a question of PL-membership precision under ASN-0129's composition machinery (V-IDX static-expansion precedent, PC0/PC1/PC3) — all cited dependencies. The fix (recast the outer `∀ ρ ∈ R` as a finite static-expansion conjunction, restrict "∈ PL" to single-view registries or downgrade to "finite conjunction of PL predicates", propagate to Q7) is internal formal work requiring no external channel.
