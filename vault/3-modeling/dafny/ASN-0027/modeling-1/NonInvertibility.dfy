include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/InsertOps.dfy"

module NonInvertibilityModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened InsertOps

  // ASN-0027 A6 — NonInvertibility (LEMMA, lemma)
  // derived from A2, ASN-0026

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // Compose delete then insert
  function DeleteThenInsert(
    v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>
  ): seq<IAddr>
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    requires |newAddrs| == k
  {
    InsertV(DeleteV(v, p, k), p, k, newAddrs)
  }

  // Bridge: positions [p-1, p-1+k) in the result hold newAddrs
  lemma DeleteInsertPositions(
    v0: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>, j: nat
  )
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v0|
    requires |newAddrs| == k
    requires 0 <= j < k
    ensures DeleteThenInsert(v0, p, k, newAddrs)[p-1+j] == newAddrs[j]
  {
    var v1 := DeleteV(v0, p, k);
    assert InsertV(v1, p, k, newAddrs) == v1[..p-1] + newAddrs + v1[p-1..];
  }

  // A6: DELETE followed by INSERT at the same position cannot restore the
  // original addresses. INSERT introduces fresh addresses disjoint from
  // dom(Σ_0.I), which contains the original addresses by referential
  // completeness (P2). Therefore the new entries differ from the originals.
  lemma NonInvertibility(
    v0: seq<IAddr>,
    p: nat,
    k: nat,
    newAddrs: seq<IAddr>,
    priorDomain: set<IAddr>
  )
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v0|
    requires |newAddrs| == k
    // Deleted positions were in prior domain (from P2 — referential completeness)
    // Re-indexed so v0[i] serves as trigger for quantifier instantiation
    requires forall i :: p-1 <= i < p+k-1 ==> v0[i] in priorDomain
    // Fresh INSERT addresses are disjoint from prior domain (ISpaceExtension)
    requires SetOf(newAddrs) !! priorDomain
    ensures forall i :: p-1 <= i < p+k-1 ==>
              DeleteThenInsert(v0, p, k, newAddrs)[i] != v0[i]
  {
    forall i | p-1 <= i < p+k-1
      ensures DeleteThenInsert(v0, p, k, newAddrs)[i] != v0[i]
    {
      var j := i - (p - 1);
      DeleteInsertPositions(v0, p, k, newAddrs, j);
      assert newAddrs[j] in SetOf(newAddrs);
    }
  }
}
