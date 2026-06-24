// ASN-0053: S3 — MergeEquivalence (DEF/theorem)
// s = min(start(α), start(β)), r = max(reach(α), reach(β)), γ = (s, r ⊖ s)
// Theorem: ⟦γ⟧ = ⟦α⟧ ∪ ⟦β⟧ for overlapping/adjacent level-uniform level-compat spans.
include "IntersectionClosure.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"

module MergeEquivalence {
  import opened IntersectionClosure
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import SpanModule = Span
  import SpanWD = SpanWellDefinedness
  import IC = IntrinsicComparison
  import DR = DisplacementRoundTrip

  // s = min(start(α), start(β))
  ghost function MergeStart(alpha: SpanValue, beta: SpanValue): Tumbler
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(MergeStart(alpha, beta))
    ensures MergeStart(alpha, beta) == alpha.start || MergeStart(alpha, beta) == beta.start
    ensures MergeStart(alpha, beta) ==
            (if IC.Compare(alpha.start, beta.start) != IC.GT then alpha.start else beta.start)
  {
    if IC.Compare(alpha.start, beta.start) != IC.GT then alpha.start else beta.start
  }

  // r = max(reach(α), reach(β))
  ghost function MergeReach(alpha: SpanValue, beta: SpanValue): Tumbler
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(MergeReach(alpha, beta))
    ensures MergeReach(alpha, beta) == ReachOf(alpha) || MergeReach(alpha, beta) == ReachOf(beta)
    ensures MergeReach(alpha, beta) ==
            (if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT then ReachOf(alpha) else ReachOf(beta))
  {
    if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT then ReachOf(alpha) else ReachOf(beta)
  }

