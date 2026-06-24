// ASN-0053: S11c — DifferenceOverlap (DEF/lemma)
// For level-uniform spans α, β with level_compat in SC case (iii) (ProperOverlap):
// ⟦α⟧ \ ⟦β⟧ = ⟦γ⟧ for exactly one span γ.
// Case 1 (SA < SB): γ = (SA, SB ⊖ SA), reach(γ) = SB.
// Case 2 (SB < SA): γ' = (RB, RA ⊖ RB), reach(γ') = RA.
include "./SpanClassification.dfy"
include "./LevelConstraint.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module DifferenceOverlap {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import SC = SpanClassification
  import LC = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import TS = TumblerSub
  import IC = IntrinsicComparison
  import SWD = SpanWellDefinedness

  // Denotation equality for Case 1: SA < SB < RA < RB.
  // Witness g has g.start = SA and Reach(g) = SB.
  lemma Case1DenEqual(a: SpanEntry, b: SpanEntry, g: SpanEntry)
    requires ValidSpan(a) && ValidSpan(b) && ValidSpan(g)
    requires g.start == a.start
    requires Reach(g) == b.start
    requires LexicographicOrder.LexicographicOrder(a.start, b.start)
    requires LexicographicOrder.LexicographicOrder(b.start, Reach(a))
    requires LexicographicOrder.LexicographicOrder(Reach(a), Reach(b))
    ensures SC.Denotation(g) == SC.Denotation(a) - SC.Denotation(b)
  {
    forall t
      ensures t in SC.Denotation(g) <==>
              t in SC.Denotation(a) && t !in SC.Denotation(b)
    {
      if t in SC.Denotation(g) {
        // t ∈ g: a.start ≤ t, t < b.start (= Reach(g))
        // t ∈ a: t < b.start < Reach(a) by transitivity
        SWD.LexicographicTransitive(t, b.start, Reach(a));
        SC.InSpan(a, t);
        // t ∉ b: t < b.start, so NOT(b.start ≤ t)
        SC.LexOrderExcludes(t, b.start);
      } else if t in SC.Denotation(a) && t !in SC.Denotation(b) {
        // t < Reach(a) < Reach(b): establishes t < Reach(b)
        SWD.LexicographicTransitive(t, Reach(a), Reach(b));
        // t ∉ b with t < Reach(b): NOT(b.start ≤ t), hence t < b.start = Reach(g)
        IC.IntrinsicComparison(b.start, t);
        SC.InSpan(g, t);
      }
    }
  }

  // Denotation equality for Case 2: SB < SA < RB < RA.
  // Witness g has g.start = Reach(b) and Reach(g) = Reach(a).
  lemma Case2DenEqual(a: SpanEntry, b: SpanEntry, g: SpanEntry)
    requires ValidSpan(a) && ValidSpan(b) && ValidSpan(g)
    requires g.start == Reach(b)
    requires Reach(g) == Reach(a)
    requires LexicographicOrder.LexicographicOrder(b.start, a.start)
    requires LexicographicOrder.LexicographicOrder(a.start, Reach(b))
    requires LexicographicOrder.LexicographicOrder(Reach(b), Reach(a))
    ensures SC.Denotation(g) == SC.Denotation(a) - SC.Denotation(b)
  {
    forall t
      ensures t in SC.Denotation(g) <==>
              t in SC.Denotation(a) && t !in SC.Denotation(b)
    {
      if t in SC.Denotation(g) {
        // t ∈ g: Reach(b) ≤ t, t < Reach(a)
        // t ∈ a: SA < Reach(b) ≤ t → a.start ≤ t; t < Reach(g) = Reach(a)
        if g.start != t {
          SWD.LexicographicTransitive(a.start, Reach(b), t);
        }
        SC.InSpan(a, t);
        // t ∉ b: Reach(b) ≤ t, so NOT(t < Reach(b))
        IC.IntrinsicComparison(t, Reach(b));
        if t != Reach(b) {
          SC.LexOrderExcludes(Reach(b), t);
        }
      } else if t in SC.Denotation(a) && t !in SC.Denotation(b) {
        // SB < SA ≤ t → b.start ≤ t; from t ∉ b: NOT(t < Reach(b)), so Reach(b) ≤ t
        if a.start != t {
          SWD.LexicographicTransitive(b.start, a.start, t);
        }
        IC.IntrinsicComparison(t, Reach(b));
        SC.InSpan(g, t);
      }
    }
  }

  lemma DifferenceOverlap(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires LC.LevelUniform(alpha)
    requires LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires SC.SpanClassification(alpha, beta) == SC.ProperOverlap
    ensures exists gamma: SpanEntry ::
              ValidSpan(gamma) &&
              SC.Denotation(gamma) == SC.Denotation(alpha) - SC.Denotation(beta)
  {
    IC.IntrinsicComparison(Reach(alpha), beta.start);
    IC.IntrinsicComparison(Reach(beta), alpha.start);
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(beta.start, alpha.start);
    IC.IntrinsicComparison(Reach(alpha), Reach(beta));
    IC.IntrinsicComparison(Reach(beta), Reach(alpha));

    // Extract SB < RA: else SpanClassification would be Separated or Adjacent
    assert IC.Compare(Reach(alpha), beta.start) == IC.GT by {
      if IC.Compare(Reach(alpha), beta.start) == IC.LT {
        assert SC.SpanClassification(alpha, beta) == SC.Separated; assert false;
      } else if IC.Compare(Reach(alpha), beta.start) == IC.EQ {
        if IC.Compare(Reach(beta), alpha.start) == IC.LT {
          assert SC.SpanClassification(alpha, beta) == SC.Separated; assert false;
        } else {
          assert SC.SpanClassification(alpha, beta) == SC.Adjacent; assert false;
        }
      }
    }
    assert LexicographicOrder.LexicographicOrder(beta.start, Reach(alpha));

    // Extract SA < RB: else SpanClassification would be Separated or Adjacent
    assert IC.Compare(Reach(beta), alpha.start) == IC.GT by {
      if IC.Compare(Reach(beta), alpha.start) == IC.LT {
        assert SC.SpanClassification(alpha, beta) == SC.Separated; assert false;
      } else if IC.Compare(Reach(beta), alpha.start) == IC.EQ {
        assert SC.SpanClassification(alpha, beta) == SC.Adjacent; assert false;
      }
    }
    assert LexicographicOrder.LexicographicOrder(alpha.start, Reach(beta));

    if IC.Compare(alpha.start, beta.start) == IC.LT {
      // Case 1: SA < SB; need RA < RB (else Containment)
      assert LexicographicOrder.LexicographicOrder(alpha.start, beta.start);
      assert IC.Compare(Reach(beta), Reach(alpha)) == IC.GT by {
        if IC.Compare(Reach(beta), Reach(alpha)) != IC.GT {
          assert SC.SpanClassification(alpha, beta) == SC.Containment; assert false;
        }
      }
      assert LexicographicOrder.LexicographicOrder(Reach(alpha), Reach(beta));
      var gamma := SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start));
      WF.WellFormedSpanFromEndpoints(alpha.start, beta.start);
      Case1DenEqual(alpha, beta, gamma);
    } else if IC.Compare(alpha.start, beta.start) == IC.EQ {
      // SA == SB → Equal or Containment, never ProperOverlap
      if IC.Compare(Reach(alpha), Reach(beta)) == IC.EQ {
        assert SC.SpanClassification(alpha, beta) == SC.Equal; assert false;
      } else {
        assert SC.SpanClassification(alpha, beta) == SC.Containment; assert false;
      }
    } else {
      // Case 2: SB < SA; need RB < RA (else Containment)
      assert IC.Compare(alpha.start, beta.start) == IC.GT;
      assert LexicographicOrder.LexicographicOrder(beta.start, alpha.start);
      assert IC.Compare(Reach(alpha), Reach(beta)) == IC.GT by {
        if IC.Compare(Reach(alpha), Reach(beta)) != IC.GT {
          assert SC.SpanClassification(alpha, beta) == SC.Containment; assert false;
        }
      }
      assert LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha));
      LC.LevelConstraint(alpha);
      LC.LevelConstraint(beta);
      var gamma := SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)));
      WF.WellFormedSpanFromEndpoints(Reach(beta), Reach(alpha));
      Case2DenEqual(alpha, beta, gamma);
    }
  }
}
