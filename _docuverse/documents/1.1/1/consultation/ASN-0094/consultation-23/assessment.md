# Channel Assignment — ASN-0094 review-23

**Date:** 2026-05-20 04:05

## Issue 1: Sh4 contract suppression of duplicate Nullify calls not addressed in Nullify Compatibility
Reason: The operational equivalence argument (suppression returns ⊥ but nullified uses L_R, preserving coverage from prior retraction) is derivable internally, but the design question of whether R should be exempt from Sh4 vs subject to suppression benefits from both design intent and implementation evidence.
Nelson question: Was retraction intended to be idempotent in the duplicate-target-Nullify sense (so a second Nullify of an already-retracted address is a no-op), or are repeated retractions of the same target intended to be distinct, recorded audit events?
Gregory question: When Nullify is called twice on the same target address `a` (with `a` already in nullified(Σ) from a prior retraction), does udanax-green suppress the second call, admit it as a distinct tuple in L_R, or reject it explicitly?

## Issue 2: Stratification documentation inaccurate about Sh4's consumed lemmas
Reason: The fix is verifiable by inspecting the Sh4 proof's actual citations against the Stratified proof order's claim — purely an internal documentation correction.

## Issue 3: Retraction shape lacks a rejection-case walkthrough
Reason: Constructing a worked Sh-conf clause (d) rejection case at Retraction's `t_G = A_rel` gate is mechanical from the ASN's existing definitions (Sh-conf, the Retraction shape, R4's disjointness).

## Issue 4: PointSlotAccessors codomain conventions vs domain symbol typing
Reason: This is a notational consistency choice between two presentations both fully specified in the ASN; the fix is editorial.

## Issue 5: "Prior" terminology in Initial-State Baseline
Reason: Pure wording fix — replace "prior" with explicit reference to `L_K^{Σ_init}`.

## Issue 6: from_K notational overload between SetSlotAccessors and catalog templates
Reason: Both definitions of from_K are already stated in the ASN; the fix is naming/cross-referencing, no external input required.
