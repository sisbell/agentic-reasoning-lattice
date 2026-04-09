include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module WellDefinedSubtraction {

  import opened TumblerAlgebra

  // TA2 — WellDefinedSubtraction (PRE, requires)
  // For tumblers a, w where a ≥ w (Subtractable), a ⊖ w is a well-defined
  // tumbler with length max(|a|, |w|).
  lemma WellDefinedSubtraction(a: Tumbler, w: Tumbler)
    requires Subtractable(a, w)
    ensures |TumblerSubtract(a, w).components| == Max(|a.components|, |w.components|)
  { }

}
