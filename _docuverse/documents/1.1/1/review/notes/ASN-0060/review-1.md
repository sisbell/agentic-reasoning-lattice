# Review of ASN-0060

## REVISE

### Issue 1: Free variable n in I6 and I7
**ASN-0060, Shift Order Preservation / Shift Injectivity**: `(A v₁, v₂ : #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`
**Problem**: Both formal statements quantify over v₁ and v₂ but leave n as a free variable without its n ≥ 1 constraint. The shift is only defined for n ≥ 1 (δ(n, m) must be positive for TumblerAdd). Compare TA1 in ASN-0034, which explicitly quantifies w and constrains w > 0 in the guard.
**Required**: Quantify n explicitly: `(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))` for I6, and similarly for I7.

### Issue 2: TA0 precondition not verified in OrdinalShift definition
**ASN-0060, Ordinal Shift**: "shift(v, n) = v ⊕ δ(n, m)" then immediately "By TumblerAdd (ASN-0034): shift(v, n)ᵢ = vᵢ for i < m..."
**Problem**: TumblerAdd is invoked without verifying its precondition TA0: the action point k of the displacement must satisfy k ≤ #v. Here k = m and #v = m, so m ≤ m — trivially satisfied but unstated. Precondition verification before application is the discipline ASN-0034 establishes.
**Required**: State "TA0 is satisfied: the action point of δ(n, m) is m = #v" before expanding TumblerAdd.

### Issue 3: No concrete example
**ASN-0060**: Definitions and proofs but no worked instance.
**Problem**: No example verifies the definitions against specific values. A minimal scenario: v = [2, 3, 7], n = 4, so δ(4, 3) = [0, 0, 4] and shift(v, 4) = [2, 3, 11]. For I6: v₁ = [2, 3, 5] < v₂ = [2, 3, 9], shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). This takes two lines and catches definition errors that symbolic proofs miss.
**Required**: At least one concrete example verifying shift computation and one verifying I6 or I7.

### Issue 4: Shift composition not derived
**ASN-0060, Ordinal Shift**: Order preservation and injectivity are established; algebraic consequences are not explored.
**Problem**: The identity shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂) follows directly: by TA-assoc, (v ⊕ δ(n₁, m)) ⊕ δ(n₂, m) = v ⊕ (δ(n₁, m) ⊕ δ(n₂, m)); by TumblerAdd, δ(n₁, m) ⊕ δ(n₂, m) = δ(n₁ + n₂, m). This is the natural additivity/composability property — anyone chaining shifts needs it, and it falls out in three lines.
**Required**: State and derive shift composition as a labeled lemma.

### Issue 5: Component positivity justification incomplete
**ASN-0060, Ordinal Shift**: "since vₘ + n > 0 whenever vₘ ≥ 1 — component positivity"
**Problem**: The conditional "whenever vₘ ≥ 1" leaves vₘ = 0 unaddressed. When vₘ = 0, shift(v, n)ₘ = n ≥ 1 > 0 — the result is still positive. The full picture is: the shifted component is positive for all vₘ ≥ 0 (since n ≥ 1), which is stronger than preservation. Either both cases should be stated, or vₘ ≥ 1 should appear as an explicit precondition on the shift's domain.
**Required**: State that shift(v, n)ₘ = vₘ + n > 0 unconditionally (since n ≥ 1), or restrict the domain to vₘ ≥ 1 and state it as a precondition.

## OUT_OF_SCOPE

### Topic 1: Shift inverse
**Why out of scope**: (v ⊕ δₙ) ⊖ δₙ does not recover v in general — TumblerSub copies the tail from the minuend, not the subtrahend, so position-m gets the shifted value. TA4's preconditions (all components before k must be zero) are too restrictive for general recovery. A dedicated inverse operation belongs in a future ASN.

### Topic 2: V-position formal definition
**Why out of scope**: The ASN uses "V-position" as informal context. The formal definition of V-positions as Vstream arrangement addresses belongs in the arrangement-layer ASN, not here. The mathematics works for arbitrary tumblers regardless.

VERDICT: REVISE
