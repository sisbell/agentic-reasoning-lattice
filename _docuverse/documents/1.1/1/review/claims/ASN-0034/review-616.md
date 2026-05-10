# Cone Review — ASN-0034/TA7a (cycle 1)

*2026-04-26 09:00*

### TA7a missing ZPD in Depends
**Class**: REVISE
**Foundation**: ZPD (ZeroPaddedDivergence)
**ASN**: TA7a Conjunct 2 proof: "Since `o₁ > w₁` gives `o₁ ≠ w₁`, the zero-padded sequences disagree at position 1, and **by ZPD's minimality** `zpd(o, w) = 1`."
**Issue**: TA7a's Conjunct 2 proof load-bearingly invokes ZPD's minimality clause to identify the divergence index as 1, and references TumblerSub's "ZPD-based dispatch" implicitly. However, ZPD does not appear in TA7a's *Depends* list (only in TA7a.1, TA7a.2, TA7a.3). A downstream consumer extracting TA7a's dependency closure will miss ZPD.
**What needs resolving**: Add ZPD to TA7a's *Depends* slot, with a citation noting its minimality role in fixing `zpd(o, w) = 1` from the position-1 disagreement.

---

### TA7a Conjunct 2 has a redundant precondition
**Class**: OBSERVE
**Foundation**: ActionPoint postcondition `1 ≤ actionPoint(w) ≤ #w`
**ASN**: TA7a Conjunct 2: `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ **k ≤ #o** ∧ #w ≤ #o ∧ o₁ > w₁ ⟹ o ⊖ w ∈ S)`
**Issue**: The conjunct lists `k ≤ #o` as a precondition. But ActionPoint guarantees `k ≤ #w`, and the conjunct also requires `#w ≤ #o`; chaining gives `k ≤ #o` automatically. The proof never invokes `k ≤ #o` as a hypothesis (the divergence is fixed at 1 from `o₁ > w₁`, independently of `k`). The precondition is implied by sibling preconditions and unused.

---

### TA7a.3 Depends lists items used only in narrative
**Class**: OBSERVE
**Foundation**: TA6 (ZeroTumblers), TA-PosDom (PositiveDominatesZero)
**ASN**: TA7a.3 *Depends* includes TA6 and TA-PosDom; the proof body's only mention of them is the trailing narrative sentence: "As a sentinel, `r` is not a valid address (TA6) and serves as a lower bound relative to every positive tumbler (TA-PosDom)".
**Issue**: The postcondition `o ⊖ o ∈ Z` is established without invoking either TA6 or TA-PosDom. Listing them in *Depends* inflates the dependency closure with non-load-bearing references; downstream traversal will follow these arrows unnecessarily.

---

### Redundant length conjunct in S definition
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition) clause `(A a ∈ T :: 1 ≤ #a)`
**ASN**: TA7a *Definition*: `**S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}`
**Issue**: The conjunct `#o ≥ 1` is implied by `o ∈ T` via T0's nonemptiness clause; including it in S's definition is redundant with carrier-level guarantees already in scope.

VERDICT: REVISE
