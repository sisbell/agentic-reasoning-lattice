include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module WellDefinedAddition {

  import opened TumblerAlgebra

  // TA0 — WellDefinedAddition (PRE, requires)
  // For tumblers a, w where w > 0 and ActionPoint(w) < |a.components|,
  // a ⊕ w is a well-defined tumbler with length |w.components|.
  lemma WellDefinedAddition(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    ensures |TumblerAdd(a, w).components| == |w.components|
  { }

}
