# Channel Assignment — ASN-0128 review-34

**Date:** 2026-06-11 09:40

## Issue 1: retract_stale establishes per-constituent admission but never states the batch's net postcondition
Reason: The fix is internal — the review itself notes the postcondition is derivable from material already on the page: the miss branch's enforced P-tgt nullification (S3), the hit branch's Nullification bullet via R6b, and R6a persistence, all of which the ASN already cites and applies.

## Issue 2: frontier-landing, a step-quantified claim, is cited under RP-a's single-state transfer
Reason: The fix is internal — it is proof-routing bookkeeping within the ASN's own transfer machinery (RP-a vs RP(ii)/RP-b), and the note already demonstrates the correct routing pattern in the same sentence for RangeSterilization. No design-intent or implementation question is at stake.

## Issue 3: "does not even type-check" misstates why the inherited postcondition fails on a hit
Reason: The fix is internal — the accurate justification (the inherited postcondition is generally false on a hit because the stored decomposition need not be the presented one) follows directly from the ASN's own hit-branch description and the dependency facts it already cites; only the erroneous sentence needs rewording.

## Issue 4: the operation-set taxonomy misses `retract_stale`
Reason: The fix is internal — BH4's own text already states that `retract_stale` is a sequence of `Nullify_Binary` steps, so the operation-set paragraph just needs to restate that classification (behavior-provided write tooling reducing to the existing primitive, no fourth primitive).

## Issue 5: SD defines a quantifier-phrase the note never uses
Reason: The fix is internal — it is a dead-setup deletion (or adoption at use sites) decidable entirely by inspecting the ASN's own text; no external evidence or design intent bears on it.
