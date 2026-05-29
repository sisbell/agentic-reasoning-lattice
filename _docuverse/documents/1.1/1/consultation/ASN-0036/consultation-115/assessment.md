# Channel Assignment — ASN-0036 review-115

**Date:** 2026-05-28 20:37

## Issue 1: `δ` overloaded against foundation notation
Reason: Pure notation collision fix — rename the element-field-depth scalar and reserve `δ(·,·)` for the foundation's ordinal displacement. Derivable from the ASN alone; no design intent or implementation evidence needed.

## Issue 2: `w_ord` cites the wrong (and omits the right) dependency
Reason: The postcondition `actionPoint(w_ord) = actionPoint(w) − 1` follows from `ActionPoint`'s own definition applied to the index-shifted sequence; correcting the Depends citation is internal bookkeeping against ASN-0034's contracts.

## Issue 3: S9 is S0 restated; its proof says so
Reason: Editorial collapse of redundant prose into a one-line named corollary of S0. The directional reading is already present in the ASN; no channel needed.

## Issue 4: Protocol rationale embedded in the S3 axiom slot
Reason: Moving the quiescence rationale out of the axiom slot and consolidating with the existing Open Question is internal restructuring — the content and its single destination already exist in the ASN.

## Issue 5: Repeated boilerplate Depends clause
Reason: De-duplicating six identical S0 justification clauses is purely editorial; the S0-fixes-components consequence is already stated and need only be cited once.

## Issue 6: State-component "proofs" are modeling rationale ending in ∎
Reason: Dropping the ∎ and "we justify the modelling choice" framing on definitional paragraphs is internal editorial cleanup — nothing is derived, so no design or implementation input is required.
