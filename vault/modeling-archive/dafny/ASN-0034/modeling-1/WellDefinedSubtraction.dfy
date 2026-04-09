include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module WellDefinedSubtraction {
  import opened TumblerAlgebra

  // TA2 — WellDefinedSubtraction (PRE)
  // a ≥ w

  ghost predicate SubtractionPrecondition(a: Tumbler, w: Tumbler) {
    Subtractable(a, w)
  }

  lemma WellDefinedSubtraction(a: Tumbler, w: Tumbler)
    requires SubtractionPrecondition(a, w)
    ensures |TumblerSubtract(a, w).components| == Max(|a.components|, |w.components|)
  { }
}
