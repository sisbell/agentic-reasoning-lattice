# Channel Assignment — ASN-0111 review-46

**Date:** 2026-06-11 00:36

## Issue 1: RL4's "function of (a, Σ.L(a)) alone" gloss outruns its formal statement, and the claims table drops the precondition
Reason: The missing both-absent congruence is immediate from the definition's else-branch (`readlink(a, Σ) = ⊥` when `a ∉ dom(Σ.L)`), and the claims-table fix is a mechanical restoration of the body's precondition. No design intent or implementation evidence bears on it.

## Issue 2: Justificatory parenthetical inside the 𝒮 definition; reachability restriction stated three times
Reason: Purely editorial — the fix deletes redundant justification and collapses three statements of the standing precondition to one pointer, all of which the ASN already contains. Internal.

## Issue 3: Composite-validity discharge duplicated verbatim plus a forward use-site pointer
Reason: The fix is structural: name the existing one-sentence discharge as a micro-lemma and cite it at the three use sites. The argument itself is already present and correct in the ASN; no external consultation needed.
