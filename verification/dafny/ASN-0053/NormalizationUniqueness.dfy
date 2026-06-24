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

  // N1 (strictly increasing starts) and N2 (strict separation) hold for all consecutive pairs
  ghost predicate StrictlyNormalized(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
    forall i :: 0 <= i < |spans| - 1 ==>
      LexicographicOrder(spans[i].start, spans[i+1].start) &&
      LexicographicOrder(Reach(spans[i]), spans[i+1].start)
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
      ensures LexicographicOrder(spans[1..][i].start, spans[1..][i+1].start)
      ensures LexicographicOrder(Reach(spans[1..][i]), spans[1..][i+1].start)
    {
      assert spans[1..][i] == spans[i + 1];
      assert spans[1..][i + 1] == spans[i + 2];
    }
  }

  // ─── Order helpers ─────────────────────────────────────────────────────────

  lemma LexTransitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LexicographicOrder(a, b)
    requires LexicographicOrder(b, c)
    ensures LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  lemma LexIrreflexive(a: Tumbler)
    requires InT(a)
    ensures !LexicographicOrder(a, a)
  {
    IC.IntrinsicComparison(a, a);
  }

  lemma LexAsymmetric(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder(a, b)
    ensures !LexicographicOrder(b, a)
    ensures a != b
  {
    IC.IntrinsicComparison(a, b);
  }

  // ─── Denotation membership lemmas ──────────────────────────────────────────

  // Every member of Denote(spans) belongs to some constituent Span
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

  // Membership in any constituent Span implies membership in Denote
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

  // Reach is the exclusive upper bound, so it is not in its own span
  lemma ReachNotInOwnSpan(sigma: SpanEntry)
    requires ValidSpan(sigma)
    ensures Reach(sigma) !in S.Span(sigma.start, sigma.width)
  {
    LexIrreflexive(Reach(sigma));
  }

  // Reach(spans[0]) < spans[k].start for all k >= 1 (by N2 + N1 chain)
  lemma ReachLtStart(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures LexicographicOrder(Reach(spans[0]), spans[k].start)
    decreases k
  {
    if k >= 2 {
      ReachLtStart(spans, k - 1);
      LexTransitive(Reach(spans[0]), spans[k-1].start, spans[k].start);
    }
    // Base k == 1: N2 at i=0 gives LexOrder(Reach(spans[0]), spans[1].start) directly
  }

  // spans[0].start < spans[k].start for all k >= 1 (by N1 chain)
  lemma StartLtLaterStart(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures LexicographicOrder(spans[0].start, spans[k].start)
    decreases k
  {
    if k >= 2 {
      StartLtLaterStart(spans, k - 1);
      LexTransitive(spans[0].start, spans[k-1].start, spans[k].start);
    }
    // Base k == 1: N1 at i=0 gives LexOrder(spans[0].start, spans[1].start) directly
  }

  // spans[0].start is a lower bound for all members of Denote(spans)
  lemma MinimalStart(spans: seq<SpanEntry>, p: Tumbler)
    requires |spans| > 0
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires InT(p)
    requires p in Denote(spans)
    ensures spans[0].start == p || LexicographicOrder(spans[0].start, p)
  {
    DenoteMemberInSpan(spans, p);
    var k :| 0 <= k < |spans| && p in S.Span(spans[k].start, spans[k].width);
    if k == 0 {
      // Span membership directly gives spans[0].start <= p
      assert spans[0].start == p || LexicographicOrder(spans[0].start, p);
    } else {
      StartLtLaterStart(spans, k);
      // spans[0].start < spans[k].start
      assert spans[k].start == p || LexicographicOrder(spans[k].start, p);
      if spans[k].start == p {
        // spans[0].start < spans[k].start = p
      } else {
        LexTransitive(spans[0].start, spans[k].start, p);
      }
    }
  }

  // Reach(spans[0]) is not in any later span (since it is strictly less than their starts)
  lemma ReachNotInLaterSpan(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans)
    requires StrictlyNormalized(spans)
    requires 1 <= k < |spans|
    ensures Reach(spans[0]) !in S.Span(spans[k].start, spans[k].width)
  {
    ReachLtStart(spans, k);
    LexAsymmetric(Reach(spans[0]), spans[k].start);
    // !LexOrder(spans[k].start, Reach(spans[0])) and spans[k].start != Reach(spans[0])
    // So the first Span membership condition fails
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

  // The first span is disjoint from the denotation of the tail (by N2 + N1 separation)
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
      // p in Span(spans[0]): p < Reach(spans[0])
      assert LexicographicOrder(p, Reach(spans[0]));
      // Reach(spans[0]) < spans[k'+1].start (N2 + N1 chain)
      ReachLtStart(spans, k' + 1);
      // Chain: p < Reach(spans[0]) < spans[k'+1].start
      LexTransitive(p, Reach(spans[0]), spans[k' + 1].start);
      // But p in Span(spans[k'+1]): spans[k'+1].start <= p — contradiction
      assert spans[k' + 1].start == p || LexicographicOrder(spans[k' + 1].start, p);
      if spans[k' + 1].start == p {
        LexIrreflexive(p);
      } else {
        LexAsymmetric(p, spans[k' + 1].start);
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
      // spans2 non-empty but Denote(spans2) = Denote(spans1) = iset{}: contradiction
      StartInDenote(spans2);
      assert false;
    } else if |spans2| == 0 {
      StartInDenote(spans1);
      assert false;
    } else {
      // Step 1: equal starts — each start is a lower bound of the shared denotation
      StartInDenote(spans1);
      StartInDenote(spans2);
      assert spans1[0].start in Denote(spans2);
      assert spans2[0].start in Denote(spans1);
      MinimalStart(spans2, spans1[0].start);
      // spans2[0].start <= spans1[0].start
      MinimalStart(spans1, spans2[0].start);
      // spans1[0].start <= spans2[0].start
      if spans1[0].start != spans2[0].start {
        // Both strict inequalities hold — impossible by asymmetry
        assert LexicographicOrder(spans2[0].start, spans1[0].start);
        assert LexicographicOrder(spans1[0].start, spans2[0].start);
        LexAsymmetric(spans1[0].start, spans2[0].start);
        assert false;
      }
      assert spans1[0].start == spans2[0].start;

      // Step 2: equal reaches — if they differed, the smaller reach would be in the
      // opposite denotation but not its own (by ReachNotInDenote), contradicting equality
      ReachNotInDenote(spans1);
      ReachNotInDenote(spans2);
      SI.StrictIncrease(spans1[0].start, spans1[0].width);
      SI.StrictIncrease(spans2[0].start, spans2[0].width);
      IC.IntrinsicComparison(Reach(spans1[0]), Reach(spans2[0]));
      if LexicographicOrder(Reach(spans1[0]), Reach(spans2[0])) {
        // Reach(spans1[0]) in Span(spans2[0]): start2 < reach1 < reach2
        assert Reach(spans1[0]) in S.Span(spans2[0].start, spans2[0].width);
        SpanMemberInDenote(spans2, Reach(spans1[0]), 0);
        assert false;
      } else if LexicographicOrder(Reach(spans2[0]), Reach(spans1[0])) {
        // Reach(spans2[0]) in Span(spans1[0]): start1 < reach2 < reach1
        assert Reach(spans2[0]) in S.Span(spans1[0].start, spans1[0].width);
        SpanMemberInDenote(spans1, Reach(spans2[0]), 0);
        assert false;
      }
      // IntrinsicComparison trichotomy: neither LT nor GT means EQ
      assert Reach(spans1[0]) == Reach(spans2[0]);

      // Step 2b: left cancellation gives equal widths, hence equal first spans
      LC.LeftCancellation(spans1[0].start, spans1[0].width, spans2[0].width);
      assert spans1[0].width == spans2[0].width;
      assert spans1[0] == spans2[0];

      // Step 3: tails share denotation (set cancellation on the equal first span)
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
      // Step 4: induction on strictly shorter tails
      NormalizationUniqueness(spans1[1..], spans2[1..]);
      assert spans1[1..] == spans2[1..];
    }
  }
}
