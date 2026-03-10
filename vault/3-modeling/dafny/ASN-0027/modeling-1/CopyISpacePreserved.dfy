include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module CopyISpacePreserved {
  import opened Foundation

  // ASN-0027 A4.frame-I — CopyISpacePreserved (FRAME, ensures)
  // instance of A1
  // Σ'.I = Σ.I
  predicate CopyISpacePreserved(s: State, s': State) {
    s'.iota == s.iota
  }
}
