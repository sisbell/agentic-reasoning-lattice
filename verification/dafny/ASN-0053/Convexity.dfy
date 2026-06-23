// ASN-0053: S0 — Convexity (DEF)
// Span membership: x ∈ ⟦σ⟧ ⟺ start(σ) ≤ x < reach(σ)
// Convexity: p, r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r ⟹ q ∈ ⟦σ⟧
include "../ASN-0034/SpanWellDefinedness.dfy"

module Convexity {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened Span
  import opened NatCarrierSet
  import SpanWD = SpanWellDefinedness

  // Span σ = (start, length) pair satisfying T12.
  datatype SpanValue = SpanValue(start: Tumbler, length: Tumbler)

  ghost predicate ValidSpan(sigma: SpanValue) {
    InT(sigma.start) &&
    InT(sigma.length) &&
    PositiveTumbler.PositiveTumbler(sigma.length) &&
    ActionPoint.ActionPoint(sigma.length) <= Length(sigma.start)
  }

  // S0 (DEF): x ∈ ⟦σ⟧ ⟺ start(σ) ≤ x < reach(σ)
  ghost predicate SpanMembership(x: Tumbler, sigma: SpanValue)
    requires InT(x)
    requires ValidSpan(sigma)
  {
    x in Span.Span(sigma.start, sigma.length)
  }

  // S0 (theorem): p, r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r ⟹ q ∈ ⟦σ⟧
  lemma Convexity(sigma: SpanValue, p: Tumbler, q: Tumbler, r: Tumbler)
    requires ValidSpan(sigma)
    requires InT(p) && InT(q) && InT(r)
    requires SpanMembership(p, sigma) && SpanMembership(r, sigma)
    requires (p == q || LexicographicOrder.LexicographicOrder(p, q))
    requires (q == r || LexicographicOrder.LexicographicOrder(q, r))
    ensures SpanMembership(q, sigma)
  {
    SpanWD.SpanWellDefinedness(sigma.start, sigma.length);
  }
}
