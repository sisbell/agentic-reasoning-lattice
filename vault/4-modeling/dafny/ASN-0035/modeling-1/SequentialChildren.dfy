include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SequentialChildren {
  import opened TumblerAlgebra

  datatype State = State(nodes: set<Tumbler>)

  // N5 — SequentialChildren
  // For children(p) = {c₁, ..., cₖ} ordered by T1:
  // (A i : 1 ≤ i ≤ k : (cᵢ)_{#cᵢ} = i)
  //
  // Children share their parent's prefix and differ only in their last
  // component, so T1 ordering coincides with last-component ordering.
  // The property is equivalent to: if c is baptized with last component x,
  // then siblings with last components 1, 2, ..., x are all baptized.
  // This ensures children are numbered {1, ..., k} with no gaps.
  ghost predicate SequentialChildren(s: State) {
    forall c :: c in s.nodes && |c.components| > 1 ==>
      forall i: nat :: 1 <= i <= c.components[|c.components| - 1] ==>
        Tumbler(c.components[..|c.components| - 1] + [i]) in s.nodes
  }
}
