// ASN-0053: SpanDefs — shared type definitions for span-set claims.
// SpanEntry, ValidSpan, Reach, IsNormalizedSpanSet used across all ASN-0053 claims.
include "../ASN-0034/CarrierSetDefinition.dfy"
include "../ASN-0034/LexicographicOrder.dfy"
include "../ASN-0034/TumblerAdd.dfy"
include "../ASN-0034/PositiveTumbler.dfy"
include "../ASN-0034/ActionPoint.dfy"

module SpanDefs {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened NatCarrierSet

  datatype SpanEntry = SpanEntry(start: Tumbler, width: Tumbler)

  ghost predicate ValidSpan(sigma: SpanEntry) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  function Reach(sigma: SpanEntry): (r: Tumbler)
    requires ValidSpan(sigma)
    ensures InT(r)
    ensures LexicographicOrder.LexicographicOrder(sigma.start, r)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.width)
  }

  ghost predicate IsNormalizedSpanSet(spans: seq<SpanEntry>)
  {
    forall i :: 0 <= i < |spans| - 1 ==>
      (ValidSpan(spans[i]) && ValidSpan(spans[i+1]) ==>
        LexicographicOrder.LexicographicOrder(spans[i].start, spans[i+1].start) &&
        LexicographicOrder.LexicographicOrder(Reach(spans[i]), spans[i+1].start))
  }
}
