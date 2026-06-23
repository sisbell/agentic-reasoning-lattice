// ASN-0053: S2 — EmptyDistinction (DEF/corollary)
// The denotation of a well-formed span is the half-open interval [s, s⊕ℓ),
// which is non-empty: s ∈ Denotation(s, l).
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module EmptyDistinction {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened NatCarrierSet
  import SpanModule = Span
  import SWD = SpanWellDefinedness

  // S2: denotation of (s, l) is the span set; postcondition captures non-emptiness.
  ghost function Denotation(s: Tumbler, l: Tumbler): iset<Tumbler>
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    ensures s in Denotation(s, l)
  {
    SWD.SpanWellDefinedness(s, l);
    SpanModule.Span(s, l)
  }
}
