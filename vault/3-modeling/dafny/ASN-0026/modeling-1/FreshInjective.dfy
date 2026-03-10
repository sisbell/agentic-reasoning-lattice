include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "InsertOps.dfy"

module FreshInjective {
  import opened Foundation
  import opened InsertOps

  // ASN-0026 P9 (inj) — FreshInjective (POST, ensures)
  // (A j_1, j_2 : p <= j_1 < j_2 < p + k : Sigma'.V(d)(j_1) =/= Sigma'.V(d)(j_2))
  //
  // After INSERT(d, p, k) with injective fresh addresses, positions
  // [p, p+k) in the post-state map to distinct I-addresses.
  // The injectivity of newAddrs follows from CreationBasedIdentity (P4):
  // distinct allocation acts produce distinct addresses.

  lemma FreshInjective(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    requires forall i, j :: 0 <= i < j < k ==> newAddrs[i] != newAddrs[j]
    ensures var v' := InsertV(v, p, k, newAddrs);
            forall j1, j2 {:trigger v'[j1-1], v'[j2-1]} :: p <= j1 < j2 < p + k ==> v'[j1-1] != v'[j2-1]
  { }
}
