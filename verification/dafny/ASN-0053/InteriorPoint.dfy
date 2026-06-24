// ASN-0053: InteriorPoint — interior position is a span member (LEMMA)
include "../ASN-0034/Span.dfy"

module InteriorPoint {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened PositiveTumbler
  import opened ActionPoint
  import SpanModule = Span

  // Span σ = (s, w): start(σ) = s, width(σ) = w, reach(σ) = s ⊕ w, ⟦σ⟧ = SpanModule.Span(s, w)
  lemma InteriorPoint(s: Tumbler, w: Tumbler, p: Tumbler)
    requires InT(s) && InT(w) && InT(p)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(s)
    requires LexicographicOrder.LexicographicOrder(s, p)
    requires LexicographicOrder.LexicographicOrder(p, TumblerAdd.TumblerAdd(s, w))
    ensures p in SpanModule.Span(s, w)
  {
  }
}
