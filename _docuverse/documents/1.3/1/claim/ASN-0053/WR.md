**WR (WidthRecovery).** For a level-uniform span σ = (s, ℓ): reach(σ) ⊖ start(σ) = width(σ).

*Proof.* The reach has #reach(σ) = #s (since #(s ⊕ ℓ) = #ℓ = #s by the result-length identity). Width recovery follows from displacement uniqueness in the foundation: since s ⊕ ℓ = reach(σ), D2 (DisplacementUnique, ASN-0034) gives reach(σ) ⊖ start(σ) = ℓ = width(σ), provided its preconditions hold for (a, b, w) = (s, reach(σ), ℓ). Four discharge immediately: s < reach(σ) by TA-strict on T12; ℓ > 0 with action point ≤ #s by T12; s ⊕ ℓ = reach(σ) by definition of reach (so TA0's preconditions hold, giving #(s ⊕ ℓ) = #ℓ = #s); and #s ≤ #reach(σ) since both equal #s. The fifth, divergence(s, reach(σ)) ≤ #s, we establish exactly as WF does, instantiated at (s, reach(σ)).

Since s < reach(σ), T1's trichotomy disjointness `¬(s < reach(σ) ∧ s = reach(σ))` gives s ≠ reach(σ), so divergence(s, reach(σ)) is defined. T1's order definition then witnesses s < reach(σ) by an index k (1 ≤ k) with sᵢ = reach(σ)ᵢ for 1 ≤ i < k and a strict disagreement at k. The witness falls in case (i) `k ≤ #s ∧ k ≤ #reach(σ) ∧ sₖ < reach(σ)ₖ` or case (ii) `k = #s + 1 ≤ #reach(σ)`. The equal length #s = #reach(σ) excludes case (ii): it would force #s + 1 ≤ #s, impossible since #s < #s + 1. So case (i) holds, giving k ≤ #s and sₖ < reach(σ)ₖ, whence sₖ ≠ reach(σ)ₖ. The conjunction `1 ≤ k ∧ k ≤ #s ∧ k ≤ #reach(σ) ∧ sₖ ≠ reach(σ)ₖ ∧ (A i : 1 ≤ i < k : sᵢ = reach(σ)ᵢ)` is exactly Divergence's case-(i) qualifier, whose uniqueness clause identifies k = divergence(s, reach(σ)). Hence divergence(s, reach(σ)) = k ≤ #s.

Every D2 precondition is met, so reach(σ) ⊖ start(σ) = width(σ).  ∎

A worked instance of the unequal-length failure: σ = ([1, 3, 5], [0, 2]) has reach [1, 5], but [1, 5] ⊖ [1, 3, 5] = [0, 2, 0] ≠ [0, 2] — when #start > #width the recovered displacement does not round-trip.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a well-formed level-uniform span — by T12, ℓ > 0 with action point ≤ #s, and #ℓ = #s by level-uniformity. This is the caller's only obligation; D2's preconditions for (a, b, w) = (s, reach(σ), ℓ) — s < reach(σ), s ⊕ ℓ = reach(σ), #s ≤ #reach(σ), and divergence(s, reach(σ)) ≤ #s — are intermediate results the proof discharges from well-formedness, not caller obligations.
- *Postconditions:* reach(σ) ⊖ start(σ) = width(σ).
- *Definition:* start(σ) = s; width(σ) = ℓ; reach(σ) = s ⊕ ℓ.

- *Depends:*
  - D2 (DisplacementUnique, ASN-0034) — supplies the displacement uniqueness result `reach(σ) ⊖ start(σ) = ℓ` that is the claim's conclusion, once its preconditions are discharged for (a, b, w) = (s, reach(σ), ℓ)
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that qualifies the level-uniform span; the proof cites T12 to discharge D2's preconditions on ℓ
  - TA-strict (StrictIncrease, ASN-0034) — supplies `a ⊕ w > a` instantiated as s < reach(σ), discharging D2's precondition a < b
  - TA0 (WellDefinedAddition, ASN-0034) — supplies the result-length identity `#(s ⊕ ℓ) = #ℓ = #s` used to pin #reach(σ) = #s and to confirm TA0's own preconditions for the s ⊕ ℓ = reach(σ) step
  - T1 (LexicographicOrder, ASN-0034) — its definition of s < reach(σ) supplies the witness k (with sᵢ = reach(σ)ᵢ for 1 ≤ i < k) in case (i) `k ≤ #s ∧ k ≤ #reach(σ) ∧ sₖ < reach(σ)ₖ` or case (ii) `k = #s + 1 ≤ #reach(σ)`; the equal length #s = #reach(σ) excludes case (ii) (which would force #s + 1 ≤ #s), leaving case (i) with k ≤ #s and sₖ ≠ reach(σ)ₖ; and its trichotomy disjointness `¬(s < reach(σ) ∧ s = reach(σ))` yields s ≠ reach(σ), well-defining divergence(s, reach(σ))
  - Divergence (Divergence, ASN-0034) — its case-(i) uniqueness clause identifies the T1 witness k with divergence(s, reach(σ)), so k ≤ #s discharges D2's precondition divergence(s, reach(σ)) ≤ #s
- *Forward References:*
  - WF (WellFormedSpanFromEndpoints) — sibling claim whose proof contains the equal-length/divergence-type argument reproduced inline here; cited as a navigation pointer