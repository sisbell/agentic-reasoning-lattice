include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module VersionISpacePreserved {
  import opened Foundation

  // ASN-0027 A5.frame-I — VersionISpacePreserved (FRAME, ensures)
  // instance of A1
  // Σ'.I = Σ.I
  predicate VersionISpacePreserved(s: State, s': State) {
    s'.iota == s.iota
  }
}
