# Channel Assignment — ASN-0126 review-14

**Date:** 2026-06-08 23:51

## Issue 1: P6 deposits at "some fresh key," not the named `a_emit(Σ, d)`
Reason: The fix turns on how ASN-0086 itself defines `Emit_K` (which binds `a = a_emit`) versus the bare `K.λ` transition (any fresh key) — all in the foundation ASN-0086 already available to the note. No design-intent or implementation evidence is needed; it is a proof-structure repair using inherited definitions.

## Issue 2: Non-emptiness shown for the representative `K_j`, not the emitted `K`
Reason: A one-line coverage-equality argument (`K` registered ⇒ `coverage(K) = coverage(K_j) ≠ ∅ ⇒ K ≠ ∅`) drawn entirely from the note's own registration definition and `Endset`/span properties. Fully internal.

## Issue 3: Cross-ASN reference to a non-foundation ASN
Reason: Editorial self-containment fix — drop the ASN-0036 citation, retaining the foundation-ASN L-fin parallel. The reviewer confirms it is a non-load-bearing analogy; no channel input required.
