include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubtreeDisjointness {
  import opened TumblerAlgebra

  // N10 — SubtreeDisjointness
  // For non-nesting nodes m, n, their subtrees are disjoint:
  // {a : m ≼ a} ∩ {a : n ≼ a} = ∅
  lemma SubtreeDisjointness(m: Tumbler, n: Tumbler, a: Tumbler)
    requires !IsPrefix(m, n) && !IsPrefix(n, m)
    requires IsPrefix(m, a)
    requires IsPrefix(n, a)
    ensures false
  { }
}
