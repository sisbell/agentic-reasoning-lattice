include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DeleteISpacePreserved {
  import opened Foundation

  // ASN-0027 A2.frame-I — DeleteISpacePreserved (FRAME, ensures)
  // instance of A1
  // Σ'.I = Σ.I
  predicate DeleteISpacePreserved(s: State, s': State) {
    s'.iota == s.iota
  }
}
