# Channel Assignment — ASN-0131 review-28

**Date:** 2026-06-13 19:48

## Issue 1: The retraction-type symbol `Θ` is used before it is introduced, and is reintroduced inconsistently as `R`
Reason: Purely notational/expository — move `Θ`'s definition to its first use, apply the note's own `Θ` renaming consistently in place of the `R` in the `K ≁ R` citation, and confirm the `θ`/`Θ` distinction. The note already establishes that it renames ASN-0086's retraction type to `Θ`, keeps it distinct from the retention set `R`, and uses lowercase `θ` for a separate classifying address; the fix is internal consistency, requiring no design intent or implementation evidence.

## Issue 2: The computability paragraph forward-references `addressable(Σ)` and "the answer" before they are defined
Reason: Purely an ordering fix — split the correctly-placed touch-test decidability from the premature addressability/answer-computability content and relocate the latter to after RE-DEF. All the content already exists in the note; nothing external is needed.
