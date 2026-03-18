include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangeISpacePreserved {
  import opened Foundation

  // ASN-0027 A3.frame-I — RearrangeISpacePreserved (FRAME, ensures)
  // instance of A1
  // Σ'.I = Σ.I
  predicate RearrangeISpacePreserved(s: State, s': State) {
    s'.iota == s.iota
  }
}
