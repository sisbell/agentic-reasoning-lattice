include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/CrossDocVIndependent.dfy"

module CopyCrossDocFrame {
  import opened Foundation
  import CrossDocVIndependent

  // ASN-0027 A4.frame-doc — CopyCrossDocFrame (FRAME, ensures)
  // (A d' : d' ∈ Σ.D ∧ d' ≠ d_t : Σ'.V(d') = Σ.V(d'))

  ghost predicate CopyCrossDocFrame(s: State, s': State, d_t: DocId) {
    CrossDocVIndependent.CrossDocVIndependent(s, s', d_t)
  }
}
