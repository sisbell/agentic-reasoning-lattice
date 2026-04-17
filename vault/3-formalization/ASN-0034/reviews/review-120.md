# Cone Review — ASN-0034/D2 (cycle 1)

*2026-04-17 03:29*

### TA-LC's Depends omits NAT-order despite invoking trichotomy on action-point indices

**Foundation**: (foundation ASN — internal consistency; per-step NAT-* citation convention established by T0)
**ASN**: TA-LC's proof concludes the action-point-equality step with: *"Both strict orderings are impossible, so `k₁ = k₂`."* The two strict orderings `k₁ < k₂` and `k₂ < k₁` are ruled out by the case contradictions, and equality is concluded from the disjunction of the remaining options. TA-LC's Depends clause lists TumblerAdd, TA0, TA-Pos, ActionPoint, NAT-cancel, and T3 — no NAT-order citation.
**Issue**: The inference "¬(k₁ < k₂) ∧ ¬(k₂ < k₁) ⟹ k₁ = k₂" for natural-number indices rests on NAT-order's trichotomy clause. Without trichotomy — under only irreflexivity and transitivity — two naturals could be incomparable and the step would not go through. Sister proofs that use the same trichotomy pattern on ℕ indices cite NAT-order explicitly: T1 part (b) cites it for the component-level trichotomy, and T1 transitivity's case analysis on `k₁` vs. `k₂` proceeds under NAT-order's three exhaustive cases. TA-LC performs the same inference but omits the citation. A reviser who tightens NAT-order has no Depends-backed signal that TA-LC's action-point-equality step consumes trichotomy.
**What needs resolving**: TA-LC's Depends must cite NAT-order for the trichotomy step that promotes `¬(k₁ < k₂) ∧ ¬(k₂ < k₁)` to `k₁ = k₂`, matching the per-step citation policy applied in T1 and elsewhere. Alternatively, recast the step to make the trichotomy invocation explicit in-line and cite at that site.
