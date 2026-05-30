# Channel Assignment — ASN-0043 review-85

**Date:** 2026-05-30 10:09

## Issue 1: L9 formal statement is trivially satisfied and does not capture ghost-permission
Reason: The fix replaces the vacuous subset-on-coverage-cone condition with the start-address claim `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`, which the witness already establishes. Purely a formal-statement correction internal to the ASN — no design intent or implementation evidence is needed.

## Issue 2: L1c chain prose restates clauses already in the formula
Reason: Deleting prose that re-narrates conjuncts already present in the Chain formula is a self-contained editorial trim; the retained gloss is internal to the proof.

## Issue 3: L9 witness defers its core construction downstream, forcing a forward jump
Reason: Reordering so the Case A/Case B construction of `a` appears at first use (or inverting FSP before the L9 conclusion) is structural reorganization of existing proof content — fully internal.

## Issue 4: FSP application carries a use-site inventory of invariants
Reason: Dropping the bookkeeping roster of which labels are state-independent is editorial; the type column already marks META/LEMMA. No external input required.

## Issue 5: Worked-example factoring paragraph is essay content about proof organization
Reason: Collapsing the organizational essay into one sentence is purely editorial; the substantive checks already exist in each step.

## Issue 6: Forward references to L3 in the type-accessor definition
Reason: Moving the `.type` abbreviation to after L3 (or marking it conditional) is a local reordering resolvable from the ASN's own structure.
