# Channel Assignment — ASN-0125 review-6

**Date:** 2026-06-13 09:04

## Issue 1: Attribution discharge invokes ASN-0042 ownership over a state that does not carry it
Reason: The reviewer's option (b) is fully internal — discharge RQ3 via home-document computability using the T4b/T6 projection already present in EL8(b)'s first half, and confine the EL3/EL13 monopoly arguments to substrate-supported facts. Deciding that the note must stop invoking out-of-scope ownership state needs no design-intent or implementation evidence; the available machinery is already in the note.

## Issue 2: `DC(ℓ')` is a state-relative predicate applied to a bare value with the evaluation state left implicit
Reason: Pure formalization — the reviewer supplies the exact value-level predicate to evaluate at the pre-state `Σ`, and EL7(vi)'s own proof already relies on the `dom(Σ.L) ⊆ dom(Σ₁.L)` reading, so the correction lives entirely in the note's definitions and proof.

## Issue 3: The successor is born unlisted — a consequence of EL7 not drawn out
Reason: The successor's listing status follows from the note's own machinery — editlink performs only `K.λ` and `assert_sup` (no `K.μ⁺_L`, EL7(i)), `Σ₂.M = Σ.M`, Df-LISTED, and the two discovery regimes of EL11 — and the reviewer explicitly scopes this to surfacing defined behavior, not the coupling invariant of Open Question 7.

## Issue 4: Miscited foundation operator
Reason: Internal citation correction — the note's own "Above the substrate" paragraph and EL11(b) already attribute `Observe_K` to ASN-0086, so the Scope paragraph only needs to match its own usage.

## Issue 5: `Df-LISTED` reinvents ASN-0047's `Contains`
Reason: Foundational alignment with ASN-0047's existing `Contains`/CurrentContainment predicate, whose definition the reviewer has supplied; the fix abbreviates `listed` to it and keeps the note's own CL-OWN structural observation, requiring neither design intent nor implementation evidence.
