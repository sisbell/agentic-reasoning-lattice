include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module DocSetUnchanged {
  import opened Foundation

  // ASN-0030 A4(g) — DocSetUnchanged (FRAME, ensures)
  // DELETE
  // Σ'.D = Σ.D
  // Frame condition: DELETE(d, p, k) does not add or remove documents.
  ghost predicate DocSetUnchanged(s: State, s': State) {
    s'.docs == s.docs
  }
}
