include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/InsertOps.dfy"

module FullRestorationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened InsertOps

  // ASN-0027 A7.corollary — FullRestoration (LEMMA, lemma)
  // derived from A7, A2, A4

  // DELETE on seq-based V-space: remove k positions starting at p (1-indexed)
  function DeleteV(v: seq<IAddr>, p: nat, k: nat): (v': seq<IAddr>)
    requires 1 <= p
    requires k >= 1
    requires p + k - 1 <= |v|
    ensures |v'| == |v| - k
  {
    v[..p-1] + v[p+k-1..]
  }

  // FullRestoration: under the A7 setup (DELETE then restoring COPY),
  // the entire document is restored: Σ_2.V(d) = Σ_0.V(d).
  lemma FullRestoration(
    v0: seq<IAddr>,     // Σ_0.V(d) — original document
    vPrime: seq<IAddr>, // Σ_1.V(d') — retains the deleted addresses
    p: nat,             // position in d (1-indexed)
    k: nat,             // span length
    q: nat              // source position in d' (1-indexed)
  )
    requires 1 <= p && k >= 1 && p + k - 1 <= |v0|
    requires 1 <= q && q + k - 1 <= |vPrime|
    // A7 setup: d' holds the original addresses
    requires vPrime[q-1..q-1+k] == v0[p-1..p-1+k]
    ensures
      var v1 := DeleteV(v0, p, k);
      var v2 := InsertV(v1, p, k, vPrime[q-1..q-1+k]);
      v2 == v0
  { }
}
