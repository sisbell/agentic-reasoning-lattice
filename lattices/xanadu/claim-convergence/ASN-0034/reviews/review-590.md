# Cone Review — ASN-0034/TA4 (cycle 2)

*2026-04-26 02:18*

Reading through the ASN to find issues that span multiple claims.

### TA0 missing NAT-order in Depends
**Class**: REVISE
**ASN**: TA0 (WellDefinedAddition). The Formal Contract states preconditions `a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a` and the Depends list enumerates `TumblerAdd, T0, TA-Pos, ActionPoint` — but NAT-order is not listed.
**Issue**: TA0's precondition `actionPoint(w) ≤ #a` directly uses the relation `≤` on ℕ. That symbol is grounded by NAT-order (which posits `<` and defines `≤ ⟺ < ∨ =`). Sibling claims in this ASN that use `≤` (T1, TumblerAdd, ActionPoint, T0, etc.) all list NAT-order in their Depends with an explicit reason. TA0 is the sole exception. The body justifies inclusion of TA-Pos by saying `Pos(w)` ensures the action point exists, and ActionPoint by saying `actionPoint(w)` appears in the bound — but the bound itself uses `≤`, whose grounding axiom is omitted. Downstream consumers reading TA0's contract in isolation cannot trace the meaning of `≤` to a posited claim, breaking the convention used elsewhere in the ASN.
**What needs resolving**: Add NAT-order to TA0's Depends with a reason citing the use of `≤` in the precondition `actionPoint(w) ≤ #a`.

VERDICT: REVISE
