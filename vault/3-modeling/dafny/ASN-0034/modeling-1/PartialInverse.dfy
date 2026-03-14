include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PartialInverse {
  import opened TumblerAlgebra

  // TA4 — PartialInverse
  // (a ⊕ w) ⊖ w = a under restricted preconditions
  lemma PartialInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) + 1 == |a.components|
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    ensures Subtractable(TumblerAdd(a, w), w)
    ensures TumblerSubtract(TumblerAdd(a, w), w) == a
  { }
}
