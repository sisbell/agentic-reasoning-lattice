**WF** (*WellFormedSpanFromEndpoints*). For s, r ∈ T with s < r and #s = #r, the pair γ = (s, r ⊖ s) is a well-formed level-uniform span (satisfying T12) with reach(γ) = r.

*Proof.* Since s < r and #s = #r, the divergence k is of type (i) with k ≤ #s — equal length excludes the prefix case. The width r ⊖ s has a positive component at position k (namely rₖ − sₖ > 0), so it is positive with action point k ≤ #s; T12 is satisfied. By D1, reach(γ) = s ⊕ (r ⊖ s) = r. The span is level-uniform: #width(γ) = #(r ⊖ s) = max(#r, #s) = #s = #start(γ).  ∎

*Formal Contract:*

- *Preconditions:* s, r ∈ T with s < r and #s = #r.
- *Definition:* γ = (start(γ), width(γ)) = (s, r ⊖ s).
- *Postconditions:* γ is a well-formed level-uniform span satisfying T12 — its width r ⊖ s is positive with action point k ≤ #s, and #width(γ) = #start(γ); and reach(γ) = s ⊕ (r ⊖ s) = r.
