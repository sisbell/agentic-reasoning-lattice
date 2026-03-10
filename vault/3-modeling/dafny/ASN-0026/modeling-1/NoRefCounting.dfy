include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "ISpaceMonotone.dfy"

module NoRefCounting {
  import opened Foundation
  import ISpaceMonotone

  // ASN-0026 P8 — NoRefCounting (LEMMA, lemma)
  // derived from P1 (ISpaceMonotone)
  // dom(Sigma.I) never shrinks, regardless of |refs(a)|.
  // Content persists even when refs(a) = emptyset.
  // The lemma makes no mention of refs — that is the point:
  // P1 guarantees persistence unconditionally.
  lemma NoRefCounting(s: State, s': State, a: IAddr)
    requires ISpaceMonotone.ISpaceMonotone(s, s')
    requires a in Allocated(s)
    ensures a in Allocated(s')
  { }
}
