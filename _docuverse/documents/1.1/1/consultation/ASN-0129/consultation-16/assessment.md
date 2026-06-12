# Channel Assignment — ASN-0129 review-16

**Date:** 2026-06-11 21:01

## Issue 1: QD-audit's surface-check expressibility argument covers only one disjunct of P-tgt
Reason: Internal fix. The acknowledgment's justification is already in the note's own content — PC6 establishes that `home`/frontier arithmetic lives behind atom bounds and V-PRIM admits no address arithmetic, so scoping the sentence to the residence disjunct and stating the self-emit exclusion as deliberate requires only restating commitments the note already makes.

## Issue 2: PC6 states the same granularity point twice; the internal-iteration point appears three times
Reason: Internal fix. This is pure deduplication — consolidating the `t ⊕ w` point into the costs paragraph and the internal-iteration point into PC6's evaluation-class definition changes no semantic content, so no design intent or implementation evidence bears on it.

## Issue 3: PD0's excluded-case parenthetical asserts an unproven stability claim, and "the same witness argument" is not the same argument
Reason: Internal fix. Both repair paths are self-contained: deletion removes an aside the classification already excludes, and the admit-with-proof path uses only facts the note already carries (grow-only persistence, T1 totally ordering tumblers per ASN-0034, transitivity) — the review even supplies the two-step argument.

## Issue 4: R3's transfer to extended-record steps cites RP-b alone, skipping the B2 hop
Reason: Internal fix. The correct citation chain ("B2 with RP-b") is exhibited elsewhere in the note's own text for the parallel L12/L12a transfer, and the alternative (resting on the step effects already cited in the same parenthetical) is likewise derivable from the ASN's content — no channel evidence is needed to choose or apply either.
