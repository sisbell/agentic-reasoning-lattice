include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// E.account — IsAccount (INV, predicate(Tumbler))
module IsAccount {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // E.account: ValidAddress(t) ∧ zeros(t) = 1
  predicate IsAccount(t: Tumbler) {
    TumblerHierarchy.ValidAddress(t) && TumblerHierarchy.ZeroCount(t.components) == 1
  }
}
