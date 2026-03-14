include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module WellDefinedAddition {
  import opened TumblerAlgebra

  // TA0 — WellDefinedAddition (PRE)
  // w > 0, action point k ≤ #a

  ghost predicate AdditionPrecondition(a: Tumbler, w: Tumbler) {
    PositiveTumbler(w) &&
    ActionPoint(w) < |a.components|
  }

  lemma WellDefinedAddition(a: Tumbler, w: Tumbler)
    requires AdditionPrecondition(a, w)
    ensures |TumblerAdd(a, w).components| == |w.components|
    ensures |TumblerAdd(a, w).components| >= 1
  { }
}
