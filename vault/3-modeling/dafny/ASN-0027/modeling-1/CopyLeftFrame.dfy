include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "CopyOps.dfy"

module CopyLeftFrame {
  import opened TumblerAlgebra
  import opened Foundation
  import opened CopyOps

  // ASN-0027 A4.left — CopyLeftFrame (FRAME, ensures)
  // (A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))

  // A4.left: positions left of the insertion point are preserved
  lemma CopyLeftFrameLemma(v_s: seq<IAddr>, p_s: nat, v_t: seq<IAddr>, p_t: nat, k: nat)
    requires k >= 1
    requires 1 <= p_s
    requires p_s + k - 1 <= |v_s|
    requires 1 <= p_t <= |v_t| + 1
    ensures var v_t' := CopyV(v_s, p_s, v_t, p_t, k);
            forall j {:trigger v_t'[j-1]} :: 1 <= j < p_t ==> v_t'[j-1] == v_t[j-1]
  { }
}
