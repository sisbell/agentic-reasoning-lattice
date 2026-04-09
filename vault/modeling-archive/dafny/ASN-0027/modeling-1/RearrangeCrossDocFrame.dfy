include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/CrossDocVIndependent.dfy"

module RearrangeCrossDocFrame {
  import opened Foundation
  import CrossDocVIndependent

  // ASN-0027 A3.frame-doc — RearrangeCrossDocFrame (FRAME, ensures)
  // P7 (cross-document frame): (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))

  ghost predicate RearrangeCrossDocFrame(s: State, s': State, d: DocId) {
    CrossDocVIndependent.CrossDocVIndependent(s, s', d)
  }
}
