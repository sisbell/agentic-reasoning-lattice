include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/CrossDocVIndependent.dfy"

module DeleteCrossDocFrame {
  import opened Foundation
  import CrossDocVIndependent

  // ASN-0027 A2.frame-doc — DeleteCrossDocFrame (FRAME, ensures)
  // (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))

  ghost predicate DeleteCrossDocFrame(s: State, s': State, d: DocId) {
    CrossDocVIndependent.CrossDocVIndependent(s, s', d)
  }
}
