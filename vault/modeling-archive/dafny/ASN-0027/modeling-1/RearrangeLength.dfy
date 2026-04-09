include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "RearrangeOps.dfy"

module RearrangeLength {
  import opened TumblerAlgebra
  import opened Foundation
  import opened RearrangeOps

  // ASN-0027 A3.length — RearrangeLength (POST, ensures)
  // |Σ'.V(d)| = n_d
  // Established by ensures clauses on PivotRearrangeV and SwapRearrangeV.
}
