// Addition properties (ASN-0034): TA0, TA1, TA-strict, TA1-strict, TA1-weak,
// T12, TA7a
module TumblerAddition {
  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // TA0 — WellDefinedAddition
  // ---------------------------------------------------------------------------

  ghost predicate AdditionPrecondition(a: Tumbler, w: Tumbler) {
    PositiveTumbler(w) &&
    ActionPoint(w) < |a.components|
  }

  lemma WellDefinedAddition(a: Tumbler, w: Tumbler)
    requires AdditionPrecondition(a, w)
    ensures |TumblerAdd(a, w).components| == |w.components|
    ensures |TumblerAdd(a, w).components| >= 1
  { }

  // ---------------------------------------------------------------------------
  // TA1 — AdditionAssociative
  // ---------------------------------------------------------------------------

  lemma AdditionAssociative(a: Tumbler, b: Tumbler, c: Tumbler)
    requires PositiveTumbler(b)
    requires PositiveTumbler(c)
    requires ActionPoint(b) < |a.components|
    requires ActionPoint(c) < |b.components|
    ensures PositiveTumbler(TumblerAdd(b, c))
    ensures ActionPoint(TumblerAdd(b, c)) < |a.components|
    ensures TumblerAdd(TumblerAdd(a, b), c) == TumblerAdd(a, TumblerAdd(b, c))
  {
    var kb := ActionPoint(b);
    var kc := ActionPoint(c);
    var bc := TumblerAdd(b, c);
    assert bc.components[kc] != 0;
    if kb <= kc {
      assert bc.components[kb] != 0;
    }
  }

  // ---------------------------------------------------------------------------
  // TA-strict — StrictIncrease (a ⊕ w > a)
  // ---------------------------------------------------------------------------

  lemma StrictIncrease(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    ensures LessThan(a, TumblerAdd(a, w))
  {
    var k := ActionPoint(w);
    var r := TumblerAdd(a, w);
    LessThanIntro(a, r, k);
  }

  // ---------------------------------------------------------------------------
  // TA1-strict — AdditionStrictOrder (a < b → a ⊕ w < b ⊕ w)
  // ---------------------------------------------------------------------------

  lemma AdditionStrictOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    requires LessThan(a, b)
    requires exists d :: 0 <= d <= ActionPoint(w) &&
               d < |a.components| && d < |b.components| &&
               a.components[d] != b.components[d] &&
               (forall j :: 0 <= j < d ==> a.components[j] == b.components[j])
    ensures LessThan(TumblerAdd(a, w), TumblerAdd(b, w))
  {
    var k :| LessThanAt(a, b, k);
    LessThanIntro(TumblerAdd(a, w), TumblerAdd(b, w), k);
  }

  // ---------------------------------------------------------------------------
  // TA1-weak — AdditionWeakOrder (a < b → a ⊕ w ≤ b ⊕ w)
  // ---------------------------------------------------------------------------

  lemma AdditionWeakOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    ensures LessEq(TumblerAdd(a, w), TumblerAdd(b, w))
  {
    var ap := ActionPoint(w);
    var k :| LessThanAt(a, b, k);
    if k > ap {
      assert TumblerAdd(a, w) == TumblerAdd(b, w);
    } else {
      LessThanIntro(TumblerAdd(a, w), TumblerAdd(b, w), k);
    }
  }

  // ---------------------------------------------------------------------------
  // T12 — SpanWellDefined
  // ---------------------------------------------------------------------------

  ghost predicate SpanWellDefined(s: Tumbler, l: Tumbler) {
    PositiveTumbler(l) &&
    ActionPoint(l) < |s.components|
  }

  lemma SpanNonEmpty(s: Tumbler, l: Tumbler)
    requires SpanWellDefined(s, l)
    ensures LessThan(s, TumblerAdd(s, l))
  {
    var k := ActionPoint(l);
    var r := TumblerAdd(s, l);
    LessThanIntro(s, r, k);
  }

  // ---------------------------------------------------------------------------
  // TA7a — SubspaceClosure
  // ---------------------------------------------------------------------------

  lemma AdditionClosure(x: nat, n: nat)
    requires x > 0
    requires n > 0
    ensures PositiveTumbler(Tumbler([n]))
    ensures TumblerAdd(Tumbler([x]), Tumbler([n])) == Tumbler([x + n])
    ensures PositiveTumbler(Tumbler([x + n]))
  {
    assert Tumbler([n]).components[0] != 0;
    assert Tumbler([x + n]).components[0] != 0;
  }

  lemma SubtractionClosure(x: nat, n: nat)
    requires x > 0
    requires n > 0
    requires x >= n
    ensures Subtractable(Tumbler([x]), Tumbler([n]))
    ensures TumblerSubtract(Tumbler([x]), Tumbler([n])) == Tumbler([x - n])
    ensures x > n ==> PositiveTumbler(Tumbler([x - n]))
  {
    if x > n {
      assert Tumbler([x - n]).components[0] != 0;
    }
  }
}
