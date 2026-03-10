include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteLeftFrame {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A2.left — DeleteLeftFrame (FRAME, ensures)
  // (A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // A2.left: positions left of the deletion point are preserved
  lemma DeleteLeftFrameLemma(v: seq<IAddr>, p: nat, k: nat)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures var v' := DeleteV(v, p, k);
            forall j {:trigger v'[j-1]} :: 1 <= j < p ==> v'[j-1] == v[j-1]
  { }
}
