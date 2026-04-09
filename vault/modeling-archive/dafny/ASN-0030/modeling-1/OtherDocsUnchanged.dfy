include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/TwoSpace/CrossDocVIndependent.dfy"

module OtherDocsUnchanged {
  import opened Foundation
  import CrossDocVIndependent

  // ASN-0030 A4(f) — OtherDocsUnchanged (FRAME, ensures)
  // DELETE; instance of P7
  // (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
  // Frame condition: DELETE(d, p, k) leaves all other documents' V-spaces unchanged.
  ghost predicate OtherDocsUnchanged(s: State, s': State, d: DocId) {
    CrossDocVIndependent.CrossDocVIndependent(s, s', d)
  }
}
