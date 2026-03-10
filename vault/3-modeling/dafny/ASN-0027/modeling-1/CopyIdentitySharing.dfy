include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CopyIdentitySharing {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A4.identity — CopyIdentitySharing (POST, ensures)
  // (A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))

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

  // A4.identity: after Copy, target positions [p_t, p_t+k) share source addresses
  lemma CopyIdentitySharingLemma(v_s: seq<IAddr>, p_s: nat, v_t: seq<IAddr>, p_t: nat, k: nat)
    requires k >= 1
    requires 1 <= p_s
    requires p_s + k - 1 <= |v_s|
    requires 1 <= p_t <= |v_t| + 1
    ensures var v_t' := CopyV(v_s, p_s, v_t, p_t, k);
            forall j {:trigger v_t'[p_t + j - 1]} :: 0 <= j < k ==> v_t'[p_t + j - 1] == v_s[p_s + j - 1]
  { }
}
