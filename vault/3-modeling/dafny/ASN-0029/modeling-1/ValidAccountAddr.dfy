include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"

module ValidAccountAddr {
  import opened TumblerAlgebra
  import HierarchicalParsing

  // ASN-0029 AccountAddr — ValidAccountAddr (INV, predicate(Tumbler))
  // AccountAddr = {a ∈ T : zeros(a) = 1}
  // Account addresses are tumblers with exactly one zero separator (form N.0.U).
  predicate ValidAccountAddr(t: Tumbler) {
    HierarchicalParsing.CountZeros(t.components) == 1
  }
}
