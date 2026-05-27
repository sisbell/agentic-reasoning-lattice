# Channel Assignment — ASN-0100 review-3

**Date:** 2026-05-27 12:57

## Issue 1: Substrate model conflation (K.σ vs K.δ)
Reason: Resolvable by reading the actual substrate definitions in ASN-0047 and ASN-0093 — the fix is internal consistency cleanup, not a question of design intent or implementation evidence.

## Issue 2: K.μ⁻ omission case (i.b) argument elides a step
Reason: Pure expository fix — spell out the forced equality n'_{s_C} = 0 from n_{s_C} = 0. The reasoning is already implicit; no external evidence needed.

## Issue 3: Intermediate state invariant verification incomplete
Reason: S8-depth and S8a are defined in cited ASNs (0036) and verification proceeds mechanically from the post-step shape of each intermediate. Internal fix.

## Issue 4: Cross-chain disjointness in freshness argument is implicit
Reason: L14 / DisjointSubAllocatorChains / SC-NEQ are already established in cited ASNs (0036, 0093); the fix is to add the missing citation when discharging the dom(L) half of K.α's precondition. Internal fix.

## Issue 5: I3 preconditions not explicitly discharged
Reason: All four I3 preconditions follow mechanically from INSERT's own stated preconditions plus S8-depth (already cited from ASN-0036). Internal discharge.

## Issue 6: Alternative decomposition Σ' uniqueness asserted without proof
Reason: Uniqueness of Σ' under varied decompositions follows from the structural form of the post-state contract (INS.C, INS.M-*, INS.R) — they fix Σ' uniquely independent of the path taken. Internal verification.

## Issue 7: Composite-level atomicity not adequately distinguished from per-step atomicity
Reason: This is a design-intent question — whether the original Xanadu specification required INSERT to provide composite-atomicity against concurrent operations on the same document, or whether interleaving was always treated as an implementation concern. Nelson clarifies the intended contract; Gregory shows what udanax-green actually guarantees, which informs whether the abstract spec should constrain or admit interleaving.
Nelson question: Did the Xanadu design intend INSERT to provide composite-level atomicity (no other operation's elementary transitions interleave between INSERT's allocation, arrangement, and provenance steps for the same document), or was concurrent-INSERT serialisation left to the implementation as a separate concern?
Gregory question: How does udanax-green handle a concurrent INSERT (or any concurrent allocation/arrangement transition) on the same document while another INSERT is in progress — does the implementation serialise at the document level, lock the allocator chain, or admit interleaving with a conflict-detection scheme?
