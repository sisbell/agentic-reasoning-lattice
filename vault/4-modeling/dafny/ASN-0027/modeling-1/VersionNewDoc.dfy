include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module VersionNewDoc {
  import opened Foundation

  // ASN-0027 A5.new — VersionNewDoc (POST, ensures)
  // d' in Sigma'.D and d' not in Sigma.D
  ghost predicate VersionNewDoc(s: State, s': State, d': DocId) {
    d' in s'.docs && d' !in s.docs
  }
}
