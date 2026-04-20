module CarrierSetDefinition {
  // T0 — CarrierSetDefinition
  // T = {d₁.d₂. ... .dₙ : each dᵢ ∈ ℕ, n ≥ 1}
  // Axiom: T is the set of all finite sequences over ℕ with length ≥ 1;
  // ℕ is closed under successor and addition.

  datatype Tumbler = Tumbler(components: seq<nat>)

  ghost predicate ValidTumbler(t: Tumbler) {
    |t.components| >= 1
  }
}
