include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T5 — ContiguousSubtrees
module ContiguousSubtrees {
  import opened TumblerAlgebra

  ghost predicate LessEq(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  lemma ContiguousSubtrees(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(p, a)
    requires IsPrefix(p, c)
    requires LessEq(a, b)
    requires LessEq(b, c)
    ensures IsPrefix(p, b)
  { }
}
