# Channel Assignment — ASN-0125 review-7

**Date:** 2026-06-13 10:30

## Issue 1: `editlink` and `assert_sup` are treated as reachability-producing without discharging ValidComposite
Reason: Internal. The discharge invokes ASN-0047's ValidComposite clauses (J0, J1★, J1'★) — a foundation the note already builds on — and the note already proves the frame that makes them vacuous (no content allocation, no content-subspace `K.μ⁺`, no `K.ρ`; `Σ₂.C = Σ.C`, `Σ₂.R = Σ.R` in EL7(i), and Vocabulary fact V's per-transition frame clauses). No design intent or implementation evidence is needed; it is a proof-bookkeeping step over a referenced definition whose required content the review itself states.

## Issue 2: the "Layer transfer" exhaustiveness over-claim
Reason: Internal. The fix narrows an unverified universal ("every such fact") to the ASN-0086 results the note actually cites (R0a, `a_emit`, the Emit/Observe/Nullify contracts, wp Case 2, R3, R6a), each already named in the note and each manifestly referencing only `dom(L)` and `dom(M)` — both preserved by Vocabulary fact V and M1. Everything needed is visible within the note's own citations.

## Issue 3: "Scope" meta-paragraph and stray essay content in structural slots
Reason: Internal. Deleting the Scope paragraph and compressing the EL3 coordination remark and EL13 ownership-overlay digression is pure prose trimming; the load-bearing claims (the carrier requires no substrate change and conventions need an agreed root; cross-home — a fortiori per-asserter — order is not a state function) are already established by the EL3 derivation and EL13/EL1, so nothing external is consulted.
