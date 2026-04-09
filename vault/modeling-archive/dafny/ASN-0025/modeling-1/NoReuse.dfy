include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module NoReuseModule {
  import opened AddressPermanence
  import opened Foundation

  // P2 — NoReuse (LEMMA)
  // Derived from P0 (ISpaceGrowth) ∧ P1 (ContentImmutability).
  // (A i, j : 0 ≤ i ≤ j ∧ a ∈ Σᵢ.A : Σⱼ.ι(a) = Σᵢ.ι(a))
  lemma NoReuse(trace: seq<State>, i: nat, j: nat, a: IAddr)
    requires forall k :: 0 <= k < |trace| - 1 ==>
      forall b :: b in Allocated(trace[k]) ==>
        b in Allocated(trace[k+1]) &&                             // P0
        trace[k+1].iota[b] == trace[k].iota[b]                   // P1
    requires 0 <= i <= j < |trace|
    requires a in Allocated(trace[i])
    ensures a in Allocated(trace[j])
    ensures trace[j].iota[a] == trace[i].iota[a]
    decreases j - i
  {
    if i < j {
      NoReuse(trace, i + 1, j, a);
    }
  }
}
