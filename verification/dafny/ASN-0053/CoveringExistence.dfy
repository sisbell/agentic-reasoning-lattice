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

  // Trailing-zero extension: s.0ⁿ = Tumbler(s.components + n zeros).
  // InT holds since |components| = Length(s) + n ≥ Length(s) ≥ 1 (T0 comprehension).
  function TrailingZeroExt(s: Tumbler, n: nat): (ext: Tumbler)
    requires InT(s)
    ensures InT(ext)
    ensures Length(ext) == Length(s) + n
    ensures forall i :: 1 <= i <= Length(s) ==> Component(ext, i) == Component(s, i)
    ensures forall i :: Length(s) < i <= Length(s) + n ==> Component(ext, i) == 0
  {
    Tumbler(s.components + seq(n, _ => 0))
  }

  // Every trailing-zero extension s.0ⁿ lies in Span(s, l).
  // For n = 0: ext = s; s ∈ Span(s, l) by T12(b).
  // For n ≥ 1: s < ext by T1 case (ii) (prefix); ext < s⊕l by T1 case (i) at ActionPoint(l).
  lemma TrailingZeroExtInSpan(s: Tumbler, l: Tumbler, n: nat)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    ensures TrailingZeroExt(s, n) in SpanModule.Span(s, l)
  {
    var ext := TrailingZeroExt(s, n);
    var reach := TumblerAdd.TumblerAdd(s, l);
    var k := ActionPoint.ActionPoint(l);

    if n == 0 {
      SWD.SpanWellDefinedness(s, l);
      assert ext == s;
    } else {
      // s < ext: T1 case (ii) with witness k1 = Length(s) + 1.
      assert LexicographicOrder.LexicographicOrder(s, ext) by {
        var k1 := Length(s) + 1;
        assert 1 <= k1;
        assert k1 == Length(s) + 1 && k1 <= Length(ext);
        assert forall i :: 1 <= i < k1 ==>
          i <= Length(s) && i <= Length(ext) &&
          Component(s, i) == Component(ext, i);
      }
      // ext < reach: T1 case (i) with witness k = ActionPoint(l).
      assert LexicographicOrder.LexicographicOrder(ext, reach) by {
        assert 1 <= k;
        assert k <= Length(ext) && k <= Length(reach);
        assert forall i :: 1 <= i < k ==>
          i <= Length(ext) && i <= Length(reach) &&
          Component(ext, i) == Component(reach, i);
        assert Component(ext, k) == Component(s, k);
        assert Component(reach, k) == Component(s, k) + Component(l, k);
        assert Component(l, k) != 0;
        assert Component(ext, k) < Component(reach, k);
      }
    }
  }

  // S7 negative postcondition: Span(s, l) is infinite.
  // The map n ↦ s.0ⁿ injects ℕ into Span(s, l): all extensions lie in the span
  // (TrailingZeroExtInSpan) and are pairwise distinct (distinct lengths).
  // Hence no finite set can equal ⟦σ⟧ — the finite-vs-infinite mismatch.
  lemma SpanInfinitude(s: Tumbler, l: Tumbler)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    ensures forall n: nat :: TrailingZeroExt(s, n) in SpanModule.Span(s, l)
    ensures forall m: nat, n: nat :: m != n ==> TrailingZeroExt(s, m) != TrailingZeroExt(s, n)
  {
    forall n: nat ensures TrailingZeroExt(s, n) in SpanModule.Span(s, l) {
      TrailingZeroExtInSpan(s, l, n);
    }
    forall m: nat, n: nat | m != n ensures TrailingZeroExt(s, m) != TrailingZeroExt(s, n) {
      assert Length(TrailingZeroExt(s, m)) == Length(s) + m;
      assert Length(TrailingZeroExt(s, n)) == Length(s) + n;
    }
  }
}
