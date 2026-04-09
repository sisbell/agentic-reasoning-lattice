include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "RearrangeOps.dfy"

module RearrangePermutation {
  import opened TumblerAlgebra
  import opened Foundation
  import opened RearrangeOps

  // ASN-0027 A3.perm — RearrangePermutation (POST, ensures)
  // (A j : 1 ≤ j ≤ n_d : Σ'.V(d)(σ(j)) = Σ.V(d)(j))

  // --- Sigma bijections (1-indexed) ---

  // RearrangeBijectionPivot (m = 3)
  function PivotSigma(c1: nat, c2: nat, c3: nat, j: nat): nat
    requires 1 <= c1 && c1 < c2 && c2 < c3 && j >= 1
  {
    if c1 <= j && j < c2 then j + (c3 - c2)
    else if c2 <= j && j < c3 then j - (c2 - c1)
    else j
  }

  // RearrangeBijectionSwap (m = 4)
  function SwapSigma(c1: nat, c2: nat, c3: nat, c4: nat, j: nat): nat
    requires 1 <= c1 && c1 < c2 && c2 < c3 && c3 < c4 && j >= 1
  {
    if c1 <= j && j < c2 then j + (c4 - c2)
    else if c2 <= j && j < c3 then j + (c4 - c3) - (c2 - c1)
    else if c3 <= j && j < c4 then j - (c3 - c1)
    else j
  }

  // --- A3.perm: Permutation postcondition ---

  // Pivot case (m = 3)
  lemma PivotPermutation(v: seq<IAddr>, c1: nat, c2: nat, c3: nat)
    requires ValidPivotCuts(c1, c2, c3, |v|)
    ensures var v' := PivotRearrangeV(v, c1, c2, c3);
            forall j :: 1 <= j <= |v| ==>
              v'[PivotSigma(c1, c2, c3, j) - 1] == v[j - 1]
  { }

  // Swap case (m = 4)
  lemma SwapPermutation(v: seq<IAddr>, c1: nat, c2: nat, c3: nat, c4: nat)
    requires ValidSwapCuts(c1, c2, c3, c4, |v|)
    ensures var v' := SwapRearrangeV(v, c1, c2, c3, c4);
            forall j :: 1 <= j <= |v| ==>
              v'[SwapSigma(c1, c2, c3, c4, j) - 1] == v[j - 1]
  { }
}
