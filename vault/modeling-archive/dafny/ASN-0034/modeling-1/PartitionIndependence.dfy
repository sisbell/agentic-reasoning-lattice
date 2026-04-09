include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T10 — PartitionIndependence (derived from T3)
module PartitionIndependence {
  import opened TumblerAlgebra

  ghost predicate NonNesting(p1: Tumbler, p2: Tumbler) {
    !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
  }

  lemma PartitionIndependence(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires NonNesting(p1, p2)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures a != b
  { }
}
