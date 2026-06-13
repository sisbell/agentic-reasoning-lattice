# Channel Assignment — ASN-0123 review-29

**Date:** 2026-06-13 13:46

## Issue 1: The cross-owner identity derivation is stated three times
Reason: Pure deduplication — the full structural argument already exists at the V9 preamble (kept) and is to be relocated/trimmed, not re-derived. Consolidating prose already present in the note; no design intent or implementation evidence bears on where the argument lives.

## Issue 2: The node-tier exclusion is re-argued in three sections
Reason: The exclusion's rationale (intermediate account = a second permanent entity by P1, breaking single-mint) is already derived in the note; the fix states it once at P-tier and cites it. Internal restructuring, derivable from the ASN's own reasoning.

## Issue 3: Defensive meta-prose around assumptions and alternative proof routes
Reason: All three targets are deletions/compressions of prose that advance no claim — the V9w proof uses P4★ directly and the monotonicity route is a dead alternative. Removing the "load-bearing" sentence does not disturb deviation 4, which stays in the evidence section. Internal.

## Issue 4: Definitions enumerate their downstream consumers
Reason: Dropping consumer enumerations and collapsing duplicate "see the evidence section" deferrals is editorial; nextv's registry-purity is a fact already stated and restateable as a property. No external channel needed.

## Issue 5: B-Seq is cited for serialization against the note's own non-transfer discipline
Reason: A citation swap to ASN-0047's SequentialTransitionAxiom, which the note already invokes (nextv well-definedness, atomicity remark) and which the review identifies as the correct premise. Derivable from the ASN's own content; neither channel covers sibling-ASN citations.

## Issue 6: Single-step coverage lemma cited for the composite (V10)
Reason: V1's `L' = L` (a claim in this note) yields coverage invariance directly, or the composite-level LP3★ replaces the single-step LP3 — both are internal derivation/citation fixes. No implementation or design-intent input required.
