# Channel Assignment — ASN-0134 review-6

**Date:** 2026-06-13 20:02

## Issue 1: A6's "per-state invariant package" includes invariants that are not per-state
Reason: Internal fix — a formal-typing correction. The quantifier structure of each invariant (`C0`/`L12` over transitions `Σ → Σ'`; `SD`/`C1c`/`L1c`/`P6`/`P1`/`P2`/`R1`/`R2` per-state) is settled in ASN-0093/0126/0128 and already cited, and A6's own proof uses the correct quantifiers — so the *statement* need only be split to match its proof. No design intent or implementation evidence is in question.

## Issue 2: the BH4-age observability witness for the first non-confluence contradicts BH4's `idem = ⊥` requirement
Reason: Internal fix — a formal incompatibility already settled in the dependency. ASN-0128's BH4 ("any shape, with `idem = ⊥`") and R-C0 (age-staleness requires `idem = ⊥`) are quoted in the review and forbid the witness on an `idem = ⊤` type; deleting it (the `Observe_K` witness already suffices) or rephrasing to the frontier-shift effect on co-homed `idem=⊥` tuples follows from ASN-0128's definition plus this note's own H0. Neither channel needed.

## Issue 3: V2's "Q-affecting step" and the decomposition of `Q` are left undefined
Reason: Internal fix — the realization model is forced by the operation surface already committed (per-type `Observe_K` is the sole read primitive, ASN-0086/0128), so any cross-type or per-home `Q` must factor through the `p` reads; the fix is to state this abstractly as `Q = g(Observe_{K_1}, …, Observe_{K_p})` and define a `Q`-affecting step as one changing some `Observe_{K_i}` value. This is a generalization away from the over-specialized "conjunct," not a question of what form quiescence takes in the design — §8 already carries Nelson's quiescence intent.

## Issue 4: §8's read-count dichotomy overstates the "otherwise" horn
Reason: Internal fix — a pure counting correction (distinct observed states number between 2 and `p`, not `p`), derivable directly from the structure of zero-step reads sitting at non-decreasing indices already established in the note.
