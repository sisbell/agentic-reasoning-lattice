include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ContiguousSubtrees {

  import opened TumblerAlgebra

  // T5 — ContiguousSubtrees
  // For any tumbler prefix p, the set {t : p ≼ t} forms a contiguous
  // interval under LessThan: if p is a prefix of a and c, and
  // a ≤ b ≤ c, then p is a prefix of b.
  lemma ContiguousSubtrees(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(p, a)
    requires IsPrefix(p, c)
    requires LessThan(a, b) || a == b
    requires LessThan(b, c) || b == c
    ensures IsPrefix(p, b)
  { }
}
