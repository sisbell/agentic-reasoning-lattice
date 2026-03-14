include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ReverseInverse {
  import opened TumblerAlgebra

  // (Reverse inverse) — ASN-0034
  // (a ⊖ w) ⊕ w = a under restricted preconditions
  lemma ReverseInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) + 1 == |a.components|
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    requires Subtractable(a, w)
    ensures TumblerAdd(TumblerSubtract(a, w), w) == a
  { }
}
