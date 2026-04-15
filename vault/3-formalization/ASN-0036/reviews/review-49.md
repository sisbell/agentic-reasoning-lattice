# Cone Review — ASN-0036/S8 (cycle 1)

*2026-04-13 15:56*

I'll read through the ASN content carefully, paying attention to cross-property chains.

### shift/inc equivocation — two distinct operations used interchangeably without bridging lemma

**Foundation**: OrdinalShift (ShiftDefinition) — `shift(v, n)` advances deepest component by `n`; TA5 (HierarchicalIncrement) — `inc(v, k)` modifies position `sig(v)` when `k = 0`
**ASN**: S8-depth defines `v + k = shift(v, k)` for `k ≥ 1`; S8 proof then says `"v + 1 = inc(v, 0) > v by TA5(a)"`, `"By TA5(c), v + 1 = inc(v, 0) satisfies #(v + 1) = m"`, and `"TA5(b) gives (v + 1)ᵢ = vᵢ for all i < sig(v)"`
**Issue**: The S8-depth definition establishes `v + 1 = shift(v, 1)` (OrdinalShift). The S8 proof cites TA5(a), TA5(b), and TA5(c) — which are postconditions of `inc(v, 0)`, a different operation. The proof asserts `v + 1 = inc(v, 0)` without establishing the equivalence. These operations coincide when `sig(v) = #v` (i.e., the last component is nonzero), which S8a guarantees for V-positions — but this bridge is never constructed. The equivalence is provable: OrdinalShift gives `shift(v,1)_m = v_m + 1` with all earlier components unchanged; TA5(c) gives `inc(v,0)_{sig(v)} = v_{sig(v)} + 1` with all earlier components unchanged; when `sig(v) = m`, both produce the same result by T3 (CanonicalRepresentation). Every citation of TA5 in the S8 proof could alternatively cite OrdinalShift and T1 directly, but as written the precondition chain has an unlinked step.
**What needs resolving**: Either establish `shift(v, 1) = inc(v, 0)` for tumblers with all-positive components (bridging OrdinalShift to TA5 via T3), or rewrite the S8 proof to cite OrdinalShift directly for the ordering, length-preservation, and prefix-preservation properties it already provides.

---

### V-position minimum depth #v ≥ 2 not established — postcondition 1 is false at depth 1

**Foundation**: OrdinalShift — `shift(v, n)ᵢ = vᵢ` for `i < #v` (prefix preservation requires the target position to be strictly before the action point)
**ASN**: S8-depth postcondition 1: `"(A k : 0 ≤ k < n : (v + k)₁ = v₁) — the subspace identifier precedes the action point and is copied unchanged by TumblerAdd's prefix rule."` S8a postconditions: `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`. S8-depth axiom: within a subspace, all V-positions share the same depth.
**Issue**: Postcondition 1 claims the subspace identifier `v₁` is preserved by ordinal shift — that position 1 "precedes the action point." OrdinalShift's action point is position `#v`. Position 1 precedes it iff `#v ≥ 2`. For I-addresses, S7c guarantees element-field depth `δ ≥ 2`, and postcondition 3 correctly cites this. For V-positions, no parallel constraint is stated. S8a gives `#v ≥ 1` (via T4's non-empty field constraint) but not `#v ≥ 2`. At `#v = 1`: `shift([s], k) = [s + k]`, so `(v + k)₁ = s + k ≠ s = v₁` for `k ≥ 1` — postcondition 1 is false. The S8 proof itself is not affected (its m = 1 case uses a direct argument that avoids postcondition 1, and the m ≥ 2 case correctly has `#v ≥ 2`), but any downstream consumer of postcondition 1 inherits an unsound guarantee at depth 1.
**What needs resolving**: Either add an explicit constraint `#v ≥ 2` for V-positions (paralleling S7c for I-addresses) and cite it in postcondition 1, or guard postcondition 1 with a `#v ≥ 2` precondition so its scope matches its validity.