  // DEF: γ = (s, r ⊖ s)
  ghost function MergeEquivalence(alpha: SpanValue, beta: SpanValue): (gamma: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LexicographicOrder.LexicographicOrder(MergeStart(alpha, beta), MergeReach(alpha, beta))
    ensures gamma.start == MergeStart(alpha, beta)
  {
    SpanValue(MergeStart(alpha, beta),
              TumblerSub.TumblerSub(MergeReach(alpha, beta), MergeStart(alpha, beta)))
  }

  // WF: from s < r with equal length, build valid level-uniform span with reach r
  lemma WellFormedFromEndpoints(s: Tumbler, r: Tumbler)
    requires InT(s) && InT(r)
    requires LexicographicOrder.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    ensures ValidSpan(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures LevelUniform(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures TumblerAdd.TumblerAdd(s, TumblerSub.TumblerSub(r, s)) == r
  {
    DR.LexImpliesNotEqual(s, r);
    EqualLengthDivergenceBound(s, r);
    DR.DisplacementRoundTrip(s, r);
  }

  // Forward: ⟦α⟧ ∪ ⟦β⟧ ⊆ ⟦γ⟧.
  // gamma.start = MergeStart, ReachOf(gamma) = MergeReach.
  lemma {:timeLimit 90} MergeContains(alpha: SpanValue, beta: SpanValue, gamma: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta) && ValidSpan(gamma)
    requires gamma.start == MergeStart(alpha, beta)
    requires ReachOf(gamma) == MergeReach(alpha, beta)
    ensures forall t | t in SpanModule.Span(alpha.start, alpha.length) +
                             SpanModule.Span(beta.start, beta.length)
            :: t in SpanModule.Span(gamma.start, gamma.length)
  {
    var s := gamma.start;
    var r := ReachOf(gamma);
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));
    forall t | t in SpanModule.Span(alpha.start, alpha.length) +
                    SpanModule.Span(beta.start, beta.length)
      ensures t in SpanModule.Span(gamma.start, gamma.length)
    {
      IC.IntrinsicComparison(alpha.start, beta.start);
      IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));
      if t in SpanModule.Span(alpha.start, alpha.length) {
        // Lower: s = gamma.start ≤ alpha.start ≤ t
        if IC.Compare(alpha.start, beta.start) == IC.GT {
          // s = beta.start < alpha.start; LexicographicOrder(s, alpha.start)
          assert LexicographicOrder.LexicographicOrder(s, alpha.start);
          if alpha.start != t { SpanWD.LexicographicTransitive(s, alpha.start, t); }
        }
        // Upper: t < reach(α) ≤ r = ReachOf(gamma)
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) == IC.LT {
          // r = reach(β) > reach(α); t < reach(α) → t < r by transitivity
          SpanWD.LexicographicTransitive(t, ReachOf(alpha), r);
        }
      } else {
        // t in Span(beta): s ≤ beta.start ≤ t
        if IC.Compare(alpha.start, beta.start) == IC.LT {
          // s = alpha.start < beta.start
          assert LexicographicOrder.LexicographicOrder(s, beta.start);
          if beta.start != t { SpanWD.LexicographicTransitive(s, beta.start, t); }
        }
        // Upper: t < reach(β) ≤ r = ReachOf(gamma)
        // Only IC.GT for reaches needs transitivity; IC.EQ gives r = reach(β), automatic
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) == IC.GT {
          // r = reach(α) > reach(β); t < reach(β) → t < r by transitivity
          SpanWD.LexicographicTransitive(t, ReachOf(beta), r);
        }
      }
    }
  }

  // Backward: ⟦γ⟧ ⊆ ⟦α⟧ ∪ ⟦β⟧.
  // Overlap condition: max(start) ≤ min(reach). Both inlined here.
  lemma {:timeLimit 90} MergeCovers(alpha: SpanValue, beta: SpanValue, gamma: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta) && ValidSpan(gamma)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    requires
      ((alpha.start == beta.start || LexicographicOrder.LexicographicOrder(alpha.start, beta.start)) &&
       (beta.start == ReachOf(alpha) || LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha))))
      ||
      (LexicographicOrder.LexicographicOrder(beta.start, alpha.start) &&
       (alpha.start == ReachOf(beta) || LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta))))
    requires gamma.start == MergeStart(alpha, beta)
    requires ReachOf(gamma) == MergeReach(alpha, beta)
    ensures forall t | t in SpanModule.Span(gamma.start, gamma.length)
            :: t in SpanModule.Span(alpha.start, alpha.length) +
                    SpanModule.Span(beta.start, beta.length)
  {
    var s := gamma.start;
    var r := ReachOf(gamma);
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));
    forall t | t in SpanModule.Span(gamma.start, gamma.length)
      ensures t in SpanModule.Span(alpha.start, alpha.length) +
                   SpanModule.Span(beta.start, beta.length)
    {
      IC.IntrinsicComparison(alpha.start, beta.start);
      IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));

      if IC.Compare(alpha.start, beta.start) != IC.GT {
        // Case A: s = alpha.start; overlap's first disjunct: beta.start ≤ reach(α)
        assert beta.start == ReachOf(alpha) ||
               LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha));
        IC.IntrinsicComparison(t, ReachOf(alpha));
        if IC.Compare(t, ReachOf(alpha)) == IC.LT {
          // A1: s = alpha.start ≤ t < reach(α) → t ∈ A
          assert t in SpanModule.Span(alpha.start, alpha.length);
        } else {
          // A2: t ≥ reach(α). r = reach(α) would mean t < r but t ≥ r — contradiction.
          if r == ReachOf(alpha) { assert false; }
          assert r == ReachOf(beta);
          // beta.start ≤ reach(α) ≤ t (from overlap + A2)
          if beta.start == ReachOf(alpha) {
            if IC.Compare(t, ReachOf(alpha)) == IC.GT {
              assert LexicographicOrder.LexicographicOrder(beta.start, t);
            }
            // else EQ: beta.start = reach(α) = t → beta.start == t ✓
          } else {
            assert LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha));
            if IC.Compare(t, ReachOf(alpha)) == IC.EQ {
              assert LexicographicOrder.LexicographicOrder(beta.start, t);
            } else {
              SpanWD.LexicographicTransitive(beta.start, ReachOf(alpha), t);
            }
          }
          assert t in SpanModule.Span(beta.start, beta.length);
        }
      } else {
        // Case B: s = beta.start < alpha.start; overlap's second disjunct: alpha.start ≤ reach(β)
        assert alpha.start == ReachOf(beta) ||
               LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta));
        IC.IntrinsicComparison(t, ReachOf(beta));
        if IC.Compare(t, ReachOf(beta)) == IC.LT {
          // B1: s = beta.start ≤ t < reach(β) → t ∈ B
          assert t in SpanModule.Span(beta.start, beta.length);
        } else {
          // B2: t ≥ reach(β). r = reach(β) would mean t < r but t ≥ r — contradiction.
          if r == ReachOf(beta) { assert false; }
          assert r == ReachOf(alpha);
          // alpha.start ≤ reach(β) ≤ t (from overlap + B2)
          if alpha.start == ReachOf(beta) {
            if IC.Compare(t, ReachOf(beta)) == IC.GT {
              assert LexicographicOrder.LexicographicOrder(alpha.start, t);
            }
          } else {
            assert LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta));
            if IC.Compare(t, ReachOf(beta)) == IC.EQ {
              assert LexicographicOrder.LexicographicOrder(alpha.start, t);
            } else {
              SpanWD.LexicographicTransitive(alpha.start, ReachOf(beta), t);
            }
          }
          assert t in SpanModule.Span(alpha.start, alpha.length);
        }
      }
    }
  }

  // S3 theorem: ⟦α⟧ ∪ ⟦β⟧ = ⟦γ⟧ where γ = (s, r ⊖ s)
  lemma {:timeLimit 60} MergeEquivalenceTheorem(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    requires
      ((alpha.start == beta.start || LexicographicOrder.LexicographicOrder(alpha.start, beta.start)) &&
       (beta.start == ReachOf(alpha) || LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha))))
      ||
      (LexicographicOrder.LexicographicOrder(beta.start, alpha.start) &&
       (alpha.start == ReachOf(beta) || LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta))))
    ensures
      var s := MergeStart(alpha, beta);
      var r := MergeReach(alpha, beta);
      exists gamma: SpanValue ::
        ValidSpan(gamma) && LevelUniform(gamma) &&
        gamma.start == s && ReachOf(gamma) == r &&
        SpanModule.Span(gamma.start, gamma.length) ==
          SpanModule.Span(alpha.start, alpha.length) +
          SpanModule.Span(beta.start, beta.length)
  {
    var s := MergeStart(alpha, beta);
    var r := MergeReach(alpha, beta);

    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));

    // S6: all boundaries have the same length
    assert Length(s) == Length(alpha.start);
    assert Length(r) == Length(alpha.start);
    assert Length(s) == Length(r);

    // s < r proof: case split on which start and which reach wins
    if IC.Compare(alpha.start, beta.start) != IC.GT {
      // Case A: s = alpha.start; s < reach(α) (from ValidSpan(alpha))
      assert s == alpha.start;
      if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT {
        // r = reach(α); s < reach(α) = r from ValidSpan(alpha)
        assert r == ReachOf(alpha);
        assert LexicographicOrder.LexicographicOrder(s, r);
      } else {
        // r = reach(β) > reach(α); s < reach(α) < r by transitivity
        assert r == ReachOf(beta);
        SpanWD.LexicographicTransitive(s, ReachOf(alpha), r);
        assert LexicographicOrder.LexicographicOrder(s, r);
      }
    } else {
      // Case B: s = beta.start; LexicographicOrder(s, alpha.start) from IC.GT
      assert s == beta.start;
      assert LexicographicOrder.LexicographicOrder(s, alpha.start);
      if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT {
        // r = reach(α); s < alpha.start ≤ reach(β) ≤ reach(α) = r
        assert r == ReachOf(alpha);
        if alpha.start == ReachOf(beta) {
          // s < alpha.start = reach(β); chain to r
          if ReachOf(beta) != r {
            // reach(β) < r = reach(α); LexicographicOrder(alpha.start, r) from IC.GT
            SpanWD.LexicographicTransitive(s, alpha.start, r);
          }
          // If reach(β) == r: LexicographicOrder(s, alpha.start = r) ✓ automatic
        } else {
          // LexicographicOrder(alpha.start, ReachOf(beta)) from overlap's second disjunct
          assert LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta));
          SpanWD.LexicographicTransitive(s, alpha.start, ReachOf(beta));
          if ReachOf(beta) != r {
            SpanWD.LexicographicTransitive(s, ReachOf(beta), r);
          }
        }
        assert LexicographicOrder.LexicographicOrder(s, r);
      } else {
        // r = reach(β); s < alpha.start ≤ reach(β) = r
        assert r == ReachOf(beta);
        if alpha.start == ReachOf(beta) {
          // s < alpha.start = r ✓ automatic from LexicographicOrder(s, alpha.start)
        } else {
          assert LexicographicOrder.LexicographicOrder(alpha.start, r);
          SpanWD.LexicographicTransitive(s, alpha.start, r);
        }
        assert LexicographicOrder.LexicographicOrder(s, r);
      }
    }

    // Construct γ = (s, r ⊖ s)
    WellFormedFromEndpoints(s, r);
    var w := TumblerSub.TumblerSub(r, s);
    var gamma := SpanValue(s, w);
    assert ValidSpan(gamma);
    assert LevelUniform(gamma);
    assert TumblerAdd.TumblerAdd(s, w) == r;
    assert ReachOf(gamma) == r;

    // Union equality via helper lemmas
    MergeContains(alpha, beta, gamma);
    MergeCovers(alpha, beta, gamma);
    assert SpanModule.Span(gamma.start, gamma.length) ==
           SpanModule.Span(alpha.start, alpha.length) +
           SpanModule.Span(beta.start, beta.length);
  }
}
