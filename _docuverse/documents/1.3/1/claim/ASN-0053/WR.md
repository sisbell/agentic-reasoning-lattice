**WR** (*WidthRecovery*). For a level-uniform span σ = (s, ℓ): reach(σ) ⊖ start(σ) = width(σ).

*Proof.* The reach has #reach(σ) = #s (since #(s ⊕ ℓ) = #ℓ = #s by the result-length identity). Width recovery follows from displacement uniqueness in the foundation: since s ⊕ ℓ = reach(σ), D2 (DisplacementUnique, ASN-0034) gives reach(σ) ⊖ start(σ) = ℓ = width(σ), provided its preconditions hold for (a, b, w) = (s, reach(σ), ℓ). We discharge them: s < reach(σ) by TA-strict on T12; ℓ > 0 and its action point k ≤ #s by T12; s ⊕ ℓ = reach(σ) by definition of reach (so TA0's preconditions hold, giving #(s ⊕ ℓ) = #ℓ = #s); divergence(s, reach(σ)) = k ≤ #s, the D2 precondition on divergence (established as in WF's proof: #s = #reach(σ) excludes the prefix case, so the divergence is of type (i)); #s ≤ #reach(σ) since both equal #s. Every D2 precondition is met, so reach(σ) ⊖ start(σ) = width(σ).  ∎

A worked instance of the unequal-length failure: σ = ([1, 3, 5], [0, 2]) has reach [1, 5], but [1, 5] ⊖ [1, 3, 5] = [0, 2, 0] ≠ [0, 2] — when #start > #width the recovered displacement does not round-trip.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a level-uniform span; ℓ > 0 with action point k ≤ #s (T12); s < reach(σ) (TA-strict on T12); s ⊕ ℓ = reach(σ) satisfies TA0's preconditions; divergence(s, reach(σ)) = k ≤ #s of type (i).
- *Postconditions:* reach(σ) ⊖ start(σ) = width(σ).
- *Definition:* start(σ) = s; width(σ) = ℓ; reach(σ) = s ⊕ ℓ.

- *Depends:*
  - D2 (DisplacementUnique, ASN-0034) — supplies the displacement uniqueness result `reach(σ) ⊖ start(σ) = ℓ` that is the claim's conclusion, once its preconditions are discharged for (a, b, w) = (s, reach(σ), ℓ)
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that qualifies the level-uniform span; the proof cites T12 to discharge D2's preconditions on ℓ
  - TA-strict (StrictIncrease, ASN-0034) — supplies `a ⊕ w > a` instantiated as s < reach(σ), discharging D2's precondition a < b
  - TA0 (WellDefinedAddition, ASN-0034) — supplies the result-length identity `#(s ⊕ ℓ) = #ℓ = #s` used to pin #reach(σ) = #s and to confirm TA0's own preconditions for the s ⊕ ℓ = reach(σ) step
- *Forward References:*
  - WF (WellFormedSpanFromEndpoints) — sibling claim whose proof contains the equal-length/divergence-type argument reproduced inline here; cited as a navigation pointer