// ASN-0053: S9 — NormalizationUniqueness (theorem)
// Two normalized span sequences with equal denotation are identical.
include "./SpanDefs.dfy"
include "../ASN-0034/StrictIncrease.dfy"
include "../ASN-0034/LeftCancellation.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module NormalizationUniqueness {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import S = Span
  import LC = LeftCancellation
  import SI = StrictIncrease
  import SWD = SpanWellDefinedness
  import IC = IntrinsicComparison

  // Abbreviation: strict lexicographic order predicate (module and predicate share a name)
  ghost predicate LO(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    LexicographicOrder.LexicographicOrder(a, b)
  }

  // Every span in the sequence is well-formed
  ghost predicate AllValid(spans: seq<SpanEntry>) {
    forall i :: 0 <= i < |spans| ==> ValidSpan(spans[i])
  }

  // Union of all span denotations
  ghost function Denote(spans: seq<SpanEntry>): iset<Tumbler>
    requires AllValid(spans)
    decreases |spans|
  {
    if |spans| == 0 then iset{}
    else S.Span(spans[0].start, spans[0].width) + Denote(spans[1..])
  }

  // N1 (strictly increasing starts) and N2 (strict separation) for all consecutive pairs
  ghost predicate StrictlyNormalized(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
    forall i :: 0 <= i < |spans| - 1 ==>
      LexicographicOrder.LexicographicOrder(spans[i].start, spans[i+1].start) &&
      LexicographicOrder.LexicographicOrder(Reach(spans[i]), spans[i+1].start)
  }

  // ─── Structural helpers ────────────────────────────────────────────────────

  lemma AllValidTail(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    ensures AllValid(spans[1..])
  {
    forall i | 0 <= i < |spans[1..]|
      ensures ValidSpan(spans[1..][i])
    {
      assert spans[1..][i] == spans[i + 1];
    }
  }

  lemma StrictlyNormalizedTail(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    ensures AllValid(spans[1..])
    ensures StrictlyNormalized(spans[1..])
  {
    AllValidTail(spans);
    forall i | 0 <= i < |spans[1..]| - 1
      ensures LexicographicOrder.LexicographicOrder(spans[1..][i].start, spans[1..][i+1].start)
      ensures LexicographicOrder.LexicographicOrder(Reach(spans[1..][i]), spans[1..][i+1].start)
    {
      assert spans[1..][i] == spans[i + 1];
      assert spans[1..][i + 1] == spans[i + 2];
    }
  }

  // ─── Order helpers ─────────────────────────────────────────────────────────

  lemma LexTrans(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(b, c)
    ensures LexicographicOrder.LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  lemma LexIrreflexive(a: Tumbler)
    requires InT(a)
    ensures !LexicographicOrder.LexicographicOrder(a, a)
  {
    IC.IntrinsicComparison(a, a);
  }

  lemma LexAsymm(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures !LexicographicOrder.LexicographicOrder(b, a)
    ensures a != b
  {
    IC.IntrinsicComparison(a, b);
  }

  // ─── Denotation membership lemmas ──────────────────────────────────────────

  lemma DenoteMemberInSpan(spans: seq<SpanEntry>, p: Tumbler)
    requires AllValid(spans)
    requires InT(p)
    requires p in Denote(spans)
    ensures exists k :: 0 <= k < |spans| && p in S.Span(spans[k].start, spans[k].width)
    decreases |spans|
  {
    if |spans| > 0 {
      if p !in S.Span(spans[0].start, spans[0].width) {
        AllValidTail(spans);
        assert p in Denote(spans[1..]);
        DenoteMemberInSpan(spans[1..], p);
        var k' :| 0 <= k' < |spans[1..]| && p in S.Span(spans[1..][k'].start, spans[1..][k'].width);
        assert spans[1..][k'] == spans[k' + 1];
      }
    }
  }

  lemma SpanMemberInDenote(spans: seq<SpanEntry>, p: Tumbler, k: nat)
    requires AllValid(spans)
    requires 0 <= k < |spans|
    requires p in S.Span(spans[k].start, spans[k].width)
    ensures p in Denote(spans)
    decreases k
  {
    if k > 0 {
      AllValidTail(spans);
      assert spans[1..][k - 1] == spans[k];
      SpanMemberInDenote(spans[1..], p, k - 1);
    }
  }

  lemma StartInDenote(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    ensures spans[0].start in Denote(spans)
  {
    // Reach's ensures: LexicographicOrder(spans[0].start, Reach(spans[0]))
    // so spans[0].start satisfies all three Span membership conditions
    assert spans[0].start in S.Span(spans[0].start, spans[0].width);
    SpanMemberInDenote(spans, spans[0].start, 0);
  }

  // ─── Reach non-membership ──────────────────────────────────────────────────

  lemma ReachNotInOwnSpan(sigma: SpanEntry)
    requires ValidSpan(sigma)
    ensures Reach(sigma) !in S.Span(sigma.start, sigma.width)
  {
    LexIrreflexive(Reach(sigma));
  }

  lemma ReachLtStart(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures LexicographicOrder.LexicographicOrder(Reach(spans[0]), spans[k].start)
    decreases k
  {
    if k >= 2 {
      ReachLtStart(spans, k - 1);
      LexTrans(Reach(spans[0]), spans[k-1].start, spans[k].start);
    }
  }

  lemma StartLtLaterStart(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures LexicographicOrder.LexicographicOrder(spans[0].start, spans[k].start)
    decreases k
  {
    if k >= 2 {
      StartLtLaterStart(spans, k - 1);
      LexTrans(spans[0].start, spans[k-1].start, spans[k].start);
    }
  }

  lemma MinimalStart(spans: seq<SpanEntry>, p: Tumbler)
    requires |spans| > 0
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires InT(p)
    requires p in Denote(spans)
    ensures spans[0].start == p || LexicographicOrder.LexicographicOrder(spans[0].start, p)
  {
    DenoteMemberInSpan(spans, p);
    var k :| 0 <= k < |spans| && p in S.Span(spans[k].start, spans[k].width);
    if k == 0 {
      assert spans[0].start == p || LexicographicOrder.LexicographicOrder(spans[0].start, p);
    } else {
      StartLtLaterStart(spans, k);
      assert spans[k].start == p || LexicographicOrder.LexicographicOrder(spans[k].start, p);
      if spans[k].start == p {
      } else {
        LexTrans(spans[0].start, spans[k].start, p);
      }
    }
  }

  lemma ReachNotInLaterSpan(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures Reach(spans[0]) !in S.Span(spans[k].start, spans[k].width)
  {
    ReachLtStart(spans, k);
    LexAsymm(Reach(spans[0]), spans[k].start);
  }

  lemma ReachNotInDenoteTail(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    requires AllValid(spans[1..])
    requires StrictlyNormalized(spans)
    ensures Reach(spans[0]) !in Denote(spans[1..])
  {
    if Reach(spans[0]) in Denote(spans[1..]) {
      DenoteMemberInSpan(spans[1..], Reach(spans[0]));
      var k' :| 0 <= k' < |spans[1..]| && Reach(spans[0]) in S.Span(spans[1..][k'].start, spans[1..][k'].width);
      assert spans[1..][k'] == spans[k' + 1];
      ReachNotInLaterSpan(spans, k' + 1);
      assert false;
    }
  }

  lemma ReachNotInDenote(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    ensures Reach(spans[0]) !in Denote(spans)
  {
    AllValidTail(spans);
    ReachNotInOwnSpan(spans[0]);
    ReachNotInDenoteTail(spans);
  }

  // ─── Set cancellation and disjointness ─────────────────────────────────────

  lemma ISetCancellation(A: iset<Tumbler>, B: iset<Tumbler>, C: iset<Tumbler>)
    requires A !! B
    requires A !! C
    requires A + B == A + C
    ensures B == C
  {
  }

  lemma FirstSpanDisjointFromTail(spans: seq<SpanEntry>)
    requires |spans| > 0
    requires AllValid(spans)
    requires AllValid(spans[1..])
    requires StrictlyNormalized(spans)
    ensures S.Span(spans[0].start, spans[0].width) !! Denote(spans[1..])
  {
    forall p | p in S.Span(spans[0].start, spans[0].width) && p in Denote(spans[1..])
      ensures false
    {
      assert InT(p);
      DenoteMemberInSpan(spans[1..], p);
      var k' :| 0 <= k' < |spans[1..]| && p in S.Span(spans[1..][k'].start, spans[1..][k'].width);
      assert spans[1..][k'] == spans[k' + 1];
      assert LexicographicOrder.LexicographicOrder(p, Reach(spans[0]));
      ReachLtStart(spans, k' + 1);
      LexTrans(p, Reach(spans[0]), spans[k' + 1].start);
      assert spans[k' + 1].start == p || LexicographicOrder.LexicographicOrder(spans[k' + 1].start, p);
      if spans[k' + 1].start == p {
        LexIrreflexive(p);
      } else {
        LexAsymm(p, spans[k' + 1].start);
      }
    }
  }

  // ─── Main theorem ──────────────────────────────────────────────────────────

  lemma NormalizationUniqueness(spans1: seq<SpanEntry>, spans2: seq<SpanEntry>)
    requires AllValid(spans1) && AllValid(spans2)
    requires StrictlyNormalized(spans1) && StrictlyNormalized(spans2)
    requires Denote(spans1) == Denote(spans2)
    ensures spans1 == spans2
    decreases |spans1| + |spans2|
  {
    if |spans1| == 0 && |spans2| == 0 {
    } else if |spans1| == 0 {
      StartInDenote(spans2);
      assert false;
    } else if |spans2| == 0 {
      StartInDenote(spans1);
      assert false;
    } else {
      // Step 1: equal starts
      StartInDenote(spans1);
      StartInDenote(spans2);
      assert spans1[0].start in Denote(spans2);
      assert spans2[0].start in Denote(spans1);
      MinimalStart(spans2, spans1[0].start);
      MinimalStart(spans1, spans2[0].start);
      if spans1[0].start != spans2[0].start {
        assert LexicographicOrder.LexicographicOrder(spans2[0].start, spans1[0].start);
        assert LexicographicOrder.LexicographicOrder(spans1[0].start, spans2[0].start);
        LexAsymm(spans1[0].start, spans2[0].start);
        assert false;
      }
      assert spans1[0].start == spans2[0].start;

      // Step 2: equal reaches → equal widths via left cancellation
      ReachNotInDenote(spans1);
      ReachNotInDenote(spans2);
      SI.StrictIncrease(spans1[0].start, spans1[0].width);
      SI.StrictIncrease(spans2[0].start, spans2[0].width);
      IC.IntrinsicComparison(Reach(spans1[0]), Reach(spans2[0]));
      if LexicographicOrder.LexicographicOrder(Reach(spans1[0]), Reach(spans2[0])) {
        assert Reach(spans1[0]) in S.Span(spans2[0].start, spans2[0].width);
        SpanMemberInDenote(spans2, Reach(spans1[0]), 0);
        assert false;
      } else if LexicographicOrder.LexicographicOrder(Reach(spans2[0]), Reach(spans1[0])) {
        assert Reach(spans2[0]) in S.Span(spans1[0].start, spans1[0].width);
        SpanMemberInDenote(spans1, Reach(spans2[0]), 0);
        assert false;
      }
      assert Reach(spans1[0]) == Reach(spans2[0]);
      LC.LeftCancellation(spans1[0].start, spans1[0].width, spans2[0].width);
      assert spans1[0].width == spans2[0].width;
      assert spans1[0] == spans2[0];

      // Step 3: tails share denotation; recurse
      StrictlyNormalizedTail(spans1);
      StrictlyNormalizedTail(spans2);
      FirstSpanDisjointFromTail(spans1);
      FirstSpanDisjointFromTail(spans2);
      assert S.Span(spans1[0].start, spans1[0].width) == S.Span(spans2[0].start, spans2[0].width);
      assert Denote(spans1) == S.Span(spans1[0].start, spans1[0].width) + Denote(spans1[1..]);
      assert Denote(spans2) == S.Span(spans2[0].start, spans2[0].width) + Denote(spans2[1..]);
      ISetCancellation(
        S.Span(spans1[0].start, spans1[0].width),
        Denote(spans1[1..]),
        Denote(spans2[1..]));
      NormalizationUniqueness(spans1[1..], spans2[1..]);
      assert spans1[1..] == spans2[1..];
    }
  }
}
