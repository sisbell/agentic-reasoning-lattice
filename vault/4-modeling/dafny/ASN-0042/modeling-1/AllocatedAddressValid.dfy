include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// O17 — AllocatedAddressValid
// (A Σ, a : a ∈ Σ.alloc ⟹ T4(a))
module AllocatedAddressValid {
  import opened TumblerAlgebra
  import TumblerHierarchy

  datatype State = State(alloc: set<Tumbler>)

  // O17 — AllocatedAddressValid
  ghost predicate AllocatedAddressValid(s: State) {
    forall a :: a in s.alloc ==> TumblerHierarchy.ValidAddress(a)
  }
}
