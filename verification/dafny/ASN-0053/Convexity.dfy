// ASN-0053: S0 — Convexity
// x ∈ ⟦σ⟧ ⟺ x ∈ T ∧ start(σ) ≤ x < reach(σ)
// (A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ q ∈ T ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)
include "../ASN-0034/LexicographicOrder.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module Convexity {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened ActionPoint
  import opened PositiveTumbler
  import S = Span
  import SWD = SpanWellDefinedness
  import opened NatCarrierSet

  // S0: span membership as the half-open interval over T1 addresses
  // x ∈ ⟦σ⟧ ⟺ x ∈ T ∧ start(σ) ≤ x < reach(σ)
  // where start(σ) = s, reach(σ) = s ⊕ l = TumblerAdd(s, l)
  ghost predicate InSpan(x: Tumbler, s: Tumbler, l: Tumbler)
    requires InT(x) && InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
  {
    x in S.Span(s, l)
  }

  // Convexity: ⟦σ⟧ is closed under betweenness — no span skips a T1 position
  lemma Convexity(s: Tumbler, l: Tumbler, p: Tumbler, q: Tumbler, r: Tumbler)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    requires p in S.Span(s, l)
    requires r in S.Span(s, l)
    requires InT(q)
    requires p == q || LexicographicOrder.LexicographicOrder(p, q)
    requires q == r || LexicographicOrder.LexicographicOrder(q, r)
    ensures q in S.Span(s, l)
  {
    SWD.SpanWellDefinedness(s, l);
  }
}
