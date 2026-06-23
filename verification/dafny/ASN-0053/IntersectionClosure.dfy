// ASN-0053: S1 — IntersectionClosure (DEF)
// s' = max(start(α), start(β)), r' = min(reach(α), reach(β))
// γ = (s', r' ⊖ s'); intersection is non-empty iff r' > s'
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"
include "../ASN-0034/Divergence.dfy"

module IntersectionClosure {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import SpanModule = Span
  import SpanWD = SpanWellDefinedness
  import IC = IntrinsicComparison
  import DR = DisplacementRoundTrip
  import Div = Divergence

  datatype SpanValue = SpanValue(start: Tumbler, length: Tumbler)

  ghost predicate ValidSpan(sigma: SpanValue) {
    InT(sigma.start) &&
    InT(sigma.length) &&
    PositiveTumbler.PositiveTumbler(sigma.length) &&
    ActionPoint.ActionPoint(sigma.length) <= Length(sigma.start)
  }

  ghost predicate LevelUniform(sigma: SpanValue)
    requires ValidSpan(sigma)
  {
    Length(sigma.start) == Length(sigma.length)
  }

  function ReachOf(sigma: SpanValue): Tumbler
    requires ValidSpan(sigma)
    ensures InT(ReachOf(sigma))
    ensures Length(ReachOf(sigma)) == Length(sigma.length)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.length)
  }

  // s' = max(start(α), start(β)) — uses IC.Compare (non-ghost) in body
  ghost function IntersectionStart(alpha: SpanValue, beta: SpanValue): Tumbler
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(IntersectionStart(alpha, beta))
    ensures IntersectionStart(alpha, beta) == alpha.start ||
            IntersectionStart(alpha, beta) == beta.start
    ensures IntersectionStart(alpha, beta) ==
            (if IC.Compare(alpha.start, beta.start) != IC.GT then beta.start else alpha.start)
  {
    if IC.Compare(alpha.start, beta.start) != IC.GT
    then beta.start
    else alpha.start
  }

  // r' = min(reach(α), reach(β)) — uses IC.Compare (non-ghost) in body
  ghost function IntersectionReach(alpha: SpanValue, beta: SpanValue): Tumbler
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(IntersectionReach(alpha, beta))
    ensures IntersectionReach(alpha, beta) == ReachOf(alpha) ||
            IntersectionReach(alpha, beta) == ReachOf(beta)
    ensures IntersectionReach(alpha, beta) ==
            (if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.GT then ReachOf(alpha) else ReachOf(beta))
  {
    if IC.Compare(ReachOf(alpha), ReachOf(beta)) != IC.GT
    then ReachOf(alpha)
    else ReachOf(beta)
  }

  // For equal-length distinct tumblers, Divergence(a, b) ≤ Length(a)
  lemma EqualLengthDivergenceBound(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) == Length(b)
    requires a != b
    ensures Div.Divergence(a, b) <= Length(a)
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    assert m == Length(a);
    var d := Div.Divergence(a, b);
    assert d == Div.FirstMismatch(a, b, 1, m);
    if d > m {
      assert d == m + 1;
      assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);
      Extensionality(a, b);
    }
  }

  // S1 (theorem): the intersection of two level-uniform level-compatible spans
  // is either empty or a single span
  lemma IntersectionClosure(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    ensures
      var I := SpanModule.Span(alpha.start, alpha.length) *
               SpanModule.Span(beta.start, beta.length);
      (forall t: Tumbler :: !(t in I)) ||
      exists gamma: SpanValue ::
        ValidSpan(gamma) &&
        SpanModule.Span(gamma.start, gamma.length) == I
  {
    var sPrime := IntersectionStart(alpha, beta);
    var rPrime := IntersectionReach(alpha, beta);
    var I := SpanModule.Span(alpha.start, alpha.length) *
             SpanModule.Span(beta.start, beta.length);

    // Derive ordering facts about sPrime from trichotomy on starts
    IC.IntrinsicComparison(alpha.start, beta.start);
    if IC.Compare(alpha.start, beta.start) == IC.GT {
      assert sPrime == alpha.start;
      assert LexicographicOrder.LexicographicOrder(beta.start, alpha.start);
      assert alpha.start == sPrime || LexicographicOrder.LexicographicOrder(alpha.start, sPrime);
      assert beta.start == sPrime || LexicographicOrder.LexicographicOrder(beta.start, sPrime);
    } else {
      assert sPrime == beta.start;
      assert alpha.start == sPrime || LexicographicOrder.LexicographicOrder(alpha.start, sPrime);
      assert beta.start == sPrime || LexicographicOrder.LexicographicOrder(beta.start, sPrime);
    }
    assert alpha.start == sPrime || LexicographicOrder.LexicographicOrder(alpha.start, sPrime);
    assert beta.start == sPrime || LexicographicOrder.LexicographicOrder(beta.start, sPrime);

    // Derive ordering facts about rPrime from trichotomy on reaches
    IC.IntrinsicComparison(ReachOf(alpha), ReachOf(beta));
    if IC.Compare(ReachOf(alpha), ReachOf(beta)) == IC.GT {
      assert rPrime == ReachOf(beta);
      assert LexicographicOrder.LexicographicOrder(ReachOf(beta), ReachOf(alpha));
      assert rPrime == ReachOf(alpha) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(alpha));
      assert rPrime == ReachOf(beta) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(beta));
    } else {
      assert rPrime == ReachOf(alpha);
      assert rPrime == ReachOf(alpha) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(alpha));
      assert rPrime == ReachOf(beta) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(beta));
    }
    assert rPrime == ReachOf(alpha) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(alpha));
    assert rPrime == ReachOf(beta) || LexicographicOrder.LexicographicOrder(rPrime, ReachOf(beta));

    // S6: all four boundary tumblers share one length
    assert Length(ReachOf(alpha)) == Length(alpha.start);
    assert Length(ReachOf(beta)) == Length(beta.start);
    if sPrime == alpha.start {
      assert Length(sPrime) == Length(alpha.start);
    } else {
      assert sPrime == beta.start;
      assert Length(sPrime) == Length(alpha.start);
    }
    if rPrime == ReachOf(alpha) {
      assert Length(rPrime) == Length(alpha.start);
    } else {
      assert rPrime == ReachOf(beta);
      assert Length(rPrime) == Length(alpha.start);
    }
    assert Length(sPrime) == Length(rPrime);

    if sPrime == rPrime || LexicographicOrder.LexicographicOrder(rPrime, sPrime) {
      // Empty case: forward inclusion + rPrime ≤ sPrime forces I = ∅
      forall t: Tumbler | t in I
        ensures false
      {
        // Lower bound: sPrime ≤ t
        if sPrime == alpha.start {
          assert t == sPrime || LexicographicOrder.LexicographicOrder(sPrime, t);
        } else {
          assert sPrime == beta.start;
          assert t == sPrime || LexicographicOrder.LexicographicOrder(sPrime, t);
        }
        // Upper bound: t < rPrime
        if rPrime == ReachOf(alpha) {
          assert LexicographicOrder.LexicographicOrder(t, rPrime);
        } else {
          assert rPrime == ReachOf(beta);
          assert LexicographicOrder.LexicographicOrder(t, rPrime);
        }
        // rPrime ≤ sPrime ≤ t and t < rPrime → contradiction
        if sPrime == rPrime {
          if t == sPrime {
            IC.IntrinsicComparison(sPrime, sPrime);
          } else {
            IC.IntrinsicComparison(sPrime, t);
          }
        } else {
          SpanWD.LexicographicTransitive(t, rPrime, sPrime);
          if t == sPrime {
            IC.IntrinsicComparison(sPrime, sPrime);
          } else {
            IC.IntrinsicComparison(sPrime, t);
          }
        }
      }
    } else {
      // Non-empty case: sPrime < rPrime
      IC.IntrinsicComparison(sPrime, rPrime);
      assert IC.Compare(sPrime, rPrime) == IC.LT;
      assert LexicographicOrder.LexicographicOrder(sPrime, rPrime);
      DR.LexImpliesNotEqual(sPrime, rPrime);
      EqualLengthDivergenceBound(sPrime, rPrime);
      DR.DisplacementRoundTrip(sPrime, rPrime);
      var w := TumblerSub.TumblerSub(rPrime, sPrime);
      assert TumblerAdd.TumblerAdd(sPrime, w) == rPrime;
      assert Length(w) == Length(sPrime);
      var gamma := SpanValue(sPrime, w);
      assert ValidSpan(gamma);
      assert LevelUniform(gamma);

      // Span(gamma) ⊆ I
      forall t: Tumbler | t in SpanModule.Span(gamma.start, gamma.length)
        ensures t in I
      {
        assert LexicographicOrder.LexicographicOrder(t, TumblerAdd.TumblerAdd(gamma.start, gamma.length));
        assert LexicographicOrder.LexicographicOrder(t, rPrime);
        // t ∈ Span(alpha): alpha.start ≤ sPrime ≤ t and t < rPrime ≤ ReachOf(alpha)
        if alpha.start == sPrime {
        } else if t == sPrime {
        } else {
          SpanWD.LexicographicTransitive(alpha.start, sPrime, t);
        }
        if rPrime == ReachOf(alpha) {
        } else {
          SpanWD.LexicographicTransitive(t, rPrime, ReachOf(alpha));
        }
        assert t in SpanModule.Span(alpha.start, alpha.length);
        // t ∈ Span(beta): symmetrically
        if beta.start == sPrime {
        } else if t == sPrime {
        } else {
          SpanWD.LexicographicTransitive(beta.start, sPrime, t);
        }
        if rPrime == ReachOf(beta) {
        } else {
          SpanWD.LexicographicTransitive(t, rPrime, ReachOf(beta));
        }
        assert t in SpanModule.Span(beta.start, beta.length);
      }

      // I ⊆ Span(gamma)
      forall t: Tumbler | t in I
        ensures t in SpanModule.Span(gamma.start, gamma.length)
      {
        // Lower: sPrime ≤ t (from sPrime = max of starts)
        if sPrime == alpha.start {
          assert t == sPrime || LexicographicOrder.LexicographicOrder(sPrime, t);
        } else {
          assert sPrime == beta.start;
          assert t == sPrime || LexicographicOrder.LexicographicOrder(sPrime, t);
        }
        // Upper: t < rPrime = TumblerAdd(sPrime, w)
        if rPrime == ReachOf(alpha) {
          assert LexicographicOrder.LexicographicOrder(t, rPrime);
        } else {
          assert rPrime == ReachOf(beta);
          assert LexicographicOrder.LexicographicOrder(t, rPrime);
        }
        assert t in SpanModule.Span(gamma.start, gamma.length);
      }

      assert SpanModule.Span(gamma.start, gamma.length) == I;
    }
  }
}
