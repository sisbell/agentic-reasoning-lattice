// ASN-0053: WF — WellFormedSpanFromEndpoints (DEF/lemma)
// For s, r ∈ T with s < r and #s = #r, the pair γ = (s, r ⊖ s) is a well-formed
// level-uniform span with reach(γ) = r.
include "./SpanDefs.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"
include "../ASN-0034/Divergence.dfy"
include "../ASN-0034/TumblerSub.dfy"

module WellFormedSpanFromEndpoints {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import D1 = DisplacementRoundTrip
  import Div = Divergence
  import TS = TumblerSub

  // When #a = #b and a != b, divergence(a, b) ≤ #a.
  // Equal length excludes the prefix case: if FirstMismatch returned #a + 1,
  // all shared components would agree and extensionality would force a == b.
  lemma DivergenceEqualLength(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires a != b
    requires Length(a) == Length(b)
    ensures Div.Divergence(a, b) <= Length(a)
  {
    var m := Length(a);
    if Div.Divergence(a, b) == m + 1 {
      assert forall i :: 1 <= i < Div.Divergence(a, b) ==> Component(a, i) == Component(b, i);
      assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);
      Extensionality(a, b);
    }
  }

  // WF: for s < r with #s = #r, γ = (s, r ⊖ s) is a valid level-uniform span
  // with reach(γ) = r.
  lemma WellFormedSpanFromEndpoints(s: Tumbler, r: Tumbler)
    requires InT(s) && InT(r)
    requires LexicographicOrder.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    ensures ValidSpan(SpanEntry(s, TS.TumblerSub(r, s)))
    ensures Reach(SpanEntry(s, TS.TumblerSub(r, s))) == r
    ensures Length(TS.TumblerSub(r, s)) == Length(s)
  {
    D1.LexImpliesNotEqual(s, r);
    DivergenceEqualLength(s, r);
    D1.DisplacementRoundTrip(s, r);
  }
}
