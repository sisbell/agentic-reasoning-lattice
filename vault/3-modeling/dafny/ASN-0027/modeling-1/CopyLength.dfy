include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CopyLength {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A4.length — CopyLength (POST, ensures)
  // |Σ'.V(d_t)| = n_{d_t} + k

  // COPY on seq-based V-space: insert source addresses into target
  function CopyV(v_s: seq<IAddr>, p_s: nat, v_t: seq<IAddr>, p_t: nat, k: nat): (v_t': seq<IAddr>)
    requires k >= 1
    requires 1 <= p_s
    requires p_s + k - 1 <= |v_s|
    requires 1 <= p_t <= |v_t| + 1
    ensures |v_t'| == |v_t| + k
  {
    v_t[..p_t-1] + v_s[p_s-1..p_s-1+k] + v_t[p_t-1..]
  }
}
