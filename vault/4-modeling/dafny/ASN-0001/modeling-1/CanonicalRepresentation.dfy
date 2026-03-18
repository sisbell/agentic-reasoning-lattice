include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module CanonicalRepresentation {

  import opened TumblerAlgebra

  // T3 — CanonicalRepresentation
  // (A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)
  // Componentwise agreement with equal length is equivalent to equality.

  ghost predicate ComponentwiseEqual(a: Tumbler, b: Tumbler) {
    |a.components| == |b.components| &&
    forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i]
  }

  lemma CanonicalRepresentation(a: Tumbler, b: Tumbler)
    ensures ComponentwiseEqual(a, b) <==> a == b
  { }
}
