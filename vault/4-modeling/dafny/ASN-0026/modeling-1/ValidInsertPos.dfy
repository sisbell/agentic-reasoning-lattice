include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ValidInsertPos {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0026 P9 (pre) — ValidInsertPos (PRE, requires)
  // Insert precondition: 1 <= p <= n_d + 1 and k >= 1

  predicate ValidInsertPos(s: State, d: DocId, p: nat, k: nat)
    requires WellFormed(s)
    requires d in s.docs
  {
    1 <= p <= TextCount(s, d) + 1 &&
    k >= 1
  }
}
