# Channel Assignment — ASN-0115 review-20

**Date:** 2026-06-09 20:54

## Issue 1: C0a (PrefixConfinement) is applied outside its stated contract
Reason: The review supplies the complete replacement derivation from T5 (ContiguousSubtrees, ASN-0034) — a foundation already cited in this ASN — and the step (ordinal-level width plus `#s ≥ 2` ⟹ every `t ∈ ⟦σ⟧` agrees with `s` on its first `m−1` components) is purely formal, needing neither design intent nor implementation evidence.

## Issue 2: The reachability precondition and its use-site inventory are stated three times
Reason: Pure editorial pruning — collapse the thrice-stated precondition to one statement and delete the duplicate "may fail" enumeration and convention appeal; no design or implementation question is involved.

## Issue 3: The single-boundary-crossing-span deferral is repeated across three sections
Reason: Pure redundancy — consolidate a deferral pointer that appears in three places to the Open Questions entry; the substantive restriction is already proved internally (ordinal-level confinement), so no channel is needed.

## Issue 4: The V-spec definition slot carries forward-reference justifications and a consumer inventory
Reason: Structural/editorial — relocate or cut the "why imposed directly" and "distinct from R6" rationale and drop the `act/item/deliver` consumer list and `project`-parity appeal; nothing here turns on design intent or implementation behavior.
