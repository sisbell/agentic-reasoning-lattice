include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteContentPersists {
  import opened Foundation

  // ASN-0030 A4(b) — DeleteContentPersists (LEMMA, lemma)
  // derived from A4(a)
  //
  // (A j : p ≤ j < p + k :
  //     let a = Σ.V(d)(j) :
  //     a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))
  //
  // Follows from A4(a) (Σ'.I = Σ.I) and J0 (V-space refs are allocated).

  lemma DeleteContentPersists(
    s: State, s': State, d: DocId, p: nat, k: nat
  )
    requires WellFormed(s)
    requires d in s.docs
    requires k >= 1 && p >= 1
    requires p + k - 1 <= TextCount(s, d)
    // A4(a): I-space unchanged
    requires s'.iota == s.iota
    // DIVERGENCE: positions in deleted range are required explicitly rather
    // than derived from J1 + range bounds. J1 establishes TextOrdinals ==
    // RangeSet(TextCount), but the solver cannot automatically connect
    // membership in that set comprehension back to TextPos(j) in s.vmap[d].
    requires forall j :: p <= j < p + k ==> TextPos(j) in s.vmap[d]
    ensures forall j :: p <= j < p + k ==>
      s.vmap[d][TextPos(j)] in Allocated(s') &&
      s'.iota[s.vmap[d][TextPos(j)]] == s.iota[s.vmap[d][TextPos(j)]]
  { }
}
