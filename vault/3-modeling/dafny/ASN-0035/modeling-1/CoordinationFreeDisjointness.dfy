include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

module CoordinationFreeDisjointness {
  import opened TumblerAlgebra
  import TumblerAllocation

  // N11 — CoordinationFreeDisjointness
  // Two allocators under distinct, non-nesting prefixes produce
  // pairwise-disjoint outputs without inter-allocator communication.
  // Direct application of PartitionIndependence (T10b, ASN-0034).
  lemma CoordinationFreeDisjointness(
    p: Tumbler, q: Tumbler,
    outputs_p: seq<Tumbler>, outputs_q: seq<Tumbler>
  )
    requires TumblerAllocation.NonNesting(p, q)
    requires TumblerAllocation.AllExtend(outputs_p, p)
    requires TumblerAllocation.AllExtend(outputs_q, q)
    ensures forall i, j :: 0 <= i < |outputs_p| && 0 <= j < |outputs_q|
              ==> outputs_p[i] != outputs_q[j]
  { }
}
