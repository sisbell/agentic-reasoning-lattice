// ASN-0053: S11 — DifferenceBound (DEF)
// For level-uniform spans α and β with LevelCompat and ⟦β⟧ ⊆ ⟦α⟧,
// ⟦α⟧ \ ⟦β⟧ is expressible as at most two spans:
//   λ = (start(α), start(β) ⊖ start(α))  when start(α) < start(β)
//   ρ = (reach(β), reach(α) ⊖ reach(β))  when reach(β) < reach(α)
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"

module DifferenceBound {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import opened NatStrictTotalOrder
  import SWD = SpanWellDefinedness
  import DRT = DisplacementRoundTrip
  import DivModule = Divergence
  import SpanModule = Span
  import IC = IntrinsicComparison

  datatype SpanValue = SpanValue(start: Tumbler, width: Tumbler)

  ghost predicate ValidSpan(sigma: SpanValue) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  predicate LevelUniform(sigma: SpanValue) {
    Length(sigma.start) == Length(sigma.width)
  }

  predicate LevelCompat(t1: Tumbler, t2: Tumbler) {
    Length(t1) == Length(t2)
  }

  ghost function Reach(sigma: SpanValue): (r: Tumbler)
    requires ValidSpan(sigma)
    ensures InT(r)
    ensures LexicographicOrder.LexicographicOrder(sigma.start, r)
    ensures Length(r) == Length(sigma.width)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.width)
  }

  ghost function SpanSet(sigma: SpanValue): iset<Tumbler>
    requires ValidSpan(sigma)
  {
    SpanModule.Span(sigma.start, sigma.width)
  }

  // LexicographicOrder is strict and irreflexive
  lemma LexOrderIrreflexive(a: Tumbler)
    requires InT(a)
    ensures !LexicographicOrder.LexicographicOrder(a, a)
  {
    if LexicographicOrder.LexicographicOrder(a, a) {
      var k: nat :| 1 <= k &&
        (forall i :: 1 <= i < k ==>
           i <= Length(a) && i <= Length(a) &&
           Component(a, i) == Component(a, i)) &&
        ((k <= Length(a) && k <= Length(a) &&
          Less(Component(a, k), Component(a, k))) ||
         (k == Length(a) + 1 && k <= Length(a)));
      if k <= Length(a) && Less(Component(a, k), Component(a, k)) {
        Irreflexive(Component(a, k));
      }
    }
  }

  // When a < b and Length(a) = Length(b), Divergence(a,b) ≤ Length(a)
  lemma EqualLengthDivergenceBound(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires Length(a) == Length(b)
    ensures DivModule.Divergence(a, b) <= Length(a)
  {
    DRT.LexImpliesNotEqual(a, b);
    var m := Length(a);
    var k: nat :| 1 <= k &&
      (forall i :: 1 <= i < k ==>
         i <= Length(a) && i <= Length(b) &&
         Component(a, i) == Component(b, i)) &&
      ((k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k))) ||
       (k == Length(a) + 1 && k <= Length(b)));
    assert k <= m;
    var fm := DivModule.FirstMismatch(a, b, 1, m);
    assert DivModule.Divergence(a, b) == fm;
    if fm > m {
      assert 1 <= k && k < fm;
      assert Component(a, k) == Component(b, k);
      assert Less(Component(a, k), Component(b, k));
      assert Less(Component(a, k), Component(a, k));
      Irreflexive(Component(a, k));
    }
  }

  // WF: from s < r with equal length, (s, r⊖s) is valid level-uniform with reach = r
  lemma WellFormedFromEndpoints(s: Tumbler, r: Tumbler)
    requires InT(s) && InT(r)
    requires LexicographicOrder.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    ensures ValidSpan(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures Length(TumblerSub.TumblerSub(r, s)) == Length(s)
    ensures TumblerAdd.TumblerAdd(s, TumblerSub.TumblerSub(r, s)) == r
  {
    EqualLengthDivergenceBound(s, r);
    DRT.DisplacementRoundTrip(s, r);
  }

  // Containment implies start(α) ≤ start(β) and reach(β) ≤ reach(α)
  lemma ContainmentBoundary(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires SpanSet(beta) <= SpanSet(alpha)
    ensures alpha.start == beta.start ||
            LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    ensures Reach(beta) == Reach(alpha) ||
            LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
  {
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in SpanSet(beta);
    assert beta.start in SpanSet(alpha);
    var ra := Reach(alpha);
    var rb := Reach(beta);
    IC.IntrinsicComparison(rb, ra);
    if IC.Compare(rb, ra) == IC.GT {
      assert LexicographicOrder.LexicographicOrder(ra, rb);
      assert LexicographicOrder.LexicographicOrder(
               beta.start, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
      assert LexicographicOrder.LexicographicOrder(beta.start, ra);
      assert ra in SpanModule.Span(beta.start, beta.width);
      assert ra in SpanSet(beta);
      assert ra in SpanSet(alpha);
      assert ra in SpanModule.Span(alpha.start, alpha.width);
      assert LexicographicOrder.LexicographicOrder(
               ra, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
      assert LexicographicOrder.LexicographicOrder(ra, ra);
      LexOrderIrreflexive(ra);
    }
  }

  // S11 DEF: λ = (start(α), start(β) ⊖ start(α))
  ghost function LambdaSpan(alpha: SpanValue, beta: SpanValue): SpanValue
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
  {
    SpanValue(alpha.start, TumblerSub.TumblerSub(beta.start, alpha.start))
  }

  // S11 DEF: ρ = (reach(β), reach(α) ⊖ reach(β))
  ghost function RhoSpan(alpha: SpanValue, beta: SpanValue): SpanValue
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
  {
    SpanValue(Reach(beta), TumblerSub.TumblerSub(Reach(alpha), Reach(beta)))
  }

  // S11 DEF: difference span-set — at most two spans
  ghost function DifferenceBound(alpha: SpanValue, beta: SpanValue): (result: seq<SpanValue>)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires SpanSet(beta) <= SpanSet(alpha)
    ensures |result| <= 2
  {
    var lp := if LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
              then [LambdaSpan(alpha, beta)] else [];
    var rp := if LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
              then [RhoSpan(alpha, beta)] else [];
    lp + rp
  }

  // λ is valid, level-uniform, with reach(λ) = start(β)
  lemma LambdaWF(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    ensures ValidSpan(LambdaSpan(alpha, beta))
    ensures LevelUniform(LambdaSpan(alpha, beta))
    ensures Reach(LambdaSpan(alpha, beta)) == beta.start
  {
    WellFormedFromEndpoints(alpha.start, beta.start);
  }

  // ρ is valid, level-uniform, with reach(ρ) = reach(α)
  lemma RhoWF(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures ValidSpan(RhoSpan(alpha, beta))
    ensures LevelUniform(RhoSpan(alpha, beta))
    ensures Reach(RhoSpan(alpha, beta)) == Reach(alpha)
  {
    assert Length(Reach(alpha)) == Length(alpha.start);
    assert Length(Reach(beta)) == Length(beta.start);
    WellFormedFromEndpoints(Reach(beta), Reach(alpha));
  }

  // Left interval predicate — InT(t) embedded to avoid precondition in forall ensures
  ghost predicate InLeftInterval(alpha: SpanValue, beta: SpanValue, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
  {
    InT(t) &&
    LexicographicOrder.LexicographicOrder(alpha.start, beta.start) &&
    (alpha.start == t || LexicographicOrder.LexicographicOrder(alpha.start, t)) &&
    LexicographicOrder.LexicographicOrder(t, beta.start)
  }

  // Right interval predicate — InT(t) embedded to avoid precondition in forall ensures
  ghost predicate InRightInterval(alpha: SpanValue, beta: SpanValue, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
  {
    InT(t) &&
    LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha)) &&
    (Reach(beta) == t || LexicographicOrder.LexicographicOrder(Reach(beta), t)) &&
    LexicographicOrder.LexicographicOrder(t, Reach(alpha))
  }

  // ⟹: t ∈ ⟦α⟧ \ ⟦β⟧ → left interval or right interval
  lemma DiffToInterval(alpha: SpanValue, beta: SpanValue, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires SpanSet(beta) <= SpanSet(alpha)
    requires InT(t)
    requires t in SpanSet(alpha)
    requires t !in SpanSet(beta)
    ensures InLeftInterval(alpha, beta, t) || InRightInterval(alpha, beta, t)
  {
    // Membership gives: alpha.start ≤ t < Reach(alpha)
    assert alpha.start == t || LexicographicOrder.LexicographicOrder(alpha.start, t);
    assert LexicographicOrder.LexicographicOrder(t, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
    // beta non-empty: beta.start < Reach(beta)
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in SpanSet(beta);
    assert LexicographicOrder.LexicographicOrder(beta.start, TumblerAdd.TumblerAdd(beta.start, beta.width));
    // Trichotomy on t vs beta.start
    IC.IntrinsicComparison(t, beta.start);
    if IC.Compare(t, beta.start) == IC.LT {
      // t < beta.start → LEFT: prove LexOrder(alpha.start, beta.start)
      if alpha.start == t {
        assert LexicographicOrder.LexicographicOrder(alpha.start, beta.start);
      } else {
        SWD.LexicographicTransitive(alpha.start, t, beta.start);
      }
      assert InLeftInterval(alpha, beta, t);
    } else if IC.Compare(t, beta.start) == IC.EQ {
      // t == beta.start → t ∈ ⟦β⟧ — contradiction with t !in SpanSet(beta)
      assert t == beta.start;
      assert t in SpanSet(beta);
    } else {
      // t > beta.start; trichotomy on t vs Reach(beta)
      assert LexicographicOrder.LexicographicOrder(beta.start, t);
      IC.IntrinsicComparison(t, TumblerAdd.TumblerAdd(beta.start, beta.width));
      if IC.Compare(t, TumblerAdd.TumblerAdd(beta.start, beta.width)) == IC.LT {
        // beta.start < t < Reach(beta) → t ∈ ⟦β⟧ — contradiction
        assert t in SpanModule.Span(beta.start, beta.width);
        assert t in SpanSet(beta);
      } else if IC.Compare(t, TumblerAdd.TumblerAdd(beta.start, beta.width)) == IC.EQ {
        // t == Reach(beta) < Reach(alpha) → RIGHT
        assert t == TumblerAdd.TumblerAdd(beta.start, beta.width);
        assert LexicographicOrder.LexicographicOrder(
                 TumblerAdd.TumblerAdd(beta.start, beta.width),
                 TumblerAdd.TumblerAdd(alpha.start, alpha.width));
        assert InRightInterval(alpha, beta, t);
      } else {
        // t > Reach(beta); trans → Reach(beta) < Reach(alpha)
        assert LexicographicOrder.LexicographicOrder(
                 TumblerAdd.TumblerAdd(beta.start, beta.width), t);
        SWD.LexicographicTransitive(
          TumblerAdd.TumblerAdd(beta.start, beta.width), t,
          TumblerAdd.TumblerAdd(alpha.start, alpha.width));
        assert InRightInterval(alpha, beta, t);
      }
    }
  }

  // ⟸ (left): t ∈ left interval → t ∈ ⟦α⟧ \ ⟦β⟧
  lemma LeftIntervalToDiff(alpha: SpanValue, beta: SpanValue, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires SpanSet(beta) <= SpanSet(alpha)
    requires InLeftInterval(alpha, beta, t)
    ensures t in SpanSet(alpha)
    ensures t !in SpanSet(beta)
  {
    // beta.start ∈ ⟦β⟧ ⊆ ⟦α⟧ → beta.start < Reach(alpha)
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in SpanSet(beta);
    assert beta.start in SpanSet(alpha);
    assert LexicographicOrder.LexicographicOrder(
             beta.start, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
    // t < beta.start < Reach(alpha) → t < Reach(alpha)
    SWD.LexicographicTransitive(t, beta.start, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
    // alpha.start ≤ t and t < Reach(alpha) → t ∈ ⟦α⟧
    assert t in SpanSet(alpha);
    // t ∉ ⟦β⟧: beta.start ≤ t contradicts t < beta.start
    if t in SpanSet(beta) {
      assert beta.start == t || LexicographicOrder.LexicographicOrder(beta.start, t);
      if beta.start == t {
        LexOrderIrreflexive(t);
      } else {
        SWD.LexicographicTransitive(beta.start, t, beta.start);
        LexOrderIrreflexive(beta.start);
      }
    }
  }

  // ⟸ (right): t ∈ right interval → t ∈ ⟦α⟧ \ ⟦β⟧
  lemma RightIntervalToDiff(alpha: SpanValue, beta: SpanValue, t: Tumbler)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires SpanSet(beta) <= SpanSet(alpha)
    requires InRightInterval(alpha, beta, t)
    ensures t in SpanSet(alpha)
    ensures t !in SpanSet(beta)
  {
    // beta non-empty: beta.start < Reach(beta)
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in SpanSet(beta);
    assert LexicographicOrder.LexicographicOrder(
             beta.start, TumblerAdd.TumblerAdd(beta.start, beta.width));
    // ContainmentBoundary: alpha.start ≤ beta.start
    ContainmentBoundary(alpha, beta);
    // alpha.start ≤ beta.start < Reach(beta) → alpha.start < Reach(beta)
    if alpha.start == beta.start {
      assert LexicographicOrder.LexicographicOrder(
               alpha.start, TumblerAdd.TumblerAdd(beta.start, beta.width));
    } else {
      SWD.LexicographicTransitive(
        alpha.start, beta.start, TumblerAdd.TumblerAdd(beta.start, beta.width));
    }
    // alpha.start < Reach(beta) ≤ t → alpha.start < t
    if TumblerAdd.TumblerAdd(beta.start, beta.width) == t {
      assert LexicographicOrder.LexicographicOrder(alpha.start, t);
    } else {
      assert LexicographicOrder.LexicographicOrder(TumblerAdd.TumblerAdd(beta.start, beta.width), t);
      SWD.LexicographicTransitive(
        alpha.start, TumblerAdd.TumblerAdd(beta.start, beta.width), t);
    }
    // alpha.start < t and t < Reach(alpha) → t ∈ ⟦α⟧
    assert LexicographicOrder.LexicographicOrder(alpha.start, t);
    assert LexicographicOrder.LexicographicOrder(t, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
    assert t in SpanSet(alpha);
    // t ∉ ⟦β⟧: Reach(beta) ≤ t but membership requires t < Reach(beta)
    if t in SpanSet(beta) {
      assert LexicographicOrder.LexicographicOrder(t, TumblerAdd.TumblerAdd(beta.start, beta.width));
      if TumblerAdd.TumblerAdd(beta.start, beta.width) == t {
        LexOrderIrreflexive(t);
      } else {
        assert LexicographicOrder.LexicographicOrder(TumblerAdd.TumblerAdd(beta.start, beta.width), t);
        SWD.LexicographicTransitive(
          TumblerAdd.TumblerAdd(beta.start, beta.width), t,
          TumblerAdd.TumblerAdd(beta.start, beta.width));
        LexOrderIrreflexive(TumblerAdd.TumblerAdd(beta.start, beta.width));
      }
    }
  }

  // S11 Theorem: ⟦α⟧ \ ⟦β⟧ = left interval ∪ right interval
  lemma DifferenceBoundTheorem(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires SpanSet(beta) <= SpanSet(alpha)
    ensures
      forall t ::
        (t in SpanSet(alpha) && t !in SpanSet(beta)) <==>
        (InLeftInterval(alpha, beta, t) || InRightInterval(alpha, beta, t))
  {
    forall t
      ensures (t in SpanSet(alpha) && t !in SpanSet(beta)) <==>
              (InLeftInterval(alpha, beta, t) || InRightInterval(alpha, beta, t))
    {
      if InT(t) {
        if t in SpanSet(alpha) && t !in SpanSet(beta) {
          DiffToInterval(alpha, beta, t);
        }
        if InLeftInterval(alpha, beta, t) {
          LeftIntervalToDiff(alpha, beta, t);
        }
        if InRightInterval(alpha, beta, t) {
          RightIntervalToDiff(alpha, beta, t);
        }
      } else {
        // !InT(t): iset Span requires InT so t ∉ SpanSet(anything)
        assert t !in SpanSet(alpha);
        assert !InLeftInterval(alpha, beta, t);
        assert !InRightInterval(alpha, beta, t);
      }
    }
  }
}
