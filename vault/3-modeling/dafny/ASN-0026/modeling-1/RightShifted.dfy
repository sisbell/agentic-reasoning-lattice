include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "InsertOps.dfy"

module RightShifted {
  import opened Foundation
  import opened InsertOps

  // ASN-0026 P9 (right) — RightShifted (FRAME, ensures)
  // After Insert(d, p, k), positions at and after the insertion point shift right by k:
  //   (A j : p <= j <= n_d : Sigma'.V(d)(j + k) = Sigma.V(d)(j))

  lemma RightShifted(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures var v' := InsertV(v, p, k, newAddrs);
            forall j {:trigger v'[j+k-1]} :: p <= j <= |v| ==> v'[j+k-1] == v[j-1]
  { }
}
