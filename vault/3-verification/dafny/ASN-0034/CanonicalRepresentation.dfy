include "./CarrierSetDefinition.dfy"

module CanonicalRepresentation {
  // T3 — CanonicalRepresentation
  // (A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)
  // Axiom: Tumbler equality is sequence equality — no quotient,
  // normalization, or external identification is imposed on T.
  // Trailing zeros are significant: [1, 2] ≠ [1, 2, 0].

  import opened CarrierSetDefinition

  // Dafny datatype equality is structural: this axiom holds by construction.
  lemma CanonicalRepresentation(a: Tumbler, b: Tumbler)
    ensures (a == b) <==>
            (|a.components| == |b.components| &&
             forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i])
  { }
}
