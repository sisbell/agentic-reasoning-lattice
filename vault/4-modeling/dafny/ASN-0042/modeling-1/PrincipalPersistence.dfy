include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"

// O12 — PrincipalPersistence
// (A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})
module PrincipalPersistence {
  import opened TumblerAlgebra
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  // O12 — PrincipalPersistence
  ghost predicate PrincipalPersistence(s: State, s': State) {
    s.principals <= s'.principals
  }
}
