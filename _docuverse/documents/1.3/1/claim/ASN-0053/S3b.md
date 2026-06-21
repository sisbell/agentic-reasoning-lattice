**S3b (MergeSplitInverse).** For adjacent level-uniform spans α and β with level_compat(start(α), start(β)), merging α and β (S3) and splitting the result at the shared boundary (S4) recovers the unordered pair {α, β} exactly: the split yields a left part λ and a right part ρ with {λ, ρ} = {α, β}. The assignment of α and β to the left/right positions is determined by the adjacency direction: in Case A (reach(α) = start(β)), λ = α and ρ = β; in Case B (reach(β) = start(α)), λ = β and ρ = α.

*Proof.* Adjacency means reach(α) = start(β) or reach(β) = start(α). We handle each disjunct.

*Case A: reach(α) = start(β).* The merge produces γ = (start(α), r ⊖ start(α)) where r = max(reach(α), reach(β)) = reach(β), since reach(α) = start(β) < reach(β) (β is non-empty). So γ = (start(α), reach(β) ⊖ start(α)) with reach(γ) = reach(β). The shared boundary p = start(β) is interior to γ: start(α) < start(β) (since α is non-empty, start(α) < reach(α) = start(β)) and start(β) < reach(β) = reach(γ) (since β is non-empty). Level compatibility holds by assumption.

Splitting γ at p yields λ = (start(α), p ⊖ start(α)) and ρ = (p, reach(γ) ⊖ p). For λ: p ⊖ start(α) = reach(α) ⊖ start(α) = width(α) by WR (α is level-uniform). So λ = (start(α), width(α)) = α. For ρ: reach(γ) ⊖ p = reach(β) ⊖ start(β) = width(β) by WR (β is level-uniform). So ρ = (start(β), width(β)) = β.

*Case B: reach(β) = start(α).* Here β abuts α from the left, so we derive the split directly from the merge formula rather than routing through commutativity. Since β is non-empty, start(β) < reach(β) = start(α); and since α is non-empty, start(α) < reach(α). The merge formula (S3) gives γ = (s, r ⊖ s) with s = min(start(α), start(β)) = start(β) (as start(β) < start(α)) and r = max(reach(α), reach(β)) = reach(α) (as reach(β) = start(α) < reach(α)). So γ = (start(β), reach(α) ⊖ start(β)) with start(γ) = start(β) and reach(γ) = reach(α). The shared boundary p = start(α) is interior to γ: start(γ) = start(β) < start(α) and start(α) < reach(α) = reach(γ). Level compatibility level_compat(start(γ), p) = level_compat(start(β), start(α)) holds — it is the assumed level_compat(start(α), start(β)) read in the other order, both asserting #start(α) = #start(β).

Splitting γ at p yields λ = (start(β), p ⊖ start(β)) and ρ = (p, reach(γ) ⊖ p). For λ: p ⊖ start(β) = start(α) ⊖ start(β) = reach(β) ⊖ start(β) = width(β) by WR (β is level-uniform), using start(α) = reach(β). So λ = (start(β), width(β)) = β. For ρ: reach(γ) ⊖ p = reach(α) ⊖ start(α) = width(α) by WR (α is level-uniform). So ρ = (start(α), width(α)) = α. Thus {λ, ρ} = {β, α} = {α, β}, with λ = β and ρ = α — the left-right assignment reversed relative to Case A, as required.  ∎

*Formal Contract:*

- *Preconditions:* α and β are level-uniform spans; both are non-empty (width(α) > 0 and width(β) > 0); level_compat(start(α), start(β)) holds; α and β are adjacent, i.e. reach(α) = start(β) ∨ reach(β) = start(α).
- *Postconditions:* Let γ = merge(α, β) (S3) and let p be the shared boundary (p = start(β) in Case A, p = start(α) in Case B); then split(γ, p) (S4) yields ⟨λ, ρ⟩ with {λ, ρ} = {α, β}. In Case A (reach(α) = start(β)): λ = α and ρ = β. In Case B (reach(β) = start(α)): λ = β and ρ = α.
- *Frame:* No spans other than α, β are read or produced; γ, λ, ρ are the only constructed values.
- *Definition:* The shared boundary p is the interior point of γ at which the original adjacency met (start(β) in Case A, start(α) in Case B); interiority start(γ) < p < reach(γ) is what makes p an admissible split point for S4.

- *Depends:*
  - S3 (MergeEquivalence) — supplies the merge operation and the endpoint formula γ = (s, r ⊖ s) with s = min(start(α), start(β)) and r = max(reach(α), reach(β)), used in both cases
  - S4 (SplitPartition) — supplies the split operation; the proof invokes split(γ, p) and reads off λ and ρ from S4's output structure
  - WR (WidthRecovery) — supplies reach(σ) ⊖ start(σ) = width(σ), used twice in each case to identify the split parts as α and β