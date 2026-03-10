include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteCrossDocFrame {
  import opened Foundation

  // ASN-0027 A2.frame-doc — DeleteCrossDocFrame (FRAME, ensures)
  // (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))

  ghost predicate DeleteCrossDocFrame(s: State, s': State, d: DocId) {
    forall d' :: d' in s.docs && d' != d && d' in s.vmap ==>
      d' in s'.vmap && s'.vmap[d'] == s.vmap[d']
  }
}
