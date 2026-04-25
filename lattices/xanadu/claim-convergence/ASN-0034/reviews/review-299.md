# Cone Review — ASN-0034/T10a.6 (cycle 1)

*2026-04-18 15:10*

### Standalone T10a.3 Depends omits T0 while main T10a.3 entry cites it
**Foundation**: T10a.3 is internal to this ASN (no foundation outside). The issue is within-document consistency between the Formal Contract of T10a (which enumerates T10a.3's dependencies) and the standalone T10a.3 block that follows.
**ASN**: The standalone T10a.3's Formal Contract begins "*Depends:* T10a (AllocatorDiscipline) … T10a.1 (UniformSiblingLength) … TA5 (HierarchicalIncrement) … NAT-addcompat … NAT-sub … NAT-zero … NAT-discrete … T3 (CanonicalRepresentation)." It does not list T0. By contrast, the main T10a contract's T10a.3 entry explicitly cites "T0 (CarrierSetDefinition — fixes the carrier as ℕ so that `k'`, every length term `#t`, `γ + k'₁ + … + k'_d`, and the depth-gap `d_B − d_A` lie in ℕ, supplying the set on which the NAT-* axioms speak at each order inference)."
**Issue**: The standalone T10a.3 proof invokes the same ℕ-membership inferences — "NAT-addcompat's strict successor inequality `n < n + 1` for every `n ∈ ℕ`", "The hypothesis `d_B > d_A` on naturals sharpens to `d_B − d_A ≥ 1`", etc. Those inferences require the carrier of each arithmetic term to be fixed at ℕ, which is T0's content. The standalone T10a.5's Formal Contract cites T0 explicitly for the structurally identical reason ("T0 (CarrierSetDefinition — fixes the carrier as ℕ so that `#tᵢ ∈ ℕ` at the ancestor-descendant nesting step"), as do T10a.8 and T10a-N. T10a.3 standalone breaks this per-step citation convention.
**What needs resolving**: The standalone T10a.3 Formal Contract should cite T0 among its dependencies with a justification parallel to T10a.5 / T10a.8 / T10a-N — or the main contract's T10a.3 entry and the other NAT-* users should collectively explain why T10a.3 uniquely does not need the T0 citation at its standalone level.

## Result

Cone converged after 2 cycles.

*Elapsed: 934s*
