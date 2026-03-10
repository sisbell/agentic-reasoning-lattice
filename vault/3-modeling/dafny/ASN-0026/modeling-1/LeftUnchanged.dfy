include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "InsertOps.dfy"

module LeftUnchanged {
  import opened Foundation
  import opened InsertOps

  // ASN-0026 P9 (left) — LeftUnchanged (FRAME, ensures)
  // After Insert(d, p, k), positions before the insertion point are unchanged:
  //   (A j : 1 <= j < p : Sigma'.V(d)(j) = Sigma.V(d)(j))

  lemma LeftUnchanged(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures var v' := InsertV(v, p, k, newAddrs);
            forall j {:trigger v'[j-1]} :: 1 <= j < p ==> v'[j-1] == v[j-1]
  { }
}
