**TS3 (ShiftComposition).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

*Proof.* We show that shifting by n₁ then n₂ is the same as shifting by their sum: composing two ordinal shifts reduces to a single shift whose amount is the sum of the individual amounts.

Fix v ∈ T with #v = m, and fix n₁ ≥ 1, n₂ ≥ 1. We must prove shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂). We compute each side by expanding OrdinalShift and applying TumblerAdd's constructive definition (Definition TumblerAdd), then show the results agree at every component.

**Left side.** By OrdinalShift, shift(v, n₁) = v ⊕ δ(n₁, m), where δ(n₁, m) = [0, ..., 0, n₁] has action point m. Since m = #v, the precondition of TA0 is satisfied (k = m ≤ m = #v). Let u = v ⊕ δ(n₁, m). By TumblerAdd's constructive definition with action point k = m:

- For 1 ≤ i < m: uᵢ = vᵢ (prefix copy — all m − 1 higher-level components are preserved).
- At i = m: uₘ = vₘ + n₁ (single-component advance).
- No positions i > m exist, since #u = #δ(n₁, m) = m by the result-length identity.

Now we apply the second shift. By OrdinalShift, shift(u, n₂) = u ⊕ δ(n₂, m), where δ(n₂, m) has action point m. The precondition of TA0 is satisfied: k = m ≤ m = #u. Let L = u ⊕ δ(n₂, m) denote the left side. By TumblerAdd with action point k = m:

- For 1 ≤ i < m: Lᵢ = uᵢ = vᵢ (prefix copy, substituting the values of u established above).
- At i = m: Lₘ = uₘ + n₂ = (vₘ + n₁) + n₂ (advance, substituting uₘ = vₘ + n₁).
- Length: #L = #δ(n₂, m) = m by the result-length identity.

**Right side.** Since n₁ ≥ 1 and n₂ ≥ 1, their sum n₁ + n₂ ≥ 2 ≥ 1, so δ(n₁ + n₂, m) is a well-formed ordinal displacement with action point m. By OrdinalShift, shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m). The precondition of TA0 is satisfied: k = m ≤ m = #v. Let R = v ⊕ δ(n₁ + n₂, m) denote the right side. By TumblerAdd with action point k = m:

- For 1 ≤ i < m: Rᵢ = vᵢ (prefix copy).
- At i = m: Rₘ = vₘ + (n₁ + n₂) (single-component advance).
- Length: #R = #δ(n₁ + n₂, m) = m by the result-length identity.

**Comparison.** Both sides have length m: #L = m = #R. We verify component-wise equality:

- For 1 ≤ i < m: Lᵢ = vᵢ = Rᵢ — both sides copied the prefix from v.
- At i = m: Lₘ = (vₘ + n₁) + n₂ and Rₘ = vₘ + (n₁ + n₂). These are equal by NAT-addassoc (NatAdditionAssociative), which states `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`: instantiated with `vₘ, n₁, n₂`, it yields `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)`.

Every component agrees and both tumblers have the same length. By T3 (CanonicalRepresentation): L = R, that is, shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂). ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Depends:* OrdinalShift (OrdinalShift) — invoked three times (left side, second shift, right side) to unfold `shift(·, n) = · ⊕ δ(n, m)` ("By OrdinalShift, shift(v, n₁) = v ⊕ δ(n₁, m)" / "By OrdinalShift, shift(u, n₂) = u ⊕ δ(n₂, m)" / "By OrdinalShift, shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m)"); without OrdinalShift the entire reduction to `⊕` arithmetic could not begin. OrdinalDisplacement (OrdinalDisplacement) — invoked at every shift unfolding to fix the displacement form `δ(n, m) = [0, ..., 0, n]` with action point `m` ("δ(n₁, m) = [0, ..., 0, n₁] has action point m" and analogous instances for `δ(n₂, m)` and `δ(n₁ + n₂, m)") and at the right-side preface to source the well-formedness of `δ(n₁ + n₂, m)` from `n₁ + n₂ ≥ 2 ≥ 1`. TA0 (WellDefinedAddition) — invoked three times to discharge the precondition `k ≤ #v` for each `⊕` ("the precondition of TA0 is satisfied (k = m ≤ m = #v)" / "The precondition of TA0 is satisfied: k = m ≤ m = #u" / "The precondition of TA0 is satisfied: k = m ≤ m = #v") and to source the result-length identity `#u = #δ(n₁, m) = m` (and analogous identities for `#L` and `#R`); without TA0 the lengths would not be derivable and the comparison step could not establish `#L = m = #R`. TumblerAdd (TumblerAdd) — invoked at every component computation to apply the three-region rule (prefix copy for `i < k`, single-component advance at `i = k`, tail copy for `i > k`) ("By TumblerAdd's constructive definition with action point k = m") that produces the explicit values of `uᵢ`, `Lᵢ`, and `Rᵢ`. NAT-addassoc (NatAdditionAssociative) — invoked at the comparison step to convert `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)` ("These are equal by NAT-addassoc (NatAdditionAssociative), which states `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`"); without NAT-addassoc the load-bearing equality at position `m` is unsourced. T3 (CanonicalRepresentation) — invoked at the proof closing to convert component-wise plus length agreement into tumbler equality ("Every component agrees and both tumblers have the same length. By T3 (CanonicalRepresentation): L = R").
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)
