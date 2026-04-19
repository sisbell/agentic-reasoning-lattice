include "./StrictIncrease.dfy"

module SpanWellDefinedness {
  // T12 — SpanWellDefinedness
  // span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import TA = TumblerAdd
  import SI = StrictIncrease

  ghost predicate LessEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  ghost function Span(s: Tumbler, len: Tumbler): iset<Tumbler>
    requires ValidTumbler(s)
    requires ValidTumbler(len)
    requires IsPositive(len)
    requires TA.ActionPoint(len) < |s.components|
  {
    iset t: Tumbler | ValidTumbler(t) && LessEqual(s, t) && LessThan(t, TA.TumblerAdd(s, len))
  }

  // (a) Endpoint existence — s ⊕ ℓ ∈ T (by TA0)
  lemma SpanEndpointExists(s: Tumbler, len: Tumbler)
    requires ValidTumbler(s)
    requires ValidTumbler(len)
    requires IsPositive(len)
    requires TA.ActionPoint(len) < |s.components|
    ensures ValidTumbler(TA.TumblerAdd(s, len))
  { }

  // (b) Non-emptiness — s ∈ span(s, ℓ) (by TA-strict)
  lemma SpanNonEmpty(s: Tumbler, len: Tumbler)
    requires ValidTumbler(s)
    requires ValidTumbler(len)
    requires IsPositive(len)
    requires TA.ActionPoint(len) < |s.components|
    ensures s in Span(s, len)
  {
    SI.StrictIncrease(s, len);
  }

  // (c) Order-convexity — a,c ∈ span ∧ a ≤ b ≤ c ⟹ b ∈ span
  lemma SpanConvex(s: Tumbler, len: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires ValidTumbler(s)
    requires ValidTumbler(len)
    requires IsPositive(len)
    requires TA.ActionPoint(len) < |s.components|
    requires a in Span(s, len)
    requires c in Span(s, len)
    requires ValidTumbler(b)
    requires LessEqual(a, b)
    requires LessEqual(b, c)
    ensures b in Span(s, len)
  { }
}
