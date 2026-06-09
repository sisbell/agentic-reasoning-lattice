# Channel Assignment — ASN-0116 review-21

**Date:** 2026-06-09 08:15

## Issue 1: Post-state appeal to ExtendedReachableStateInvariants rests on a premise the precondition does not assert
Reason: Internal. The reviewer offers two self-contained fixes — either strengthen the precondition to "Σ reachable from Σ₀" or discharge S8★ directly from P1 (inserted block is one run), I-SHIFT (shifted-suffix runs), and S8 per-subspace — both derivable from the ASN's own claims and the cited ASN-0047/ASN-0082 machinery already in hand.

## Issue 2: RAN's introduction is a use-site inventory of downstream consumers
Reason: Internal. A pure prose edit — strip the consumer enumerations from RAN and the block-disjointness fact, leaving their self-contained statements untouched. No design intent or implementation evidence bears on this.

## Issue 3: The freshness-vs-immutability caution is stated defensively twice
Reason: Internal. Editorial deduplication — keep the ghost-reference fact once where it is load-bearing (P4 new-block witnesses, P6) and reduce the P5 parenthetical to the bare proof step, both fully derivable from the ASN's existing P0/S3/L4/L9 content.
