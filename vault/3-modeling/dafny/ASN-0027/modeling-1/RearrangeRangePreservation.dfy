include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "RearrangeOps.dfy"

module RearrangeRangePreservation {
  import opened TumblerAlgebra
  import opened Foundation
  import opened RearrangeOps

  // ASN-0027 A3.range — RearrangeRangePreservation (LEMMA, lemma)
  // range(Σ'.V(d)) = range(Σ.V(d))
  // Derived from A3.perm: a bijection preserves the multiset of values, hence the range.

  // Range of a V-space sequence: set of addresses appearing in it
  function SeqRange(v: seq<IAddr>): set<IAddr> {
    set i | 0 <= i < |v| :: v[i]
  }

  // --- A3.range: Range preservation ---

  // Pivot case (m = 3): v' = v[..c1-1] + v[c2-1..c3-1] + v[c1-1..c2-1] + v[c3-1..]
  lemma PivotRangePreservation(v: seq<IAddr>, c1: nat, c2: nat, c3: nat)
    requires ValidPivotCuts(c1, c2, c3, |v|)
    ensures SeqRange(PivotRearrangeV(v, c1, c2, c3)) == SeqRange(v)
  {
    var v' := PivotRearrangeV(v, c1, c2, c3);
    // Every element of v appears in v' (inverse mapping)
    forall j | 0 <= j < |v|
      ensures v[j] in SeqRange(v')
    {
      if j < c1 - 1 {
        assert v'[j] == v[j];
      } else if j < c2 - 1 {
        assert v'[j + (c3 - c2)] == v[j];
      } else if j < c3 - 1 {
        assert v'[j - (c2 - c1)] == v[j];
      } else {
        assert v'[j] == v[j];
      }
    }
  }

  // Swap case (m = 4): v' = v[..c1-1] + v[c3-1..c4-1] + v[c2-1..c3-1] + v[c1-1..c2-1] + v[c4-1..]
  lemma SwapRangePreservation(v: seq<IAddr>, c1: nat, c2: nat, c3: nat, c4: nat)
    requires ValidSwapCuts(c1, c2, c3, c4, |v|)
    ensures SeqRange(SwapRearrangeV(v, c1, c2, c3, c4)) == SeqRange(v)
  {
    var v' := SwapRearrangeV(v, c1, c2, c3, c4);
    // Every element of v appears in v' (inverse mapping)
    forall j | 0 <= j < |v|
      ensures v[j] in SeqRange(v')
    {
      if j < c1 - 1 {
        assert v'[j] == v[j];
      } else if j < c2 - 1 {
        assert v'[j + (c4 - c2)] == v[j];
      } else if j < c3 - 1 {
        assert v'[j + (c4 - c3) - (c2 - c1)] == v[j];
      } else if j < c4 - 1 {
        assert v'[j - (c3 - c1)] == v[j];
      } else {
        assert v'[j] == v[j];
      }
    }
  }
}
