include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module IsInitialState {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // State with all four components for initial-state predicate
  datatype State = State(
    C: map<Tumbler, nat>,                       // content
    E: set<Tumbler>,                            // entities
    M: map<Tumbler, map<Tumbler, Tumbler>>,     // arrangements
    R: set<(Tumbler, Tumbler)>                  // provenance
  )

  // ---------------------------------------------------------------------------
  // Σ₀ — IsInitialState
  //
  // The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:
  //   C₀ = ∅
  //   E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
  //   M₀(d) = ∅ for all d
  //   R₀ = ∅
  // ---------------------------------------------------------------------------

  ghost predicate IsInitialState(s: State) {
    s.C == map[] &&
    |s.E| == 1 &&
    (forall e :: e in s.E ==> TumblerHierarchy.NodeAddress(e)) &&
    s.M == map[] &&
    s.R == {}
  }
}
