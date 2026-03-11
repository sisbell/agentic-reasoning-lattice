include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "DeleteOps.dfy"

module DeleteCompaction {
  import opened TumblerAlgebra
  import opened Foundation
  import opened DeleteOps

  // ASN-0027 A2.compact — DeleteCompaction (POST, ensures)
  // (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))

  // A2.compact: positions beyond the deleted range compact leftward by k
  lemma DeleteCompactionLemma(v: seq<IAddr>, p: nat, k: nat)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures var v' := DeleteV(v, p, k);
            forall j {:trigger v'[j-k-1]} :: p + k <= j <= |v| ==> v'[j - k - 1] == v[j - 1]
  { }
}
