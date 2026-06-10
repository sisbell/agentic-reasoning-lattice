# Channel Assignment — ASN-0115 review-21

**Date:** 2026-06-09 21:15

## Issue 1: R6's `act = ∅` sub-case is justified by a false premise, and "terminal overrun" mischaracterizes it
Reason: Internal. The correction is purely about the geometry of the span's depth-`m_S` slice relative to the active range, and the fix the reviewer prescribes (split `V_S(d)=∅` from `V_S(d)≠∅`, discharge the latter by slice-disjointness) is built entirely from machinery already in the ASN — D-SEQ★, the Confinement lemma, S8-depth. No design intent or implementation evidence bears on whether the sub-case reasoning is sound.

## Issue 2: undefined symbol `n` in the slice characterization
Reason: Internal. `n` is fixed by the ASN's own definitions as the width's deepest component `ℓ_{m_S}`, confirmed by the §Exactness worked instance (`ℓ = δ(5,2)` → 5-element slice); binding it at first use is a notational fix needing no external channel.

## Issue 3: R6 claim statement and R6 proof restate the same scoping caveat (anti-bloat)
Reason: Internal. This is a de-duplication of the ASN's own prose — state the bindable-slice scoping once (property in the claim, derivation in the proof) — with no semantic change and nothing to verify against design intent or the implementation.

## Issue 4: defensive and meta-prose that does not advance the reasoning (anti-bloat)
Reason: Internal. Trimming meta-commentary, a forward reference, and an unraised-objection defense removes nothing load-bearing; the surviving statements (the Confinement quantifier, the reachability precondition, the per-case citations) are all already in the ASN, so no channel is needed.
