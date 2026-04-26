# Cone Review — ASN-0034/TA2 (cycle 1)

*2026-04-26 01:31*

### TumblerSub overloads `aᵢ`/`wᵢ` to mean both native and zero-padded values
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition) commits `aᵢ ∈ ℕ` only on the native index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`. ZPD introduces explicit `â`, `ŵ` for zero-padded extensions to keep the native projection symbol unambiguous.
**ASN**: TumblerSub's *Definition* parenthetical: "all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k". The same `aᵢ`/`wᵢ` symbol then appears in the Pos derivation and in TA2's prose with mixed interpretations — Divergence-case (i) cites native projections (k ≤ #w ∧ k ≤ #a, native `wₖ ≠ aₖ`), sub-case (ii-a) cites the padded value (k > #w, "wₖ = 0 by zero-padding").
**Issue**: ZPD already standardised `â`/`ŵ` precisely to avoid this. TumblerSub re-uses the bare `aᵢ`/`wᵢ` with a local re-binding, requiring the reader to track which interpretation is in scope at each cite. Identical symbols carrying two meanings inside the same proof is exactly the ambiguity the precise reader must guard against.
**What needs resolving**: Either commit to the ZPD `â`/`ŵ` notation throughout TumblerSub when the zero-padded interpretation is intended, or rename the operands to a padded-tumbler symbol, so the symbol used in TumblerSub has exactly one meaning. Native and padded projections must be lexically distinguishable.

### TA2 (WellDefinedSubtraction) duplicates TumblerSub's already-established postcondition
**Class**: OBSERVE
**ASN**: TumblerSub's Postconditions already include `a ⊖ w ∈ T, #(a ⊖ w) = L`, established by the in-line "Each component of the result is a natural number..." paragraph. TA2 then re-states "`a ⊖ w` is a well-defined tumbler in `T`" and re-walks the same case analysis (no-divergence; divergence sub-cases (i) and (ii)) to reach the same conclusion.
**Issue**: Two parallel proofs of the same fact in one ASN. The second adds nothing not delivered by the first, and forks maintenance: any future tightening of the carrier-membership argument would need to land in two places.

### Meta-prose justifying Consequence-vs-Axiom classification in NAT-sub
**Class**: OBSERVE
**ASN**: NAT-sub's strict-monotonicity passage opens "is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from..." and references "the same concern that kept NAT-order's disjointness form... from being separately exported". Strict-positivity opens analogously. The Formal Contract bullets repeat this justification ("recorded as a Consequence rather than an axiom clause so the derivation is not laundered through a non-minimal clause").
**Issue**: This is structural-classification commentary — defensive justification of why the slot is *Consequence:* rather than *Axiom:* — not mathematical content. The reader following the derivation has to skip past it to reach the proof. The classification choice can be conveyed by the slot label alone.

VERDICT: REVISE
