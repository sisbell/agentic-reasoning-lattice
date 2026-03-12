include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteRightShift {
  import opened Foundation

  // ASN-0030 A4(e) — DeleteRightShift (POST, ensures)
  // (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))
  // symmetric to P9-right (reversed)

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // A4(e): after DELETE(d, p, k), positions p+k..n_d shift left by k
  lemma DeleteRightShift(v: seq<IAddr>, p: nat, k: nat)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures var v' := DeleteV(v, p, k);
            forall j {:trigger v'[j - k - 1]} :: p + k <= j <= |v| ==> v'[j - k - 1] == v[j - 1]
  { }
}
