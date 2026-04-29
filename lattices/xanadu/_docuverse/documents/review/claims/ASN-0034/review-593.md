# Cone Review — ASN-0034/TA4 (cycle 5)

*2026-04-26 03:14*

Reading through ASN-0034 against the previous findings (which appear to be addressed in the current text) and looking for new issues that span multiple claims.

I verified the proofs walk all cases:
- TA4 case analysis on `aₖ > 0 ∨ aₖ = 0` cleanly partitions, with NAT-sub right-telescoping discharging case 1 and T3 + NAT-closure left-identity discharging case 2.
- T1 trichotomy walks all three cases (Case 1: no divergence, Case 2: clause (α), Case 3: clauses (β)/(γ)) with reverse-witness ruling-out.
- TumblerSub's `âₖ > ŵₖ` derivation now does the case split (A)/(B) properly grounding T3's contrapositive against ZPD's padded-projection definition.

I verified precondition chains:
- TA4 → TumblerAdd: `actionPoint(w) ≤ #a` discharged by `k = #a`.
- TA4 → TumblerSub: `r ≥ w` discharged by TumblerAdd's dominance postcondition.
- TumblerSub → NAT-sub: `âₖ ≥ ŵₖ` from `âₖ > ŵₖ` via NAT-order.

I verified citations:
- TA0 now lists NAT-order in Depends.
- TumblerSub Postconditions now exports `Zero(a ⊖ w)` for the no-divergence branch.
- NAT-sub's Consequence prose no longer carries the meta-justification about classification.
- TA4 contains no implementation-comparison content.

All claim labels referenced in proofs and Depends lists (TA0, TumblerAdd, TumblerSub, TA-Pos, ActionPoint, T0, T1, T3, ZPD, Divergence, TA4, NAT-carrier, NAT-order, NAT-zero, NAT-closure, NAT-cancel, NAT-addcompat, NAT-addbound, NAT-discrete, NAT-wellorder, NAT-sub) are defined within the ASN content.

VERDICT: CONVERGED

## Result

Cone review converged.

*Elapsed: 4795s*
