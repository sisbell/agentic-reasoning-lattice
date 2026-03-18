include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"
include "OwnershipDelegation.dfy"

// O15 — PrincipalClosure
module PrincipalClosure {
  import opened TumblerAlgebra
  import PrefixDetermination
  import OD = OwnershipDelegation

  type Principal = PrefixDetermination.Principal

  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  // O15 — PrincipalClosure
  // (A Sigma, Sigma' : Sigma -> Sigma' ==> |Pi_{Sigma'} \ Pi_Sigma| <= 1)
  // (A pi' in Pi_{Sigma'} \ Pi_Sigma : (E pi in Pi_Sigma : delegated_Sigma(pi, pi')))
  ghost predicate PrincipalClosure(s: State, s': State) {
    |s'.principals - s.principals| <= 1 &&
    (forall pi' :: pi' in s'.principals - s.principals ==>
      exists pi :: pi in s.principals &&
        OD.DelegationPrecondition(OD.State(s.principals, s.alloc), pi, pi'))
  }
}
