include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangePermutation {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A3.perm — RearrangePermutation (POST, ensures)
  // (A j : 1 ≤ j ≤ n_d : Σ'.V(d)(σ(j)) = Σ.V(d)(j))

  // --- Cut validity predicates ---

  predicate ValidPivotCuts(c1: nat, c2: nat, c3: nat, n: nat) {
    1 <= c1 && c1 < c2 && c2 < c3 && c3 <= n + 1
  }

  predicate ValidSwapCuts(c1: nat, c2: nat, c3: nat, c4: nat, n: nat) {
    1 <= c1 && c1 < c2 && c2 < c3 && c3 < c4 && c4 <= n + 1
  }

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

  // --- Rearrange operations on V-space ---

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
