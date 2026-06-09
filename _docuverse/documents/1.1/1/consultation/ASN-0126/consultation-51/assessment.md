# Channel Assignment — ASN-0126 review-51

**Date:** 2026-06-09 12:43

## Issue 1: `π(Σ_init) = Σ_init^{0086}` stated twice, with mutual cross-reference
Reason: Pure structural fix — consolidating a duplicated equation to a single statement in Registry permanence (where `Σ_init` is defined) and replacing the other with a citation. The construction and equation are already present in the ASN; no design intent or implementation evidence bears on where they are stated.

## Issue 2: R5(c) cited as a redundant second exclusion witness
Reason: The required action is a deletion, and the review's own argument shows it is internally derivable — `|F| = 1` excludes every empty-from emit, and the `Emit_K`-totality witness already establishes non-vacuity, so R5(c) is a logically redundant second illustration. Dropping it needs nothing from Nelson or Gregory.

## Issue 3: Defensive and redundant prose
Reason: Both edits are prose-only — cutting a defensive clause and collapsing two sentences whose shared mechanics (gate → audit slice; inherited conjuncts → active subset) are already established in the note. The narrowing to the third conjunct is content the ASN already contains, so the fix is internal.
