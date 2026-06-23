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

  // S3 theorem: ⟦α⟧ ∪ ⟦β⟧ = ⟦γ⟧
  lemma {:timeLimit 120} MergeEquivalenceTheorem(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    requires
      // overlap or adjacent: max(start) ≤ min(reach)
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

    // S6: all boundaries share the same length
    assert Length(s) == Length(alpha.start);
    assert Length(r) == Length(alpha.start);
    assert Length(s) == Length(r);

    // s < r: from TA-strict (start < reach) + transitivity + overlap for Case B1
    assert LexicographicOrder.LexicographicOrder(s, r) by {
      if IC.Compare(alpha.start, beta.start) != IC.GT {
        assert s == alpha.start;
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT {
          assert r == ReachOf(alpha);
          // s = start(α) < reach(α) = r from ReachOf ensures
        } else {
          assert r == ReachOf(beta);
          // s = start(α) < reach(α) < reach(β) = r
          SpanWD.LexicographicTransitive(s, ReachOf(alpha), r);
        }
      } else {
        // beta.start < alpha.start; overlap gives alpha.start ≤ reach(β)
        assert s == beta.start;
        assert LexicographicOrder.LexicographicOrder(s, alpha.start);
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT {
          assert r == ReachOf(alpha);
          // s < alpha.start ≤ reach(β) ≤ reach(α) = r
          if alpha.start == ReachOf(beta) {
            if ReachOf(beta) == r {
              SpanWD.LexicographicTransitive(s, alpha.start, r);
            } else {
              SpanWD.LexicographicTransitive(s, alpha.start, ReachOf(beta));
              SpanWD.LexicographicTransitive(s, ReachOf(beta), r);
            }
          } else {
            assert LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta));
            SpanWD.LexicographicTransitive(s, alpha.start, ReachOf(beta));
            if ReachOf(beta) == r {
            } else {
              SpanWD.LexicographicTransitive(s, ReachOf(beta), r);
            }
          }
        } else {
          assert r == ReachOf(beta);
          // s = beta.start < reach(β) = r from ReachOf ensures
        }
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

    var A := SpanModule.Span(alpha.start, alpha.length);
    var B := SpanModule.Span(beta.start, beta.length);
    var G := SpanModule.Span(gamma.start, gamma.length);

    // ⟦α⟧ ∪ ⟦β⟧ ⊆ ⟦γ⟧
    forall t | t in A + B ensures t in G {
      IC.IntrinsicComparison(alpha.start, beta.start);
      IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));
      if t in A {
        // s ≤ start(α) ≤ t
        if IC.Compare(alpha.start, beta.start) == IC.GT {
          assert s == beta.start;
          assert LexicographicOrder.LexicographicOrder(s, alpha.start);
          if alpha.start != t { SpanWD.LexicographicTransitive(s, alpha.start, t); }
        }
        // t < reach(α) ≤ r
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) == IC.LT {
          assert r == ReachOf(beta);
          SpanWD.LexicographicTransitive(t, ReachOf(alpha), r);
        }
        assert t in G;
      } else {
        // t in B: s ≤ start(β) ≤ t
        if IC.Compare(alpha.start, beta.start) == IC.LT {
          assert s == alpha.start;
          assert LexicographicOrder.LexicographicOrder(s, beta.start);
          if beta.start != t { SpanWD.LexicographicTransitive(s, beta.start, t); }
        }
        // t < reach(β) ≤ r
        if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.LT {
          assert r == ReachOf(alpha);
          SpanWD.LexicographicTransitive(t, ReachOf(beta), r);
        }
        assert t in G;
      }
    }

    // ⟦γ⟧ ⊆ ⟦α⟧ ∪ ⟦β⟧
    forall t | t in G ensures t in A + B {
      IC.IntrinsicComparison(alpha.start, beta.start);
      IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));

      if IC.Compare(alpha.start, beta.start) != IC.GT {
        // Case A: s = start(α); overlap gives beta.start ≤ reach(α)
        assert s == alpha.start;
        assert beta.start == ReachOf(alpha) ||
               LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha));
        IC.IntrinsicComparison(t, ReachOf(alpha));
        if IC.Compare(t, ReachOf(alpha)) == IC.LT {
          // A1: start(α) ≤ t < reach(α) → t ∈ A
          assert t in A;
        } else {
          // A2: t ≥ reach(α); r must be reach(β)
          if r == ReachOf(alpha) {
            if IC.Compare(t, ReachOf(alpha)) == IC.EQ {
              IC.IntrinsicComparison(t, r);
            } else {
              SpanWD.LexicographicTransitive(ReachOf(alpha), t, r);
              IC.IntrinsicComparison(ReachOf(alpha), r);
            }
          }
          assert r == ReachOf(beta);
          // beta.start ≤ reach(α) ≤ t (from overlap)
          if beta.start == ReachOf(alpha) {
            if IC.Compare(t, ReachOf(alpha)) == IC.EQ {
              assert beta.start == t;
            } else {
              assert LexicographicOrder.LexicographicOrder(beta.start, t);
            }
          } else {
            assert LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha));
            if IC.Compare(t, ReachOf(alpha)) == IC.EQ {
              assert LexicographicOrder.LexicographicOrder(beta.start, t);
            } else {
              SpanWD.LexicographicTransitive(beta.start, ReachOf(alpha), t);
            }
          }
          assert t in B;
        }
      } else {
        // Case B: s = start(β) < start(α); overlap gives alpha.start ≤ reach(β)
        assert s == beta.start;
        assert LexicographicOrder.LexicographicOrder(beta.start, alpha.start);
        assert alpha.start == ReachOf(beta) ||
               LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta));
        IC.IntrinsicComparison(t, ReachOf(beta));
        if IC.Compare(t, ReachOf(beta)) == IC.LT {
          // B1: start(β) ≤ t < reach(β) → t ∈ B
          assert t in B;
        } else {
          // B2: t ≥ reach(β); r must be reach(α)
          if r == ReachOf(beta) {
            if IC.Compare(t, ReachOf(beta)) == IC.EQ {
              IC.IntrinsicComparison(t, r);
            } else {
              SpanWD.LexicographicTransitive(ReachOf(beta), t, r);
              IC.IntrinsicComparison(ReachOf(beta), r);
            }
          }
          assert r == ReachOf(alpha);
          // alpha.start ≤ reach(β) ≤ t (from overlap)
          if alpha.start == ReachOf(beta) {
            if IC.Compare(t, ReachOf(beta)) == IC.EQ {
              assert alpha.start == t;
            } else {
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
          assert t in A;
        }
      }
    }

    assert G == A + B;
  }
}
