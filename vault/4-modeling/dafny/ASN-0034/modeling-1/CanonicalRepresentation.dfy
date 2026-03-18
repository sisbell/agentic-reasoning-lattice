include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module CanonicalRepresentation {

  import opened TumblerAlgebra

  // T3: CanonicalRepresentation
  // (A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)

  // Component-wise equality: same length and same value at every position
  ghost predicate ComponentEqual(a: Tumbler, b: Tumbler) {
    |a.components| == |b.components| &&
    forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i]
  }

  // T3: structural equality from datatype — component-wise equality is identity
  lemma CanonicalRepresentation(a: Tumbler, b: Tumbler)
    ensures ComponentEqual(a, b) <==> a == b
  { }
}
