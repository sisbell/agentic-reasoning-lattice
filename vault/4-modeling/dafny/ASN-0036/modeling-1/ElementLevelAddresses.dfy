include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// S7b — ElementLevelAddresses
module ElementLevelAddresses {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Val(==)

  datatype State = State(C: map<Tumbler, Val>)

  // S7b — ElementLevelAddresses
  // (A a ∈ dom(Σ.C) :: zeros(a) = 3)
  ghost predicate ElementLevelAddresses(s: State) {
    forall a :: a in s.C ==>
      TumblerHierarchy.ZeroCount(a.components) == 3
  }
}
