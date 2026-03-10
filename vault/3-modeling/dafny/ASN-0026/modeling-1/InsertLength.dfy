include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "InsertOps.dfy"

module InsertLength {
  import opened Foundation
  import opened InsertOps

  // ASN-0026 P9 (length) — InsertLength (POST, ensures)
  // After Insert(d, p, k): |Sigma'.V(d)| = n_d + k

  lemma InsertLength(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures |InsertV(v, p, k, newAddrs)| == |v| + k
  { }
}
