include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// B6 — ValidDepth
module ValidDepth {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // B6 — ValidDepth (PRE, requires) — on baptize
  // Baptism at depth d from parent p is valid iff:
  //   (i)   p satisfies T4
  //   (ii)  d ∈ {1, 2}
  //   (iii) zeros(p) + (d − 1) ≤ 3
  predicate ValidBaptismDepth(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    (d == 1 || d == 2) &&
    TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
  }
}
