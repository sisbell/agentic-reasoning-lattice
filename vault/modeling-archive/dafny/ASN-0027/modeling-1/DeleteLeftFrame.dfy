include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "DeleteOps.dfy"

module DeleteLeftFrame {
  import opened TumblerAlgebra
  import opened Foundation
  import opened DeleteOps

  // ASN-0027 A2.left — DeleteLeftFrame (FRAME, ensures)
  // (A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))

  // A2.left: positions left of the deletion point are preserved
  lemma DeleteLeftFrameLemma(v: seq<IAddr>, p: nat, k: nat)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures var v' := DeleteV(v, p, k);
            forall j {:trigger v'[j-1]} :: 1 <= j < p ==> v'[j-1] == v[j-1]
  { }
}
