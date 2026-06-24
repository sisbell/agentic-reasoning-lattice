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
      // ValidSpan(spans[0]); CollectiveDenotation = S.Span(spans[0]) + ...; x in it.
    } else {
      assert spans[1..][i - 1] == spans[i];
      EntryCoversCollective(spans[1..], i - 1, x);
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
