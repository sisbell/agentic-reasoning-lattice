include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CopyRightShift {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A4.right — CopyRightShift (POST, ensures)
  // (A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))

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

  // A4.right: positions at or beyond the insertion point shift right by k
  lemma CopyRightShiftLemma(v_s: seq<IAddr>, p_s: nat, v_t: seq<IAddr>, p_t: nat, k: nat)
    requires k >= 1
    requires 1 <= p_s
    requires p_s + k - 1 <= |v_s|
    requires 1 <= p_t <= |v_t| + 1
    ensures var v_t' := CopyV(v_s, p_s, v_t, p_t, k);
            forall j {:trigger v_t'[j+k-1]} :: p_t <= j <= |v_t| ==> v_t'[j+k-1] == v_t[j-1]
  { }
}
