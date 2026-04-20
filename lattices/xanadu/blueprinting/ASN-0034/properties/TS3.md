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
- At i = m: Lₘ = (vₘ + n₁) + n₂ and Rₘ = vₘ + (n₁ + n₂). These are equal by the associativity of addition in ℕ: (vₘ + n₁) + n₂ = vₘ + (n₁ + n₂).

Every component agrees and both tumblers have the same length. By T3 (CanonicalRepresentation): L = R, that is, shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂). ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)
