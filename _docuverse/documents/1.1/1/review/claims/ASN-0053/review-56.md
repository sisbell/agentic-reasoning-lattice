I read the foundation statements, then the full ASN as a dependency system: the within-ASN DAG (WF, WR → S0/SC/S6 → S1/S2/S3/S4/S5 → S7/S8/S9/S10/S11*), and every foundation citation's precondition discharge.

The core algebra is sound. I verified the load-bearing precondition chains across claim boundaries and found them unbroken:

- **WF** discharges D1's five preconditions at `(s, r)` (equal length excludes T1 case (ii), so `divergence(s,r) ≤ #s`), and draws `Pos(r⊖s)` / `actionPoint(r⊖s)=k≤#s` / `#(r⊖s)=#s` from TumblerSub+ZPD+Divergence. **WR** discharges all nine D2 preconditions at `(s, reach(σ), ℓ)`.
- **S5** correctly discharges TA-assoc's `k_{d'} ≤ #d` via `k_{d'} ≤ #p = #s = #d` (ρ-validity + level_compat + λ level-uniformity), then TA-LC's `actionPoint(d⊕d') = min(k_d,k_{d'}) ≤ k_d ≤ #s`. **S9** correctly observes the equal-start case makes `#start(αᵢ)=#start(βᵢ)=#s` automatic, so TA-LC applies without a level-uniformity precondition — and S9's contract correctly omits that precondition.
- Case analyses are exhaustive: **S9** walks all six (1a/1b/2a/2b/3a/3b) in full; **SC** five; **S11d** all SC cases with both containment orientations; **S8**'s loop invariant addresses init/merge/emit/finalize plus non-emptiness, and N1/N2 strictness is correctly traced to the emit condition rather than to sortedness.
- All worked examples (S4/S5/S8/S11/S11c arithmetic) check out.

For each level-uniform claim, `level_compat(start(α),start(β))` + per-span level-uniformity correctly forces all boundary tumblers to one length, and reach-in-`T` is correctly placed via TumblerAdd's carrier postcondition before any membership test consumes it. I found no correctness, precondition, or case-coverage defect. The findings below are observations only.

### D0 declared "cited" but never cited; WF/WR reconstruct it instead
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined) — postconditions `Pos(b⊖a)`, `actionPoint(b⊖a) = divergence(a,b)`, `#(b⊖a)=L`
**ASN**: Properties Introduced table row "D0 | Displacement well-definedness: a < b and divergence(a, b) ≤ #a (DisplacementWellDefined, ASN-0034) | **cited**"; WF and WR proofs and their Depends lists (which name Divergence, TumblerSub, ZPD but not D0)
**Issue**: No proof in ASN-0053 cites D0. WF instead reconstructs D0's exact width result — "the width r ⊖ s has a positive component at position k (namely rₖ − sₖ > 0)... action point k ≤ #s" / `actionPoint(r⊖s)=zpd(r,s)=k`, `#(r⊖s)=#s` — from TumblerSub+ZPD+Divergence plus the equal-length divergence analysis. But D0 delivers precisely `Pos(b⊖a)`, `actionPoint(b⊖a)=divergence(a,b)`, `#(b⊖a)=L` at `(a,b)=(s,r)` under `a<b` and `divergence(a,b)≤#a` — the two conditions WF already establishes. The table's "cited" status misrepresents the actual dependency edge, and WF re-derives a packaged foundation result.
**What needs resolving**: Either cite D0 in WF (replacing the inline positivity/action-point reconstruction, which would also shorten WF's Divergence/ZPD/TumblerSub coupling), or correct the table so D0 is not marked "cited" if the reconstruction is deliberately kept.

### Use-site inventories and dependency-justification prose in structural slots
**Class**: OBSERVE
**Foundation**: n/a (recurs across several claims)
**ASN**: S11's Depends-on-TumblerAdd ("...this membership is consumed twice. It is needed already in the boundary characterization... and again in the ρ-construction... Second, the result-length identity..."); S9's Depends-on-T1 (a paragraph re-narrating which T1 postcondition is used at which case); S11c's Depends-on-T1; S6's Axiom prose: "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub...) and the round-trip identity (D1...), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ."
**Issue**: Several Depends/Axiom entries have grown into multi-sentence essays that inventory every use-site or argue why a dependency is *needed* (ruling out alternatives) rather than stating what it *supplies*. The S6 Axiom prose is the clearest "explains why the axiom is needed rather than what it says" instance. A reader scanning the contract for "what does TumblerAdd give me" must skip past consumption traces. Per the cross-cycle warning, these compound if not trimmed at source.
**What needs resolving**: Reduce each Depends entry to the fact the dependency supplies (e.g., "TumblerAdd — carrier postcondition `a⊕w∈T` and result-length `#(a⊕w)=#w`"); move per-site consumption narration into proof prose where it belongs, and drop the alternative-ruling-out justification from the S6 Axiom slot.

### S0 stated with different preconditions in narrative vs. formal block
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder)
**ASN**: Narrative "## Convexity" states `(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)`; the formal **S0** block states `(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ q ∈ T ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)` (adds `q ∈ T`)
**Issue**: The two statements of S0 in the same document carry different precondition sets. The formal block adds `q ∈ T` and argues it must be consumer-supplied (q being given, not constructed), since the goal `q ∈ ⟦σ⟧` unfolds to `q ∈ T ∧ start ≤ q < reach`. The narrative omits it. Both are sound in-system (T1's `≤` relates only members of T, so `p ≤ q` already presupposes `q ∈ T`), but a precise reader sees two contracts for one claim. The formal block is internally consistent and the authoritative one; the narrative is the looser preview.
**What needs resolving**: Add `q ∈ T` to the narrative S0 statement to match the formal contract, or mark the narrative statement as informal so the formal block is unambiguously the contract.

VERDICT: OBSERVE