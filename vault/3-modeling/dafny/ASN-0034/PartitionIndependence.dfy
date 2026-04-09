include "./CarrierSetDefinition.dfy"

module PartitionIndependence {
  // T10 — PartitionIndependence
  // For non-nesting prefixes p₁ ⋠ p₂ ∧ p₂ ⋠ p₁,
  // any tumbler extending p₁ is distinct from any tumbler extending p₂.

  import opened CarrierSetDefinition

  ghost predicate IsPrefix(p: Tumbler, q: Tumbler) {
    |p.components| <= |q.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == q.components[i]
  }

  lemma PartitionIndependence(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
    requires IsPrefix(p1, a) && IsPrefix(p2, b)
    ensures a != b
  {
  }
}
