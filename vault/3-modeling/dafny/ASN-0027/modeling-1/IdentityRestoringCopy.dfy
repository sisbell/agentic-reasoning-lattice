include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/InsertOps.dfy"

module IdentityRestoringCopyModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened InsertOps

  // ASN-0027 A7 — IdentityRestoringCopy (LEMMA, lemma)
  // derived from A2, A4

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // A7: DELETE followed by COPY from a document that retains the original
  // addresses restores the identity. COPY reuses existing I-space addresses
  // (identity sharing, A4.identity), so the restored positions point to
  // the same content as before the DELETE.
  lemma IdentityRestoringCopy(
    v0: seq<IAddr>,     // Σ_0.V(d)
    vPrime: seq<IAddr>, // Σ_1.V(d') — retains the deleted addresses
    p: nat,             // position in d (1-indexed)
    k: nat,             // span length
    q: nat              // source position in d' (1-indexed)
  )
    requires 1 <= p && k >= 1 && p + k - 1 <= |v0|
    requires 1 <= q && q + k - 1 <= |vPrime|
    // d' holds the original addresses: slice equality
    requires vPrime[q-1..q-1+k] == v0[p-1..p-1+k]
    ensures
      var v1 := DeleteV(v0, p, k);
      var v2 := InsertV(v1, p, k, vPrime[q-1..q-1+k]);
      forall j {:trigger v2[p-1+j]} :: 0 <= j < k ==> v2[p-1+j] == v0[p-1+j]
  {
    var v1 := DeleteV(v0, p, k);
    var copied := vPrime[q-1..q-1+k];
    var v2 := InsertV(v1, p, k, copied);
    assert v2 == v1[..p-1] + copied + v1[p-1..];
  }
}
