// ASN-0053: S7 — CoveringExistence (DEF/theorem)
// Every finite sequence P of positions in T has a covering span-set of |P| spans.
// Construction: for each t ∈ P, the unit span (t, [0,...,0,1]) covers t because
// T12 is satisfied (action point = Length(t) ≤ Length(t)) and s ∈ Span(s, ℓ) by SWD.
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module CoveringExistence {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened NatCarrierSet
  import SpanModule = Span
  import SWD = SpanWellDefinedness

  datatype SpanEntry = SpanEntry(start: Tumbler, width: Tumbler)

  ghost predicate ValidSpan(sigma: SpanEntry) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  // Explicit witness for PositiveTumbler on [0,...,0,1].
  lemma UnitWidthPositive(n: nat, comps: seq<nat>)
    requires n >= 1
    requires comps == seq(n - 1, _ => 0) + [1]
    ensures PositiveTumbler.PositiveTumbler(Tumbler(comps))
  {
    var r := Tumbler(comps);
    assert r.components == comps;
    assert comps[n - 1] == 1;
    assert r.components[n - 1] == 1;
    assert |r.components| == n;
    assert Component(r, n) == r.components[n - 1];
    assert Component(r, n) != 0;
  }

  // ℓ = [0,...,0,1] with Length(ℓ) = Length(t).
  // Action point k = Length(t) ≤ Length(t), so T12 holds for (t, ℓ).
  function UnitWidth(t: Tumbler): (result: Tumbler)
    requires InT(t)
    ensures InT(result)
    ensures Length(result) == Length(t)
    ensures PositiveTumbler.PositiveTumbler(result)
    ensures ActionPoint.ActionPoint(result) <= Length(t)
  {
    var n := Length(t);
    var comps := seq(n - 1, _ => 0) + [1];
    UnitWidthPositive(n, comps);
    Tumbler(comps)
  }

  // The unit span (t, UnitWidth(t)) covers position t.
  ghost function CoverPoint(t: Tumbler): (sigma: SpanEntry)
    requires InT(t)
    ensures ValidSpan(sigma)
    ensures t in SpanModule.Span(sigma.start, sigma.width)
  {
    var l := UnitWidth(t);
    SWD.SpanWellDefinedness(t, l);
    SpanEntry(t, l)
  }

  // S7 (CoveringExistence): for any finite sequence P, returns |P| spans
  // where span i is valid and covers position P[i].
  // Combined ensures: ValidSpan guards the well-formedness of the Span call.
  ghost function CoveringSpanSet(P: seq<Tumbler>): (sigma: seq<SpanEntry>)
    requires forall i :: 0 <= i < |P| ==> InT(P[i])
    ensures |sigma| == |P|
    ensures forall i :: 0 <= i < |P| ==>
      ValidSpan(sigma[i]) &&
      P[i] in SpanModule.Span(sigma[i].start, sigma[i].width)
    decreases |P|
  {
    if |P| == 0 then []
    else [CoverPoint(P[0])] + CoveringSpanSet(P[1..])
  }
}
