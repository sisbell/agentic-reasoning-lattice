include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangeOps {
  import opened TumblerAlgebra
  import opened Foundation

  // Shared REARRANGE operations on seq-based V-space.

  // --- Cut validity predicates ---

  predicate ValidPivotCuts(c1: nat, c2: nat, c3: nat, n: nat) {
    1 <= c1 && c1 < c2 && c2 < c3 && c3 <= n + 1
  }

  predicate ValidSwapCuts(c1: nat, c2: nat, c3: nat, c4: nat, n: nat) {
    1 <= c1 && c1 < c2 && c2 < c3 && c3 < c4 && c4 <= n + 1
  }

  // --- Concrete rearrange operations ---

  // Pivot rearrange (m = 3): swaps adjacent blocks [c1,c2) and [c2,c3)
  function PivotRearrangeV(v: seq<IAddr>, c1: nat, c2: nat, c3: nat): (v': seq<IAddr>)
    requires ValidPivotCuts(c1, c2, c3, |v|)
    ensures |v'| == |v|
  {
    v[..c1-1] + v[c2-1..c3-1] + v[c1-1..c2-1] + v[c3-1..]
  }

  // Swap rearrange (m = 4): reverses order of blocks [c1,c2), [c2,c3), [c3,c4)
  function SwapRearrangeV(v: seq<IAddr>, c1: nat, c2: nat, c3: nat, c4: nat): (v': seq<IAddr>)
    requires ValidSwapCuts(c1, c2, c3, c4, |v|)
    ensures |v'| == |v|
  {
    v[..c1-1] + v[c3-1..c4-1] + v[c2-1..c3-1] + v[c1-1..c2-1] + v[c4-1..]
  }
}
