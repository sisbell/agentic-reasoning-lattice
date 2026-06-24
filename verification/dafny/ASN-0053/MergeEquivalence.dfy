// ASN-0053: S3 — MergeEquivalence (DEF/theorem)
// γ = (s, r ⊖ s) with s = min(start(α), start(β)), r = max(reach(α), reach(β)).
// ⟦α⟧ ∪ ⟦β⟧ = {t : s ≤ t < r} when α and β overlap or are adjacent.
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module MergeEquivalence {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import S = Span
  import SWD = SpanWellDefinedness
  import TS = TumblerSub
  import IC = IntrinsicComparison

  ghost predicate Leq(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    a == b || LO.LexicographicOrder(a, b)
  }

  // s = min(start(α), start(β))
  ghost function MergeStart(alpha: SpanEntry, beta: SpanEntry): (s: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(s)
    ensures LO.LexicographicOrder(alpha.start, beta.start) ==> s == alpha.start
    ensures !LO.LexicographicOrder(alpha.start, beta.start) ==> s == beta.start
    ensures Leq(s, beta.start)
  {
    if LO.LexicographicOrder(alpha.start, beta.start) then alpha.start else beta.start
  }

  // r = max(reach(α), reach(β))
  ghost function MergeReach(alpha: SpanEntry, beta: SpanEntry): (r: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(r)
    ensures LO.LexicographicOrder(Reach(alpha), Reach(beta)) ==> r == Reach(beta)
    ensures !LO.LexicographicOrder(Reach(alpha), Reach(beta)) ==> r == Reach(alpha)
    ensures Leq(Reach(alpha), r)
  {
    if LO.LexicographicOrder(Reach(alpha), Reach(beta)) then Reach(beta) else Reach(alpha)
  }

  // The earlier-starting span reaches at least to the later-starting span's start.
  ghost predicate OverlapOrAdjacent(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
  {
    if Leq(alpha.start, beta.start) then Leq(beta.start, Reach(alpha))
    else Leq(alpha.start, Reach(beta))
  }

  // γ = (s, r ⊖ s)
  ghost function MergeSpan(alpha: SpanEntry, beta: SpanEntry): SpanEntry
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LO.LexicographicOrder(MergeStart(alpha, beta), MergeReach(alpha, beta))
  {
    SpanEntry(MergeStart(alpha, beta), TS.TumblerSub(MergeReach(alpha, beta), MergeStart(alpha, beta)))
  }

  lemma LexTrans(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LO.LexicographicOrder(a, b)
    requires LO.LexicographicOrder(b, c)
    ensures LO.LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  // s < r
  lemma StartLtReach(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures LO.LexicographicOrder(MergeStart(alpha, beta), MergeReach(alpha, beta))
  {
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(Reach(alpha), Reach(beta));
    var s := MergeStart(alpha, beta);
    var r := MergeReach(alpha, beta);
    if LO.LexicographicOrder(alpha.start, beta.start) {
      assert s == alpha.start;
      if r == Reach(alpha) { } else { LexTrans(s, Reach(alpha), r); }
    } else if alpha.start == beta.start {
      assert s == beta.start;
      if r == Reach(alpha) { } else { LexTrans(s, Reach(alpha), r); }
    } else {
      assert LO.LexicographicOrder(beta.start, alpha.start);
      assert s == beta.start;
      if r == Reach(beta) {
      } else {
        LexTrans(s, alpha.start, Reach(alpha));
      }
    }
  }

  // #s = #r
  lemma SameLengthMerge(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    ensures Length(MergeStart(alpha, beta)) == Length(MergeReach(alpha, beta))
  {
    S6.LevelConstraint(alpha);
    S6.LevelConstraint(beta);
  }

  // γ is valid with reach = r; caller must supply s < r.
  lemma MergeSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    requires LO.LexicographicOrder(MergeStart(alpha, beta), MergeReach(alpha, beta))
    ensures ValidSpan(MergeSpan(alpha, beta))
    ensures Reach(MergeSpan(alpha, beta)) == MergeReach(alpha, beta)
  {
    SameLengthMerge(alpha, beta);
    WF.WellFormedSpanFromEndpoints(MergeStart(alpha, beta), MergeReach(alpha, beta));
  }

  // Forward: t ∈ Span(α) ∪ Span(β) → s ≤ t < r.
  lemma MergeForward(alpha: SpanEntry, beta: SpanEntry, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires OverlapOrAdjacent(alpha, beta)
    requires InT(t)
    requires t in S.Span(alpha.start, alpha.width) || t in S.Span(beta.start, beta.width)
    ensures (t == MergeStart(alpha, beta) || LO.LexicographicOrder(MergeStart(alpha, beta), t)) &&
            LO.LexicographicOrder(t, MergeReach(alpha, beta))
  {
    var s := MergeStart(alpha, beta);
    var r := MergeReach(alpha, beta);
    IC.IntrinsicComparison(alpha.start, beta.start);

    if t in S.Span(alpha.start, alpha.width) {
      if LO.LexicographicOrder(beta.start, alpha.start) {
        // s = beta.start < alpha.start ≤ t → LO(s, t)
        assert s == beta.start;
        if t == alpha.start { } else { LexTrans(s, alpha.start, t); }
      } else {
        // alpha.start ≤ beta.start; s = alpha.start ≤ t
        assert s == alpha.start;
      }
      // t < Reach(alpha) ≤ r
      if Reach(alpha) != r { LexTrans(t, Reach(alpha), r); }
    } else {
      // t in Span(beta): s ≤ beta.start ≤ t
      if LO.LexicographicOrder(beta.start, alpha.start) {
        // s = beta.start ≤ t (s == beta.start from MergeStart)
        assert s == beta.start;
      } else {
        // alpha.start ≤ beta.start; s = alpha.start ≤ beta.start ≤ t
        assert s == alpha.start;
        if alpha.start == beta.start {
          // s == beta.start; t ≥ beta.start = s
        } else {
          // LO(alpha.start, beta.start); (t == beta.start || LO(beta.start, t))
          if t == beta.start { } else { LexTrans(s, beta.start, t); }
        }
      }
      // t < Reach(beta) ≤ r
      IC.IntrinsicComparison(Reach(beta), r);
      if Reach(beta) != r { LexTrans(t, Reach(beta), r); }
    }
  }

  // Backward: s ≤ t < r → t ∈ Span(α) ∪ Span(β).
  lemma MergeBackward(alpha: SpanEntry, beta: SpanEntry, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires OverlapOrAdjacent(alpha, beta)
    requires InT(t)
    requires (t == MergeStart(alpha, beta) || LO.LexicographicOrder(MergeStart(alpha, beta), t)) &&
             LO.LexicographicOrder(t, MergeReach(alpha, beta))
    ensures t in S.Span(alpha.start, alpha.width) || t in S.Span(beta.start, beta.width)
  {
    var s := MergeStart(alpha, beta);
    var r := MergeReach(alpha, beta);
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(t, Reach(alpha));
    IC.IntrinsicComparison(t, Reach(beta));

    if LO.LexicographicOrder(beta.start, alpha.start) {
      // s = beta.start; OA: Leq(alpha.start, Reach(beta))
      assert s == beta.start;
      assert Leq(alpha.start, Reach(beta));

      if LO.LexicographicOrder(t, Reach(beta)) {
        // s = beta.start ≤ t < Reach(beta) → t ∈ Span(beta)
      } else if t == Reach(beta) {
        // t = Reach(beta) < r → r = Reach(alpha)
        IC.IntrinsicComparison(Reach(beta), r);
        assert r == Reach(alpha);
        // OA: alpha.start ≤ Reach(beta) = t and t < Reach(alpha) = r
        if alpha.start == t { } else { }  // Leq(alpha.start, Reach(beta)) and t = Reach(beta)
        // t ∈ Span(alpha)
      } else {
        // LO(Reach(beta), t); t < r; r = Reach(alpha) (since Reach(beta) < t < r)
        IC.IntrinsicComparison(Reach(beta), r);
        assert r == Reach(alpha);
        // OA: alpha.start ≤ Reach(beta) < t, and t < Reach(alpha) = r
        if alpha.start == Reach(beta) { }
        else { LexTrans(alpha.start, Reach(beta), t); }
        // t ∈ Span(alpha)
      }
    } else {
      // alpha.start ≤ beta.start; s = alpha.start; OA: Leq(beta.start, Reach(alpha))
      assert alpha.start == beta.start || LO.LexicographicOrder(alpha.start, beta.start);
      assert s == alpha.start;
      assert Leq(beta.start, Reach(alpha));

      if LO.LexicographicOrder(t, Reach(alpha)) {
        // s = alpha.start ≤ t < Reach(alpha) → t ∈ Span(alpha)
      } else if t == Reach(alpha) {
        // t = Reach(alpha) < r → r = Reach(beta)
        IC.IntrinsicComparison(Reach(alpha), r);
        assert r == Reach(beta);
        // OA: beta.start ≤ Reach(alpha) = t; t < Reach(beta) = r → t ∈ Span(beta)
        if beta.start == t { } else { }  // Leq(beta.start, Reach(alpha)) and t = Reach(alpha)
      } else {
        // LO(Reach(alpha), t); t < r; r = Reach(beta)
        IC.IntrinsicComparison(Reach(alpha), r);
        assert r == Reach(beta);
        // OA: beta.start ≤ Reach(alpha) < t; t < Reach(beta) = r → t ∈ Span(beta)
        if beta.start == Reach(alpha) { }
        else { LexTrans(beta.start, Reach(alpha), t); }
      }
    }
  }

  // S3: ⟦α⟧ ∪ ⟦β⟧ = {t : s ≤ t < r} — interval form of the merge.
  lemma MergeEquivalence(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    requires OverlapOrAdjacent(alpha, beta)
    ensures
      var s := MergeStart(alpha, beta);
      var r := MergeReach(alpha, beta);
      forall t: Tumbler :: InT(t) ==>
        ((t in S.Span(alpha.start, alpha.width) || t in S.Span(beta.start, beta.width)) <==>
         (InT(t) && (t == s || LO.LexicographicOrder(s, t)) && LO.LexicographicOrder(t, r)))
  {
    var s := MergeStart(alpha, beta);
    var r := MergeReach(alpha, beta);

    forall t: Tumbler | InT(t)
      ensures ((t in S.Span(alpha.start, alpha.width) || t in S.Span(beta.start, beta.width)) <==>
               (InT(t) && (t == s || LO.LexicographicOrder(s, t)) && LO.LexicographicOrder(t, r)))
    {
      if t in S.Span(alpha.start, alpha.width) || t in S.Span(beta.start, beta.width) {
        MergeForward(alpha, beta, t);
      }
      if (t == s || LO.LexicographicOrder(s, t)) && LO.LexicographicOrder(t, r) {
        MergeBackward(alpha, beta, t);
      }
    }
  }
}
