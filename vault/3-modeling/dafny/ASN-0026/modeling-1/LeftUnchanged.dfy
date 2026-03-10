include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module LeftUnchanged {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0026 P9 (left) — LeftUnchanged (FRAME, ensures)
  // After Insert(d, p, k), positions before the insertion point are unchanged:
  //   (A j : 1 <= j < p : Sigma'.V(d)(j) = Sigma.V(d)(j))

  // V-space as seq<IAddr>, isomorphic to Foundation's vmap under J1.
  // Position j (1-indexed) corresponds to index j-1.
  function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): (v': seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures |v'| == |v| + k
    ensures forall j {:trigger v'[j-1]} :: 1 <= j < p ==> v'[j-1] == v[j-1]
  {
    v[..p-1] + newAddrs + v[p-1..]
  }
}
