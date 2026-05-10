# Review of ASN-0053

## REVISE

### Issue 1: D0 is formally ill-defined when a = b and its claimed consequence is false for that case
**ASN-0053, The reach function**: "D0 (*Displacement well-definedness*). a ≤ b, and the divergence k of a and b satisfies k ≤ #a. D0 ensures the displacement b ⊖ a is a well-defined tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied)."
**Problem**: Two defects. (1) ASN-0034 defines `divergence(a, b)` only for `a ≠ b`. When `a = b`, the divergence is undefined, so D0's formal condition cannot be evaluated — the predicate is ill-formed, not merely false. (2) The prose claims D0 ensures "a ⊕ (b ⊖ a) is defined (TA0 satisfied)." When `a = b`, TumblerSubtract produces the zero tumbler, and TA0 requires `w > 0`, so `a ⊕ (b ⊖ a)` is *not* defined. The claimed consequence is false for the case D0's "a ≤ b" admits. The surrounding text acknowledges this ("When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed") — which directly contradicts D0's own claim.
**Required**: Change D0's precondition from `a ≤ b` to `a < b`. This excludes the degenerate case that the text already handles separately, makes the divergence reference well-defined, and makes the claimed consequence ("TA0 satisfied") true.

### Issue 2: S8 normalization construction omits the empty span-set boundary case
**ASN-0053, Normalization (S8)**: "Sort the component spans by start position... *Initialization.* After the first span σ₁, E = ∅ and [s, r) = [start(σ₁), reach(σ₁)) = ⟦σ₁⟧."
**Problem**: The construction assumes n ≥ 1 — it initializes from σ₁, which does not exist when n = 0. The empty span-set ⟨⟩ denoting ∅ is a valid input and is vacuously normalized (N1 and N2 hold vacuously over an empty sequence). The loop invariant, initialization, and finalization steps all require at least one span. This is a mandatory boundary case per the review standards.
**Required**: State the n = 0 case explicitly before the construction: "If n = 0, the result is the empty span-set ⟨⟩, which vacuously satisfies N1 and N2. For n ≥ 1, proceed as follows..." The loop invariant and termination argument then apply to n ≥ 1.

### Issue 3: S9 uniqueness proof cites only N2 where N1 is also required
**ASN-0053, Normalization (S9), Case 2**: "For j < i, p ∉ ⟦αⱼ⟧ since p = reach(αᵢ) > reach(αⱼ) by chaining N2."
**Problem**: The chain from reach(αⱼ) to reach(αᵢ) requires *both* N2 and N1: N2 gives `reach(αⱼ) < start(αⱼ₊₁)`, then N1 gives `start(αⱼ₊₁) < start(αⱼ₊₂) < ... < start(αᵢ)`, and non-emptiness of αᵢ gives `start(αᵢ) < reach(αᵢ)`. The full chain is `reach(αⱼ) < start(αⱼ₊₁) < ... < start(αᵢ) < reach(αᵢ) = p`. Citing only N2 omits the N1 steps and the non-emptiness step. The analogous argument for j > i correctly cites "by N2 and N1," making the inconsistency visible.
**Required**: Replace "by chaining N2" with the actual chain: "by N2 (reach(αⱼ) < start(αⱼ₊₁)), repeated application of N1 (start(αⱼ₊₁) < ... < start(αᵢ)), and non-emptiness (start(αᵢ) < reach(αᵢ))."

## OUT_OF_SCOPE

### Topic 1: LeftCancellation belongs in tumbler algebra (ASN-0034)
**Why out of scope**: The ASN correctly identifies this: "This is properly a tumbler arithmetic fact, belonging with ASN-0034." It is a pure tumbler-addition property with no span-specific content. Future revision of ASN-0034 should absorb it; this ASN's local statement is adequate for now.

### Topic 2: Span-set intersection, general difference, and exact representability
**Why out of scope**: S1 gives two-span intersection; S11 gives difference under containment. The general cases (intersection of two span-sets, difference of two arbitrary span-sets, conditions for exact representation ⟦Σ⟧ = P rather than ⟦Σ⟧ ⊇ P) are natural extensions that the algebra's building blocks support but that belong in a future ASN covering span-set operations.

VERDICT: REVISE
