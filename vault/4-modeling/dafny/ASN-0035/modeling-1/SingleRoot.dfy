include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// N2 — SingleRoot
module SingleRoot {
  import opened TumblerAlgebra

  datatype State = State(nodes: set<Tumbler>)

  const Root: Tumbler := Tumbler([1])

  // N2 — SingleRoot
  // The root [1] is in every reachable state, and every other baptized
  // node descends from it.
  ghost predicate SingleRoot(state: State) {
    Root in state.nodes &&
    forall n :: n in state.nodes && n != Root ==> IsPrefix(Root, n)
  }
}
