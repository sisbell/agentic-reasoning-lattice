// ASN-0034: Span — definition (DEF)
// span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}
// where s ∈ T, ℓ ∈ T, Pos(ℓ), and actionPoint(ℓ) ≤ #s.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./LexicographicOrder.dfy"

module Span {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened LexicographicOrder
  import opened NatCarrierSet

  ghost function Span(s: Tumbler, l: Tumbler): iset<Tumbler>
    requires InT(s)
    requires InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
  {
    iset t |
      InT(t) &&
      (t == s || LexicographicOrder.LexicographicOrder(s, t)) &&
      LexicographicOrder.LexicographicOrder(t, TumblerAdd.TumblerAdd(s, l))
  }
}
