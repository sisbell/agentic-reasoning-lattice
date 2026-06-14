# Channel Assignment — ASN-0134 review-15

**Date:** 2026-06-14 00:17

## Issue 1: V2's soundness justification contradicts the note's own worked trace
Reason: Internal. The fix is a rewording that aligns V2's justification with the note's own definition of "Q-affecting" (only *not-yet-read* constituents matter) and with its own worked trace (the banked, already-read `K₁`-emit) — both already present in the note, so no design-intent or implementation evidence is needed.

## Issue 2: G0 equates a single total order with sequential consistency
Reason: Internal. This is a standard-terminology correction (a single total order is serializability; SC additionally demands per-agent program order) resolved by the note's own §1 scoping that agents and their program order are out of the model — so the SC label was never supportable; the reviewer's richer reconciliation ("cross-home ops carry no program-order obligation") is already licensed by the Nelson locality material the note quotes ("order is always local," "zero coordination across regions").

## Issue 3: W5's "simply rejected" omits the self-emit branch of P-tgt
Reason: Internal. The fix turns entirely on `P-tgt`'s two-disjunct definition (`a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`), which the note already applies correctly in §4's target-residence race (it rejects only when both `a ∉ dom(L)` *and* `a ≠ a_emit(Σ, d')`); W5 need only be brought into line with that already-present reasoning.
