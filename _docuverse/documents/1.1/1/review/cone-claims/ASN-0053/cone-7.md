## Audit

Scanning for cross-claim consistency before per-claim analysis.

**S0, S11, S11d on T1 and ≤-transitivity.** S0's formal contract (Axiom section) states: "The non-strict compositions the proof needs… are *not* T1 exports; each is derived in the proof by case analysis on the abbreviation." S11's proof text (tightness section) states identically: "a mixed step T1 does not export." These two claims, within the same ASN, establish that ≤-transitivity is not a postcondition of T1 but is derivable from T1's strict postcondition (c) and the abbreviation `a ≤ b ≡ a < b ∨ a = b`.

**S11c Case 1 vs Case 2 on non-emptiness.** Case 1 explicitly provides a witness: "This is non-empty (start(α) < start(β) and start(α) ∈ ⟦α⟧ \ ⟦β⟧)." Case 2 states "The result is exactly 1 span" without exhibiting a witness or citing S2. The "exactly 1" postcondition requires both "expressible as 1 span" (provided by γ' construction) and "not 0 spans" (non-emptiness, not addressed). The direct witness reach(β) ∈ {t : reach(β) ≤ t < reach(α)} is one step from the Case 2 hypothesis reach(β) < reach(α), but it is absent from the proof.

All other claims audit clean: S0's four-case ≤-composition derivation is rigorous; WF's T1 case-(ii) elimination via NAT-addcompat + NAT-order irreflexivity is sound; SC's WLOG argument is valid (each case clause is symmetric or carries explicit "or symmetrically"); S11's element-chasing, boundary derivation, and tightness contradiction all close correctly; S11d's table is complete and each row delegates to the correct sub-claim; S2 and S6 are immediate from T12 and TumblerAdd respectively.

---

### S11d Depends contradicts S0 and S11 on T1's ≤-transitivity exports
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) postcondition (c): `(A a,b,c ∈ T : a < b ∧ b < c : a < c)` — strict transitivity only. T1's formal contract lists no ≤-transitivity postcondition.
**ASN**: S11d Depends field — "T1 (LexicographicOrder, ASN-0034) — supplies the transitivity of ≤ and < that closes the SC(iv)-reverse inline derivation of ⟦α⟧ ⊆ ⟦β⟧."
**Issue**: The annotation claims T1 "supplies the transitivity of ≤ and <." T1 exports only strict `<`-transitivity as postcondition (c). S0's formal contract (Axiom section) states explicitly that ≤-compositions "are *not* T1 exports; each is derived in the proof by case analysis on the abbreviation." S11's tightness proof repeats this: "a mixed step T1 does not export." S11d's Depends annotation directly contradicts these two established statements in the same ASN. The inline proof ("compose transitively (T1)") further skips the four-case derivation that S0 and S11 perform, replacing a derivation with a false attribution.
**What needs resolving**: The Depends annotation must be corrected to state that T1 supplies the building blocks — strict postcondition (c) and the abbreviation `a ≤ b ≡ a < b ∨ a = b` — from which the ≤-compositions in the SC(iv)-reverse derivation are derived by case analysis (per S0's established technique), not as a direct T1 postcondition. The inline proof should either perform the case splits explicitly or cite S0's technique by name.

---

### S11c Case 2 claims "exactly 1 span" without establishing non-emptiness of ⟦γ'⟧
**Class**: REVISE
**Foundation**: S2 (EmptyDistinction) — every well-formed span denotes a non-empty set; or direct witness from Case 2 hypothesis.
**ASN**: S11c Case 2 — "WF gives a well-formed level-uniform span with reach(γ') = reach(α). The denotation ⟦γ'⟧ = {t : reach(β) ≤ t < reach(α)} = ⟦α⟧ \ ⟦β⟧. The result is exactly 1 span."
**Issue**: The postcondition "exactly 1 span" requires both that the set is represented by 1 span (established by constructing γ') and that the set is non-empty (not representable by 0 spans). Case 1 establishes non-emptiness explicitly: "This is non-empty (start(α) < start(β) and start(α) ∈ ⟦α⟧ \ ⟦β⟧)." Case 2 makes no corresponding argument. The direct witness reach(β) ∈ {t : reach(β) ≤ t < reach(α)} follows in one step from the Case 2 hypothesis reach(β) < reach(α) — but neither this witness nor S2 (which would ground non-emptiness through the well-formed span γ') is cited. S2 does not appear in S11c's Depends. The "exactly 1" conclusion in Case 2 is unsupported at the non-emptiness step.
**What needs resolving**: Case 2 must establish ⟦γ'⟧ ≠ ∅, either by exhibiting reach(β) as a direct witness (reach(β) ≤ reach(β) trivially and reach(β) < reach(α) by hypothesis, placing reach(β) ∈ ⟦γ'⟧) or by citing S2 on the well-formed span γ'. If S2 is used, it must be added to S11c's Depends.

---

VERDICT: REVISE