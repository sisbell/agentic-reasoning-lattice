# Channel Assignment — ASN-0051 review-26

**Date:** 2026-05-15 21:29

## Issue 1: SV0 is a definitional restatement, not a substantive claim
Reason: The fix is internal — reformulating SV0 as a claim about which state components participate in resolution requires inspection of each elementary transition's effect/frame, all of which are specified in ASN-0047 and cited herein. No design intent or implementation evidence beyond the algebra is needed.

## Issue 2: SV6 precondition omits required T4-validity of s
Reason: The fix is internal — T4-validity is defined in ASN-0036 (the source of T4b's N/U/D projections) and L4's permission of non-T4-valid span starts is in ASN-0043. Stating the precondition explicitly is an authorial correction, not an evidence question.

## Issue 3: SV10 existential lacks a concrete witness
Reason: The fix is internal — constructing a tumbler witness for partial projection requires only the existing definitions (coverage, π, M(d)) and the S/L-invariants already in scope. Analogous to the SV6 worked example, which was constructed without channel input.

## Issue 4: wp analysis mixes pre-state and post-state predicates
Reason: The fix is internal — re-expressing wp as a pre-state predicate parameterised by transition effect-inputs draws only on the transition specifications in ASN-0047 (K.μ⁻'s V_remove parameter, K.μ⁺'s new-mapping parameter, etc.). Pure mathematical reformulation.

## Issue 5: Worked example covers only m = 1 and injective M(d) for SV11
Reason: The fix is internal — extending the example to m ≥ 2 and non-injective M(d) requires only S5 (UnrestrictedSharing, ASN-0036) and the existing block/span definitions. Construction is a mathematical exercise within the ASN.

## Issue 6: "Same-origin coverage growth" section has no formal status
Reason: The fix is internal — the section already cites Nelson's design distinction [LM 2/14, 4/23, 4/25] and Gregory's `tumblerincrement` evidence. The remaining decision (formalize vs. defer) is an authorial scoping choice using content already in hand; no new channel consultation is required.

## Issue 7: SV6 proof step combining cases would benefit from explicit structure
Reason: The fix is internal — extracting a shared lemma from two T1(i)-divergence arguments is pure proof restructuring. No external evidence is implicated.
