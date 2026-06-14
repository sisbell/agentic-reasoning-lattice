# Channel Assignment — ASN-0134 review-4

**Date:** 2026-06-13 19:11

## Issue 1: V2 asserts equivalence among three soundness conditions of different strength
Reason: Internal — the note's own §8 supplies every term needed: it already states "the index moves only when a writer step linearizes" and treats "Q-affecting" as strictly narrower than "writer step," which is exactly the counterexample (a non-`Q`-affecting writer step between reads). Restructuring the `iff` into the implication chain [one index] ⟹ [no `Q`-affecting step between] ⟹ [sound] is a pure logic correction from material already present; no design intent or implementation evidence bears on it.

## Issue 2: A6's canonicity argument misdescribes how the foundation invariants are quantified
Reason: Internal — the fix is a formalization-citation correction within the already-cited dependency stack, routing through transfer lemmas (ASN-0128's `RP-a`, ASN-0126's `B2` composed with ASN-0086's inheritance of ASN-0093) that the reviewer has already named. How the foundation invariants are quantified and how they project onto `𝔼`'s extended-record states is a matter of the dependency ASNs' content, not of Nelson's design intent or Gregory's implementation.

## Issue 3: The minimality claim contradicts its own clause-6 parenthetical
Reason: Internal — this is a self-contradiction within §9 ("removing any clause admits a counterexample" vs. "drop 6 is vacuous"), reconcilable using only the note's own `W6`/`R1` reasoning by either dropping clause 6 or rephrasing the minimality claim. No external channel is implicated.
