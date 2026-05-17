// ASN-0034: TA3 — OrderPreservationUnderSubtractionWeak
// (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./CanonicalRepresentation.dfy"
include "./PositiveTumbler.dfy"
include "./PositiveDominatesZero.dfy"
include "./TumblerSub.dfy"
include "./WellDefinedSubtraction.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./Divergence.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatZeroMinimum.dfy"
include "./NatDiscreteness.dfy"
include "./NatPartialSubtraction.dfy"
include "./NatArithmeticClosureAndIdentity.dfy"

module OrderPreservationUnderSubtractionWeak {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened CanonicalRepresentation
  import opened PositiveTumbler
  import opened PositiveDominatesZero
  import opened TumblerSub
  import opened WellDefinedSubtraction
  import opened ZeroPaddedDivergence
  import Divergence
  import opened NatStrictTotalOrder
  import opened NatZeroMinimum
  import opened NatDiscreteness
  import opened NatPartialSubtraction
  import opened NatArithmeticClosureAndIdentity
  import opened NatCarrierSet

  lemma OrderPreservationUnderSubtractionWeak(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  { }
}
