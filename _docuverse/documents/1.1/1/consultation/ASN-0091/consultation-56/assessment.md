# Channel Assignment — ASN-0091 review-56

**Date:** 2026-06-04 00:15

## Issue 1: Premise-avoidance commentary ("which route we did *not* take")
Reason: Pure prose-hygiene deletion — the positive facts (`π(v) ∈ dom(Σ'.M(d))` from the codomain; clause (iv) from the construction) stand on their own and are already present in the ASN. No design or implementation evidence is needed to drop the "not via" contrast clauses.

## Issue 2: Collapse-case thread is over-elaborated and repeatedly deferred
Reason: The case split, its triviality payload, and all four back-references are entirely contained in the ASN; consolidating them to one statement is an internal editorial restructuring requiring neither design intent nor implementation evidence.

## Issue 3: Stage scaffolding and exhaustiveness framing inside RE-subpres
Reason: The binary constraint, two exclusions, and combination are all present and correct in the proof; removing the stage-labelling narration and folding the conclusion is purely internal to the ASN's own argument.

## Issue 4: Post-definition re-narration of the Vstream-only class
Reason: The clause-by-clause re-narration restates the definition box that immediately precedes it, and the bijection-non-uniqueness sentence to keep is already in the paragraph; the cut is derivable from the ASN alone.
