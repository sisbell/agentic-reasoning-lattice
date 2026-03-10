include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteCompaction {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A2.compact — DeleteCompaction (POST, ensures)
  // (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // A2.compact: positions beyond the deleted range compact leftward by k
  lemma DeleteCompactionLemma(v: seq<IAddr>, p: nat, k: nat)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures var v' := DeleteV(v, p, k);
            forall j {:trigger v'[j-k-1]} :: p + k <= j <= |v| ==> v'[j - k - 1] == v[j - 1]
  { }
}
