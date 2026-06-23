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

  // LexicographicOrder is strict: a < a is impossible
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
      // else: k = Length(a)+1 ≤ Length(a) → arithmetic contradiction
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
    // Extract LexicographicOrder witness; case (ii) is impossible when Length(a) = Length(b)
    var k: nat :| 1 <= k &&
      (forall i :: 1 <= i < k ==>
         i <= Length(a) && i <= Length(b) &&
         Component(a, i) == Component(b, i)) &&
      ((k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k))) ||
       (k == Length(a) + 1 && k <= Length(b)));
    // Case (ii) would give m+1 ≤ m, which is false
    assert k <= m;
    // Call FirstMismatch to expose its postconditions
    var fm := DivModule.FirstMismatch(a, b, 1, m);
    // By function transparency: Divergence(a,b) = FirstMismatch(a,b,1,m)
    assert DivModule.Divergence(a, b) == fm;
    // If fm > m: forall i :: 1 ≤ i < fm → Component(a,i) = Component(b,i)
    // In particular at i=k (k ≤ m < fm): Component(a,k) = Component(b,k)
    // But from witness: Less(Component(a,k), Component(b,k)) → contradiction
    if fm > m {
      assert 1 <= k && k < fm;
      assert Component(a, k) == Component(b, k);
      assert Less(Component(a, k), Component(b, k));
      assert Less(Component(a, k), Component(a, k));
      Irreflexive(Component(a, k));
    }
  }

  // WF: from s < r with equal length, (s, r⊖s) is valid and level-uniform with reach = r
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
    // beta.start ∈ ⟦β⟧ [T12 postcondition (b)]
    SWD.SpanWellDefinedness(beta.start, beta.width);
    assert beta.start in SpanSet(beta);
    // beta.start ∈ ⟦α⟧ [containment]
    assert beta.start in SpanSet(alpha);
    // Part 1: SpanSet membership unfolds to give alpha.start ≤ beta.start
    // Part 2: Reach(beta) ≤ Reach(alpha) — by contradiction
    if LexicographicOrder.LexicographicOrder(Reach(alpha), Reach(beta)) {
      var ra := Reach(alpha);
      var rb := Reach(beta);
      // From beta.start ∈ SpanSet(alpha): beta.start < Reach(alpha)
      assert LexicographicOrder.LexicographicOrder(
               beta.start, TumblerAdd.TumblerAdd(alpha.start, alpha.width));
      assert LexicographicOrder.LexicographicOrder(beta.start, ra);
      // Reach(alpha) ∈ SpanSet(beta): InT(ra), beta.start < ra < rb
      assert ra in SpanModule.Span(beta.start, beta.width);
      assert ra in SpanSet(beta);
      // From containment: Reach(alpha) ∈ SpanSet(alpha)
      assert ra in SpanSet(alpha);
      assert ra in SpanModule.Span(alpha.start, alpha.width);
      // SpanSet membership gives reach(alpha) < reach(alpha) — contradiction
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

  // λ is valid, level-uniform, and has reach(λ) = start(β)
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

  // ρ is valid, level-uniform, and has reach(ρ) = reach(α)
  lemma RhoWF(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures ValidSpan(RhoSpan(alpha, beta))
    ensures LevelUniform(RhoSpan(alpha, beta))
    ensures Reach(RhoSpan(alpha, beta)) == Reach(alpha)
  {
    // Level chain: Length(Reach(α)) = Length(α.width) = Length(α.start) = Length(β.start)
    //            = Length(β.width) = Length(Reach(β))
    assert Length(Reach(alpha)) == Length(alpha.start);
    assert Length(Reach(beta)) == Length(beta.start);
    WellFormedFromEndpoints(Reach(beta), Reach(alpha));
  }

  // S11 Theorem: ⟦α⟧ \ ⟦β⟧ = ⟦λ⟧ ∪ ⟦ρ⟧
  lemma DifferenceBoundTheorem(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires SpanSet(beta) <= SpanSet(alpha)
    ensures
      var lambdaSet :=
        if LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
        then SpanSet(LambdaSpan(alpha, beta)) else iset{};
      var rhoSet :=
        if LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
        then SpanSet(RhoSpan(alpha, beta)) else iset{};
      SpanSet(alpha) - SpanSet(beta) == lambdaSet + rhoSet
  {
  }
}
