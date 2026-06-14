# Channel Assignment — ASN-0133 review-16

**Date:** 2026-06-13 17:41

## Issue 1: "Heterogeneous-view ⟹ not one PL term" ignores the cross-view rebuild the note's own foundation provides
Reason: The fix turns entirely on whether ASN-0129's fixed-view-base rewrite machinery (PC3, the `A_K`/`L_K` rebuilds, the rule that verdict/Boolean atoms are never UV-rewritten) can unify any view-parameterized Boolean trigger onto one term-view. That is a formal question about a cited substrate foundation — resolvable by working through ASN-0129's rewrite rules to either exhibit a non-unifiable Boolean read or retract — and no Xanadu design intent or udanax-green evidence bears on it.

## Issue 2: Fire atomicity is smuggled into the σ model, against the note's stated discipline
Reason: Whether ASN-0128's I4 serializes individual `→_sh` steps versus contiguous runs is fixed by that cited semantics, and the note's own worked example establishes that the load-bearing Q5a/Q6 marker fires emit one tuple (hence are single-step, atomic by I4); naming the assumption or restricting to single-step fires is an internal authorial move over existing content.

## Issue 3: The fixed `addr` projection cannot express the "per-target" tier the note advertises for tuple-domained rules
Reason: Whether `addr`-projection realizes per-target scoping for a tuple rule, and whether to generalize `π_ρ` to a rule-chosen projection (`coverage_G`/`coverage_F`), are formal facts about the note's own scope machinery plus the Binary-homing it inherits (ASN-0086/0128); the canonical tiers are this layer's application vocabulary, outside Xanadu design intent and udanax-green's implementation.

## Issue 4: No concrete fire-sequence trace exercises Q0 and Q6's reaching-claim
Reason: The trace exercises only the note's own constructs — the `cmt`/`res` triggers, the extinction fires, and evaluating the nested-quantifier `quiescent_R` at the terminal state — all fully specified by definitions already present, so it is constructed internally with no external channel.
