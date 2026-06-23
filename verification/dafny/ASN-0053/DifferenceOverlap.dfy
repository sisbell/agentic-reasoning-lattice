// ASN-0053: S11c — DifferenceOverlap (DEF/lemma)
// SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is exactly 1 span.
// Case 1: start(α) < start(β) < reach(α) < reach(β)  →  γ = (start(α), start(β) ⊖ start(α))
// Case 2: start(β) < start(α) < reach(β) < reach(α)  →  γ' = (reach(β), reach(α) ⊖ reach(β))
include "IntersectionClosure.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"

module DifferenceOverlap {
  import opened IntersectionClosure
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import SpanModule = Span
  import SpanWD = SpanWellDefinedness
  import IC = IntrinsicComparison
  import DR = DisplacementRoundTrip

  // From s < r with Length(s) == Length(r), produce a valid level-uniform span with reach = r.
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

  lemma DifferenceOverlap(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    requires
      (LexicographicOrder.LexicographicOrder(alpha.start, beta.start) &&
       LexicographicOrder.LexicographicOrder(beta.start, ReachOf(alpha)) &&
       LexicographicOrder.LexicographicOrder(ReachOf(alpha), ReachOf(beta))) ||
      (LexicographicOrder.LexicographicOrder(beta.start, alpha.start) &&
       LexicographicOrder.LexicographicOrder(alpha.start, ReachOf(beta)) &&
       LexicographicOrder.LexicographicOrder(ReachOf(beta), ReachOf(alpha)))
    ensures
      exists gamma: SpanValue ::
        ValidSpan(gamma) &&
        SpanModule.Span(gamma.start, gamma.length) ==
        SpanModule.Span(alpha.start, alpha.length) - SpanModule.Span(beta.start, beta.length)
  {
    var A := SpanModule.Span(alpha.start, alpha.length);
    var B := SpanModule.Span(beta.start, beta.length);

    if LexicographicOrder.LexicographicOrder(alpha.start, beta.start) {
      // Case 1: start(α) < start(β) < reach(α) < reach(β)
      WellFormedFromEndpoints(alpha.start, beta.start);
      var w := TumblerSub.TumblerSub(beta.start, alpha.start);
      var gamma := SpanValue(alpha.start, w);
      var G := SpanModule.Span(gamma.start, gamma.length);
      assert TumblerAdd.TumblerAdd(alpha.start, w) == beta.start;

      // A \ B ⊆ G: every t ∈ α \ β satisfies start(α) ≤ t < start(β)
      forall t | t in A && t !in B ensures t in G {
        IC.IntrinsicComparison(t, beta.start);
        if IC.Compare(t, beta.start) != IC.LT {
          // beta.start ≤ t; t < reach(α) < reach(β), so t ∈ β — contradicts t !∈ β
          SpanWD.LexicographicTransitive(t, ReachOf(alpha), ReachOf(beta));
          assert t in B;
        }
        assert t in G;
      }

      // G ⊆ A \ B: every t with start(α) ≤ t < start(β) lies in α but not β
      forall t | t in G ensures t in A && t !in B {
        // t < start(β) < reach(α), so t ∈ α
        SpanWD.LexicographicTransitive(t, beta.start, ReachOf(alpha));
        assert t in A;
        // t < start(β) prevents t ∈ β
        if t in B {
          assert t == beta.start || LexicographicOrder.LexicographicOrder(beta.start, t);
          IC.IntrinsicComparison(t, beta.start);
        }
      }

      assert A - B == G;

    } else {
      // Case 2: start(β) < start(α) < reach(β) < reach(α)
      // Establish Length(reach(β)) == Length(reach(α)) for WellFormedFromEndpoints
      assert Length(ReachOf(alpha)) == Length(alpha.length);
      assert Length(ReachOf(beta)) == Length(beta.length);
      assert Length(alpha.start) == Length(alpha.length);
      assert Length(beta.start) == Length(beta.length);
      // Chain: Length(reach(β)) = Length(β.length) = Length(β.start) = Length(α.start) = Length(α.length) = Length(reach(α))
      assert Length(ReachOf(beta)) == Length(ReachOf(alpha));

      WellFormedFromEndpoints(ReachOf(beta), ReachOf(alpha));
      var w := TumblerSub.TumblerSub(ReachOf(alpha), ReachOf(beta));
      var gamma := SpanValue(ReachOf(beta), w);
      var G := SpanModule.Span(gamma.start, gamma.length);
      assert TumblerAdd.TumblerAdd(ReachOf(beta), w) == ReachOf(alpha);

      // A \ B ⊆ G: every t ∈ α \ β satisfies reach(β) ≤ t < reach(α)
      forall t | t in A && t !in B ensures t in G {
        IC.IntrinsicComparison(t, ReachOf(beta));
        if IC.Compare(t, ReachOf(beta)) == IC.LT {
          // t < reach(β); show β.start < t, giving t ∈ β — contradiction
          if t == alpha.start {
            // β.start < α.start = t (Case 2 precondition)
            assert LexicographicOrder.LexicographicOrder(beta.start, t);
          } else {
            // α.start < t (from t ∈ α, t ≠ α.start); β.start < α.start → β.start < t
            SpanWD.LexicographicTransitive(beta.start, alpha.start, t);
          }
          assert t in B;
        }
        assert t in G;
      }

      // G ⊆ A \ B: every t with reach(β) ≤ t < reach(α) lies in α but not β
      forall t | t in G ensures t in A && t !in B {
        // α.start < reach(β) ≤ t (Case 2), so α.start < t, giving t ∈ α
        if t == ReachOf(beta) {
          // α.start < reach(β) = t
          assert LexicographicOrder.LexicographicOrder(alpha.start, t);
        } else {
          // reach(β) < t; α.start < reach(β) → α.start < t
          SpanWD.LexicographicTransitive(alpha.start, ReachOf(beta), t);
        }
        assert t in A;
        // t ≥ reach(β) prevents t ∈ β
        if t in B {
          assert LexicographicOrder.LexicographicOrder(t, ReachOf(beta));
          assert t == ReachOf(beta) || LexicographicOrder.LexicographicOrder(ReachOf(beta), t);
          IC.IntrinsicComparison(t, ReachOf(beta));
        }
      }

      assert A - B == G;
    }
  }
}
