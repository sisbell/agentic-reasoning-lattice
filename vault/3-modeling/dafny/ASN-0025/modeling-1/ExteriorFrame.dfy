include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module ExteriorFrameModule {
  import opened AddressPermanence
  import opened Foundation

  // Exterior frame — ExteriorFrame (FRAME, ensures)
  // Applies to REARRANGE. Cut positions c₁ < c₂ < ... < cₖ are text-subspace
  // V-positions; k ∈ {3, 4}.
  // (A q : q ∈ dom(Σ.v(d)) ∧ q is a text position ∧ (q < c₁ ∨ q ≥ cₖ) :
  //   Σ'.v(d)(q) = Σ.v(d)(q))

  // Valid cut sequence: all text positions with positive ordinals, strictly sorted
  predicate ValidCuts(cuts: seq<VPos>) {
    (|cuts| == 3 || |cuts| == 4) &&
    (forall i :: 0 <= i < |cuts| ==> IsTextPos(cuts[i]) && ValidVPos(cuts[i])) &&
    (forall i, j :: 0 <= i < j < |cuts| ==> Ord(cuts[i]) < Ord(cuts[j]))
  }

  // A position is exterior to the cut range [c₁, cₖ): before c₁ or at/after cₖ
  predicate Exterior(q: VPos, cuts: seq<VPos>)
    requires |cuts| >= 1
  {
    Ord(q) < Ord(cuts[0]) || Ord(q) >= Ord(cuts[|cuts| - 1])
  }

  ghost predicate ExteriorFrame(s: State, s': State, d: DocId, cuts: seq<VPos>) {
    (d in s.vmap && d in s'.vmap && ValidCuts(cuts)) ==>
      forall q :: q in s.vmap[d] && IsTextPos(q) && Exterior(q, cuts) ==>
        q in s'.vmap[d] && s'.vmap[d][q] == s.vmap[d][q]
  }
}
