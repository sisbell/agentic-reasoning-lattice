// ASN-0034: TumblerSub — definition (DEF)
// Tumbler subtraction a ⊖ w, defined component-wise on padded sequences:
//   L = max(#a, #w); k = zpd(a, w);
//   k undefined ⇒ rᵢ = 0 for all i ∈ [1, L];
//   k defined   ⇒ rᵢ = 0 for i < k; rₖ = aₖ − wₖ (padded);
//                  rᵢ = aᵢ (padded) for k < i ≤ L.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./ZeroPaddedDivergence.dfy"

module TumblerSub {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened ZeroPaddedDivergence
  import opened NatCarrierSet

  function TumblerSub(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures InT(r)
    ensures Length(r) == (if Length(a) >= Length(w) then Length(a) else Length(w))
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
              ==> PositiveTumbler.PositiveTumbler(r)
                  && ActionPoint.ActionPoint(r) ==
                       ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
  {
    assume false;
    a
  }
}
