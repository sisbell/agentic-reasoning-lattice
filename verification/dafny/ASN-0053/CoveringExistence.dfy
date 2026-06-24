// ASN-0053: S7 — CoveringExistence (DEF/theorem)
// For any finite sequence P of T-positions, CoveringSpanSet(P) has length |P|
// and its collective denotation covers every element of P.
// Depends: T0, T12, TA-strict, T1, TumblerAdd
include "./SpanDefs.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module CoveringExistence {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import SWD = SpanWellDefinedness
  import S = Span
  import TA = TumblerAdd
  import LO = LexicographicOrder
  import IC = IntrinsicComparison

  // Unit width for t: l = [0,...,0,1] with #l = #t.
  function UnitWidth(t: Tumbler): (l: Tumbler)
    requires InT(t)
    ensures InT(l)
    ensures Length(l) == Length(t)
    ensures forall i :: 1 <= i < Length(t) ==> Component(l, i) == 0
    ensures Component(l, Length(t)) == 1
  {
    Tumbler(seq(Length(t) - 1, _ => 0) + [1])
  }

  // ActionPointFromIndex(UnitWidth(t), k) == Length(t) for k in [1, Length(t)].
  lemma UnitWidthAPFromIndex(t: Tumbler, k: nat)
    requires InT(t)
    requires 1 <= k <= Length(t)
    ensures exists i :: k <= i <= Length(UnitWidth(t)) && Component(UnitWidth(t), i) != 0
    ensures ActionPoint.ActionPointFromIndex(UnitWidth(t), k) == Length(t)
    decreases Length(t) - k
  {
    var l := UnitWidth(t);
    var n := Length(t);
    assert k <= n <= Length(l) && Component(l, n) == 1;
    if k < n {
      assert Component(l, k) == 0;
      UnitWidthAPFromIndex(t, k + 1);
    }
  }

  // UnitWidth(t) is a positive tumbler with action point Length(t); span is valid.
  lemma UnitSpanValid(t: Tumbler)
    requires InT(t)
    ensures PositiveTumbler.PositiveTumbler(UnitWidth(t))
    ensures ActionPoint.ActionPoint(UnitWidth(t)) == Length(t)
    ensures ValidSpan(SpanEntry(t, UnitWidth(t)))
  {
    var l := UnitWidth(t);
    var n := Length(t);
    assert Component(l, n) == 1;
    assert exists i :: 1 <= i <= Length(l) && Component(l, i) != 0 by {
      assert 1 <= n <= Length(l) && Component(l, n) != 0;
    }
    UnitWidthAPFromIndex(t, 1);
  }

  // Trailing-zero extension: t.0ⁿ appends n zeros to t.
  function TrailingZeroExt(t: Tumbler, n: nat): Tumbler
    requires InT(t)
    ensures InT(TrailingZeroExt(t, n))
    ensures Length(TrailingZeroExt(t, n)) == Length(t) + n
    ensures forall i :: 1 <= i <= Length(t) ==> Component(TrailingZeroExt(t, n), i) == Component(t, i)
  {
    Tumbler(t.components + seq(n, _ => 0))
  }

  // For any valid span (s, l) and n, TrailingZeroExt(s, n) lies in S.Span(s, l).
  // T1 case (ii): s < e when n > 0 (s is a proper prefix of e), proved via IC.LexOrderShorterWitness.
  // T1 case (i): e < TumblerAdd(s, l) at position k = ActionPoint(l).
  lemma TrailingZeroInGeneralSpan(s: Tumbler, l: Tumbler, n: nat)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    ensures TrailingZeroExt(s, n) in S.Span(s, l)
  {
    var e := TrailingZeroExt(s, n);
    var k := ActionPoint.ActionPoint(l);
    var r := TA.TumblerAdd(s, l);
    assert InT(e);
    assert Length(e) == Length(s) + n;
    assert forall i :: 1 <= i <= Length(s) ==> Component(e, i) == Component(s, i);
    assert Length(r) == Length(l);
    assert forall i :: 1 <= i < k ==> Component(r, i) == Component(s, i);
    assert Component(r, k) == Component(s, k) + Component(l, k);
    assert k >= 1;
    assert k <= Length(s);
    assert Component(l, k) != 0;
    // e and r agree on positions 1..k-1:
    assert forall i :: 1 <= i < k ==> Component(e, i) == Component(r, i) by {
      forall i | 1 <= i < k ensures Component(e, i) == Component(r, i) {
        assert Component(e, i) == Component(s, i);
        assert Component(r, i) == Component(s, i);
      }
    }
    assert k <= Length(e);
    assert k <= Length(r);
    assert Component(e, k) == Component(s, k);
    assert Component(e, k) < Component(r, k);
    // LexicographicOrder(e, r) by T1 case (i) with witness k:
    assert LO.LexicographicOrder(e, r) by {
      assert exists kw: nat ::
        && 1 <= kw
        && (forall i :: 1 <= i < kw ==>
              i <= Length(e) && i <= Length(r) && Component(e, i) == Component(r, i))
        && ((kw <= Length(e) && kw <= Length(r) && Component(e, kw) < Component(r, kw))
            || (kw == Length(e) + 1 && kw <= Length(r))) by {
        var kw := k;
      }
    }
    // LexicographicOrder(s, e) by T1 case (ii): s is a prefix of e when n > 0.
    if n == 0 {
      assert e == s;
    } else {
      assert Length(s) < Length(e); // n >= 1
      // IC.LexOrderShorterWitness registers Component(e, Length(s)+1) as trigger
      // so Z3 can instantiate the existential with k = Length(s)+1.
      IC.LexOrderShorterWitness(s, e);
    }
  }

  // Collective denotation: union of individual span denotations.
  ghost function CollectiveDenotation(spans: seq<SpanEntry>): iset<Tumbler>
    decreases |spans|
  {
    if |spans| == 0 then iset{}
    else if ValidSpan(spans[0]) then
      S.Span(spans[0].start, spans[0].width) + CollectiveDenotation(spans[1..])
    else CollectiveDenotation(spans[1..])
  }

  // x in span i implies x in CollectiveDenotation(spans).
  lemma EntryCoversCollective(spans: seq<SpanEntry>, i: nat, x: Tumbler)
    requires 0 <= i < |spans|
    requires ValidSpan(spans[i])
    requires x in S.Span(spans[i].start, spans[i].width)
    ensures x in CollectiveDenotation(spans)
    decreases i
  {
    if i == 0 {
    } else {
      assert spans[1..][i - 1] == spans[i];
      EntryCoversCollective(spans[1..], i - 1, x);
    }
  }

  // Max component-depth over all elements of P; used to build strictly-deeper witnesses.
  ghost function MaxLength(P: seq<Tumbler>): nat
    requires forall i :: 0 <= i < |P| ==> InT(P[i])
    ensures |P| > 0 ==> MaxLength(P) >= Length(P[0])
    ensures |P| > 0 ==> MaxLength(P) >= MaxLength(P[1..])
    decreases |P|
  {
    if |P| == 0 then 0
    else
      var rest := MaxLength(P[1..]);
      if Length(P[0]) > rest then Length(P[0]) else rest
  }

  lemma MaxLengthBound(P: seq<Tumbler>)
    requires forall i :: 0 <= i < |P| ==> InT(P[i])
    ensures forall i :: 0 <= i < |P| ==> Length(P[i]) <= MaxLength(P)
    decreases |P|
  {
    if |P| > 0 {
      MaxLengthBound(P[1..]);
    }
  }

  // When sigma has no valid spans, CollectiveDenotation is the empty set.
  lemma NoValidSpansEmpty(sigma: seq<SpanEntry>)
    requires forall j :: 0 <= j < |sigma| ==> !ValidSpan(sigma[j])
    ensures CollectiveDenotation(sigma) == iset{}
    decreases |sigma|
  {
    if |sigma| > 0 {
      NoValidSpansEmpty(sigma[1..]);
    }
  }

  // Covering construction: sigma_i = SpanEntry(t_i, UnitWidth(t_i)).
  function CoveringSpanSet(P: seq<Tumbler>): seq<SpanEntry>
    requires forall i :: 0 <= i < |P| ==> InT(P[i])
    ensures |CoveringSpanSet(P)| == |P|
    ensures forall i :: 0 <= i < |P| ==> CoveringSpanSet(P)[i] == SpanEntry(P[i], UnitWidth(P[i]))
  {
    seq(|P|, i requires 0 <= i < |P| => SpanEntry(P[i], UnitWidth(P[i])))
  }

  // S7 (CoveringExistence): CoveringSpanSet(P) has length |P| and covers P.
  lemma CoveringExistence(P: seq<Tumbler>)
    requires forall i :: 0 <= i < |P| ==> InT(P[i])
    ensures |CoveringSpanSet(P)| == |P|
    ensures forall i :: 0 <= i < |P| ==>
              P[i] in CollectiveDenotation(CoveringSpanSet(P))
  {
    var sigma := CoveringSpanSet(P);
    forall i | 0 <= i < |P|
      ensures P[i] in CollectiveDenotation(sigma)
    {
      UnitSpanValid(P[i]);
      assert sigma[i] == SpanEntry(P[i], UnitWidth(P[i]));
      assert ValidSpan(sigma[i]);
      SWD.SpanWellDefinedness(P[i], UnitWidth(P[i]));
      assert P[i] in S.Span(P[i], UnitWidth(P[i]));
      assert P[i] in S.Span(sigma[i].start, sigma[i].width);
      EntryCoversCollective(sigma, i, P[i]);
    }
  }
}
