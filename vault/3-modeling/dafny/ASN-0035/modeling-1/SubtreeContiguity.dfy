include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module SubtreeContiguity {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // N9 — SubtreeContiguity
  // For any node n, the set {a : n ≼ a} is a contiguous interval under T1.
  // Derived from T5 (ContiguousSubtrees).
  lemma SubtreeContiguity(n: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(n, a)
    requires IsPrefix(n, c)
    requires LessEq(a, b)
    requires LessEq(b, c)
    ensures IsPrefix(n, b)
  { }
}
