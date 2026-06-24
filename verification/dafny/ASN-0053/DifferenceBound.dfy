// ASN-0053: S11 — DifferenceBound (DEF/theorem)
// For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧,
// ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.
// λ = (start(α), start(β) ⊖ start(α)) when start(α) < start(β)
// ρ = (reach(β), reach(α) ⊖ reach(β)) when reach(β) < reach(α)
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "./EmptyDistinction.dfy"
include "./Convexity.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module DifferenceBound {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import WF = WellFormedSpanFromEndpoints
  import LC = LevelConstraint
  import S = Span
  import SWD = SpanWellDefinedness
  import TS = TumblerSub
  import IC = IntrinsicComparison
  import CV = Convexity

  ghost predicate Leq(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    a == b || LexicographicOrder.LexicographicOrder(a, b)
  }

  // S11: DifferenceBound — constructs the span-set for ⟦α⟧ \ ⟦β⟧.
  ghost function DifferenceBound(alpha: SpanEntry, beta: SpanEntry): (result: seq<SpanEntry>)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires Leq(alpha.start, beta.start)
    requires Leq(Reach(beta), Reach(alpha))
    ensures |result| <= 2
  {
    var left :=
      if LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
      then [SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start))]
      else [];
    var right :=
      if LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
      then [SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)))]
      else [];
    left + right
  }

  lemma LeftSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    ensures ValidSpan(SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start)))
    ensures Reach(SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start))) == beta.start
  {
    WF.WellFormedSpanFromEndpoints(alpha.start, beta.start);
  }

  lemma RightSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures ValidSpan(SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta))))
    ensures Reach(SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)))) == Reach(alpha)
  {
    LC.LevelConstraint(alpha);
    LC.LevelConstraint(beta);
    WF.WellFormedSpanFromEndpoints(Reach(beta), Reach(alpha));
  }

  ghost function CollectiveDenotation(spans: seq<SpanEntry>): iset<Tumbler>
    decreases |spans|
  {
    if |spans| == 0 then iset{}
    else if ValidSpan(spans[0]) then
      S.Span(spans[0].start, spans[0].width) + CollectiveDenotation(spans[1..])
    else CollectiveDenotation(spans[1..])
  }

  lemma LexTrans(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(b, c)
    ensures LexicographicOrder.LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  lemma BetaStartLtReachAlpha(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires Leq(Reach(beta), Reach(alpha))
    ensures LexicographicOrder.LexicographicOrder(beta.start, Reach(alpha))
  {
    SWD.SpanWellDefinedness(beta.start, beta.width);
    if Reach(beta) == Reach(alpha) { }
    else { LexTrans(beta.start, Reach(beta), Reach(alpha)); }
  }

  lemma AlphaStartLtReachBeta(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires Leq(alpha.start, beta.start)
    ensures LexicographicOrder.LexicographicOrder(alpha.start, Reach(beta))
  {
    SWD.SpanWellDefinedness(beta.start, beta.width);
    if alpha.start == beta.start { }
    else { LexTrans(alpha.start, beta.start, Reach(beta)); }
  }

  // ── Per-case correctness lemmas ────────────────────────────────────────────

  // BothActive forward: every element of collective is in the difference.
  lemma {:vcs_split_on_every_assert} BothActiveForward(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures forall t: Tumbler | t in CollectiveDenotation(DifferenceBound(alpha, beta)) ::
            t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    LeftSpanValid(alpha, beta);
    RightSpanValid(alpha, beta);
    var lambda := SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start));
    var rho := SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)));
    assert DifferenceBound(alpha, beta) == [lambda, rho];
    assert Reach(lambda) == beta.start;
    assert Reach(rho) == Reach(alpha);
    SWD.SpanWellDefinedness(beta.start, beta.width);
    // Prove CollectiveDenotation equality via one-step unfoldings
    assert CollectiveDenotation([lambda, rho]) ==
           S.Span(lambda.start, lambda.width) + CollectiveDenotation([rho]);
    assert CollectiveDenotation([rho]) ==
           S.Span(rho.start, rho.width) + CollectiveDenotation([]);
    assert CollectiveDenotation([]) == iset{};
    assert CollectiveDenotation(DifferenceBound(alpha, beta)) ==
           S.Span(lambda.start, lambda.width) + S.Span(rho.start, rho.width);

    forall t: Tumbler | t in CollectiveDenotation(DifferenceBound(alpha, beta))
      ensures t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
    {
      if t in S.Span(lambda.start, lambda.width) {
        // t < beta.start < Reach(beta) ≤ Reach(alpha) → t ∈ S.Span(alpha); t < beta.start → t ∉ S.Span(beta)
        LexTrans(t, beta.start, Reach(beta));
        if Reach(beta) != Reach(alpha) { LexTrans(t, Reach(beta), Reach(alpha)); }
        IC.IntrinsicComparison(t, beta.start);
      } else {
        // t ∈ S.Span(rho): Reach(beta) ≤ t < Reach(alpha); alpha.start < Reach(beta) ≤ t → t ∈ S.Span(alpha)
        AlphaStartLtReachBeta(alpha, beta);
        if Reach(beta) == t { } else { LexTrans(alpha.start, Reach(beta), t); }
        IC.IntrinsicComparison(t, Reach(beta));
      }
    }
  }

  // BothActive backward: every element of the difference is in collective.
  lemma {:vcs_split_on_every_assert} BothActiveBackward(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures forall t: Tumbler | t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width) ::
            t in CollectiveDenotation(DifferenceBound(alpha, beta))
  {
    LeftSpanValid(alpha, beta);
    RightSpanValid(alpha, beta);
    var lambda := SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start));
    var rho := SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)));
    assert DifferenceBound(alpha, beta) == [lambda, rho];
    assert Reach(lambda) == beta.start;
    assert Reach(rho) == Reach(alpha);
    SWD.SpanWellDefinedness(beta.start, beta.width);
    // Prove CollectiveDenotation equality via one-step unfoldings
    assert CollectiveDenotation([lambda, rho]) ==
           S.Span(lambda.start, lambda.width) + CollectiveDenotation([rho]);
    assert CollectiveDenotation([rho]) ==
           S.Span(rho.start, rho.width) + CollectiveDenotation([]);
    assert CollectiveDenotation([]) == iset{};
    assert CollectiveDenotation(DifferenceBound(alpha, beta)) ==
           S.Span(lambda.start, lambda.width) + S.Span(rho.start, rho.width);

    forall t: Tumbler | t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
      ensures t in CollectiveDenotation(DifferenceBound(alpha, beta))
    {
      IC.IntrinsicComparison(t, beta.start);
      if LexicographicOrder.LexicographicOrder(t, beta.start) {
        // t < beta.start = Reach(lambda); alpha.start = lambda.start ≤ t → t ∈ S.Span(lambda)
        assert t in S.Span(lambda.start, lambda.width);
      } else if t == beta.start {
        assert false; // beta.start ∈ S.Span(beta), contradicts t ∉ S.Span(beta)
      } else {
        // beta.start < t; t ∉ S.Span(beta) → t ≥ Reach(beta)
        IC.IntrinsicComparison(t, Reach(beta));
        if LexicographicOrder.LexicographicOrder(t, Reach(beta)) {
          assert false; // t ∈ S.Span(beta), contradiction
        } else {
          // t ≥ Reach(beta) = rho.start and t < Reach(alpha) = Reach(rho) → t ∈ S.Span(rho)
          assert t in S.Span(rho.start, rho.width);
        }
      }
    }
  }

  // Case: both λ and ρ active.
  lemma BothActiveCorrect(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures CollectiveDenotation(DifferenceBound(alpha, beta)) ==
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    BothActiveForward(alpha, beta);
    BothActiveBackward(alpha, beta);
  }

  // Tightness (S11 case c): no single span γ covers ⟦α⟧ \ ⟦β⟧ when neither boundary coincides.
  lemma BothActiveTight(alpha: SpanEntry, beta: SpanEntry, gamma: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta) && ValidSpan(gamma)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures S.Span(gamma.start, gamma.width) !=
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    SWD.SpanWellDefinedness(beta.start, beta.width);
    if S.Span(gamma.start, gamma.width) == S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width) {
      SWD.SpanWellDefinedness(alpha.start, alpha.width);
      IC.IntrinsicComparison(alpha.start, beta.start);
      assert alpha.start in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width);
      AlphaStartLtReachBeta(alpha, beta);
      IC.IntrinsicComparison(Reach(beta), Reach(beta));
      assert Reach(beta) in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width);
      CV.Convexity(gamma.start, gamma.width, alpha.start, beta.start, Reach(beta));
      assert false;
    }
  }

  // Case: only λ active (reach(β) == reach(α)).
  lemma LeftOnlyCorrect(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires Leq(Reach(beta), Reach(alpha))
    requires !LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures CollectiveDenotation(DifferenceBound(alpha, beta)) ==
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    LeftSpanValid(alpha, beta);
    var lambda := SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start));
    assert DifferenceBound(alpha, beta) == [lambda];
    assert Reach(lambda) == beta.start;
    assert Reach(beta) == Reach(alpha);
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert CollectiveDenotation(DifferenceBound(alpha, beta)) ==
           S.Span(lambda.start, lambda.width);

    // Forward: collective → diff
    forall t: Tumbler | t in CollectiveDenotation(DifferenceBound(alpha, beta))
      ensures t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
    {
      // t ∈ S.Span(lambda): alpha.start ≤ t < beta.start < Reach(beta) = Reach(alpha)
      LexTrans(t, beta.start, Reach(beta));
      IC.IntrinsicComparison(t, beta.start);
    }

    // Backward: diff → collective
    forall t: Tumbler | t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
      ensures t in CollectiveDenotation(DifferenceBound(alpha, beta))
    {
      IC.IntrinsicComparison(t, beta.start);
      if LexicographicOrder.LexicographicOrder(t, beta.start) {
        // t < beta.start = Reach(lambda) and alpha.start ≤ t → t ∈ S.Span(lambda)
        assert t in S.Span(lambda.start, lambda.width);
      } else if t == beta.start {
        assert false;
      } else {
        // beta.start < t; t ∉ S.Span(beta) → t ≥ Reach(beta) = Reach(alpha)
        IC.IntrinsicComparison(t, Reach(beta));
        if LexicographicOrder.LexicographicOrder(t, Reach(beta)) {
          assert false; // t < Reach(beta) → t ∈ S.Span(beta); contradiction
        } else {
          // t ≥ Reach(beta) = Reach(alpha); but t ∈ S.Span(alpha) needs t < Reach(alpha)
          IC.IntrinsicComparison(t, Reach(alpha));
          assert false;
        }
      }
    }
  }

  // Case: only ρ active (alpha.start == beta.start).
  lemma RightOnlyCorrect(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires Leq(alpha.start, beta.start)
    requires !LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures CollectiveDenotation(DifferenceBound(alpha, beta)) ==
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    RightSpanValid(alpha, beta);
    var rho := SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)));
    assert DifferenceBound(alpha, beta) == [rho];
    assert Reach(rho) == Reach(alpha);
    assert alpha.start == beta.start;
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert CollectiveDenotation(DifferenceBound(alpha, beta)) ==
           S.Span(rho.start, rho.width);

    // Forward: collective → diff
    forall t: Tumbler | t in CollectiveDenotation(DifferenceBound(alpha, beta))
      ensures t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
    {
      // t ∈ S.Span(rho): Reach(beta) ≤ t < Reach(alpha)
      // alpha.start = beta.start < Reach(beta) ≤ t → t ∈ S.Span(alpha)
      if Reach(beta) == t { } else { LexTrans(alpha.start, Reach(beta), t); }
      // t ≥ Reach(beta) → t ∉ S.Span(beta)
      IC.IntrinsicComparison(t, Reach(beta));
    }

    // Backward: diff → collective
    forall t: Tumbler | t in S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
      ensures t in CollectiveDenotation(DifferenceBound(alpha, beta))
    {
      // alpha.start = beta.start ≤ t; t ∉ S.Span(beta) → t ≥ Reach(beta)
      IC.IntrinsicComparison(t, Reach(beta));
      if LexicographicOrder.LexicographicOrder(t, Reach(beta)) {
        // beta.start ≤ t < Reach(beta) → t ∈ S.Span(beta); contradiction
        assert false;
      } else {
        // t ≥ Reach(beta) = rho.start and t < Reach(alpha) = Reach(rho) → t ∈ S.Span(rho)
        assert t in S.Span(rho.start, rho.width);
      }
    }
  }

  // Case: neither active (alpha = beta denotation-wise).
  lemma NeitherActiveCorrect(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires Leq(alpha.start, beta.start)
    requires !LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    requires Leq(Reach(beta), Reach(alpha))
    requires !LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures CollectiveDenotation(DifferenceBound(alpha, beta)) ==
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    assert DifferenceBound(alpha, beta) == [];
    assert alpha.start == beta.start;
    assert Reach(beta) == Reach(alpha);
    assert CollectiveDenotation(DifferenceBound(alpha, beta)) == iset{};
    assert S.Span(alpha.start, alpha.width) == S.Span(beta.start, beta.width) by {
      forall t: Tumbler
        ensures t in S.Span(alpha.start, alpha.width) <==> t in S.Span(beta.start, beta.width)
      { }
    }
  }

  // Axiom derivation: ⟦β⟧ ⊆ ⟦α⟧ implies the boundary conditions start(α) ≤ start(β) and reach(β) ≤ reach(α).
  lemma ContainmentToBoundary(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S.Span(beta.start, beta.width) <= S.Span(alpha.start, alpha.width)
    ensures Leq(alpha.start, beta.start)
    ensures Leq(Reach(beta), Reach(alpha))
  {
    // start bound: beta.start ∈ ⟦β⟧ ⊆ ⟦α⟧; membership in ⟦α⟧ yields alpha.start ≤ beta.start
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in S.Span(alpha.start, alpha.width);
    // reach bound: suppose Reach(alpha) < Reach(beta); then Reach(alpha) ∈ ⟦β⟧ ⊆ ⟦α⟧,
    // but Reach(alpha) is ⟦α⟧'s exclusive upper bound — contradiction via IC
    if !Leq(Reach(beta), Reach(alpha)) {
      IC.IntrinsicComparison(Reach(beta), Reach(alpha));
      IC.IntrinsicComparison(Reach(alpha), Reach(alpha));
      assert Reach(alpha) in S.Span(beta.start, beta.width);
      assert false;
    }
  }

  // S11 correctness: assembles the four cases.
  lemma DifferenceBoundCorrect(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires Leq(alpha.start, beta.start)
    requires Leq(Reach(beta), Reach(alpha))
    ensures CollectiveDenotation(DifferenceBound(alpha, beta)) ==
            S.Span(alpha.start, alpha.width) - S.Span(beta.start, beta.width)
  {
    var leftActive := LexicographicOrder.LexicographicOrder(alpha.start, beta.start);
    var rightActive := LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha));
    if      leftActive && rightActive  { BothActiveCorrect(alpha, beta); }
    else if leftActive                 { LeftOnlyCorrect(alpha, beta); }
    else if rightActive                { RightOnlyCorrect(alpha, beta); }
    else                               { NeitherActiveCorrect(alpha, beta); }
  }
}
