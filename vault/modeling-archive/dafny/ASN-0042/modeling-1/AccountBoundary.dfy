include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// O1a — AccountBoundary
// (A π ∈ Π : zeros(pfx(π)) ≤ 1)
module AccountBoundary {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  // State: the set of active principals
  datatype State = State(principals: set<Principal>)

  // O1a: every principal's prefix has at most one zero separator
  ghost predicate AccountBoundary(s: State) {
    forall pi :: pi in s.principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1
  }
}
