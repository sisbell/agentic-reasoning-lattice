# Regional Review — ASN-0034/Divergence (cycle 1)

*2026-04-23 17:26*

### T3 proof misattributes T0's carrier
**Class**: OBSERVE
**Foundation**: n/a (internal review)
**ASN**: T3 (CanonicalRepresentation), proof preamble: *"T3 follows from T0's definition of the carrier set. By T0, T is the set of all finite sequences over ℕ."*
**Issue**: T0 defines `T` as the set of *nonempty* finite sequences (`(A a ∈ T :: 1 ≤ #a)`). "All finite sequences over ℕ" drops T0's nonemptiness clause. The proof's conclusion survives the correction — nonempty finite sequences with matching length and components are equal by the same extensional argument — but the attribution misstates what T0 exports. Nonemptiness is not used anywhere in T3's reasoning, so the misquote is a paraphrase defect rather than a broken citation chain.

### Divergence's `i ∉ S ⟹ aᵢ = bᵢ` step elides equality-dichotomy
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Divergence, uniqueness/existence paragraph: *"NAT-wellorder supplies `min S`, whose minimality automatically discharges the `(A i : 1 ≤ i < min S : aᵢ = bᵢ)` conjunct"*
**Issue**: For `1 ≤ i < min S`, minimality gives `i ∉ S`, hence `¬(aᵢ ≠ bᵢ)`. Lifting this to the positive `aᵢ = bᵢ` requires the exactly-one trichotomy on ℕ at `(aᵢ, bᵢ)` (equivalently, equality-decidability). The dependency is declared (NAT-order is cited for trichotomy at candidate pairs `(k, k')`), but the phrase "automatically discharges" papers over the one inference step from `¬≠` to `=`. Nothing is missing from the axiom surface; only the narrative walk is compressed.

### Divergence postcondition bundles "unique" and "least"
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Divergence, postconditions: *"in case (i), `divergence(a, b) = k` is the unique least index satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`"*
**Issue**: The narrative's own uniqueness argument — trichotomy on `(k, k')` against either k's or k'​'s prior-agreement conjunct — shows the full characterization has exactly one solution, independent of any least-element selection. "Unique least" reads as though two qualifiers are doing separate work (characterization pins uniqueness; NAT-wellorder pins minimality), whereas the characterization alone is enough. The companion prose ("Case (i)'s value `k` is unique from the characterization alone, without appeal to NAT-wellorder") makes this distinction, which the postcondition then blurs.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 190s*
