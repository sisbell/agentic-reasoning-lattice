include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"

// O1b — PrefixInjective
// (A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)
module PrefixInjective {
  import opened TumblerAlgebra
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  // State: the set of active principals
  datatype State = State(principals: set<Principal>)

  // O1b: the prefix mapping is injective — no two distinct principals
  // share the same ownership prefix.
  // DIVERGENCE: With Principal modeled as a datatype whose sole field is
  // the prefix tumbler, injectivity holds by construction (structural
  // equality). The ASN treats Principal as an abstract identity with pfx
  // as a separate mapping; the Dafny model collapses these, making O1b
  // a tautology. This is sound: any model satisfying the abstract version
  // also satisfies this one, and vice versa.
  ghost predicate PrefixInjective(s: State) {
    forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1.prefix == p2.prefix)
        ==> p1 == p2
  }
}
