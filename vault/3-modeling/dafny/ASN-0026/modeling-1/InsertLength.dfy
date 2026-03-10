include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module InsertLength {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0026 P9 (length) — InsertLength (POST, ensures)
  // After Insert(d, p, k): |Sigma'.V(d)| = n_d + k

  // V-space for a document modeled as seq<IAddr> of length n_d.
  // Under WellFormed / J1, Foundation's vmap[d] on TextPos(1..n_d)
  // is isomorphic to this representation.

  function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): seq<IAddr>
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures |InsertV(v, p, k, newAddrs)| == |v| + k
  {
    v[..p-1] + newAddrs + v[p-1..]
  }
}
