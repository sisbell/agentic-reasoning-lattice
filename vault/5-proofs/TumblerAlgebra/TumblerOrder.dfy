// Order properties (ASN-0034): T0, T1, T2, T3, TA6
module TumblerOrder {
  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // T0(a) — UnboundedComponents
  // ---------------------------------------------------------------------------

  function WithComponent(t: Tumbler, i: nat, v: nat): Tumbler
    requires 0 <= i < |t.components|
    ensures |WithComponent(t, i, v).components| == |t.components|
    ensures WithComponent(t, i, v).components[i] == v
    ensures forall j :: 0 <= j < |t.components| && j != i ==>
              WithComponent(t, i, v).components[j] == t.components[j]
  {
    Tumbler(t.components[..i] + [v] + t.components[i+1..])
  }

  lemma UnboundedComponents(t: Tumbler, i: nat, M: nat)
    requires 0 <= i < |t.components|
    ensures exists t': Tumbler ::
      |t'.components| == |t.components| &&
      t'.components[i] > M &&
      (forall j :: 0 <= j < |t.components| && j != i ==>
         t'.components[j] == t.components[j])
  {
    var t' := WithComponent(t, i, M + 1);
  }

  // ---------------------------------------------------------------------------
  // T0(b) — UnboundedLength
  // ---------------------------------------------------------------------------

  function TumblerOfLength(n: nat): Tumbler
    requires n >= 1
    ensures |TumblerOfLength(n).components| == n
  {
    Tumbler(seq(n, _ => 1))
  }

  lemma UnboundedLength(n: nat)
    requires n >= 1
    ensures exists t: Tumbler :: |t.components| >= n
  {
    var t := TumblerOfLength(n);
  }

  // ---------------------------------------------------------------------------
  // T1 — LexicographicOrder (strict total order)
  // ---------------------------------------------------------------------------

  ghost predicate LexicographicOrder(a: Tumbler, b: Tumbler) {
    LessThan(a, b)
  }

  lemma Irreflexive(a: Tumbler)
    ensures !LexicographicOrder(a, a)
  { }

  lemma Transitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires LexicographicOrder(a, b)
    requires LexicographicOrder(b, c)
    ensures LexicographicOrder(a, c)
  {
    var k_ab: nat :| LessThanAt(a, b, k_ab);
    var k_bc: nat :| LessThanAt(b, c, k_bc);
    if k_ab <= k_bc {
      LessThanIntro(a, c, k_ab);
    } else {
      LessThanIntro(a, c, k_bc);
    }
  }

  lemma Asymmetric(a: Tumbler, b: Tumbler)
    requires LexicographicOrder(a, b)
    ensures !LexicographicOrder(b, a)
  {
    if LexicographicOrder(b, a) {
      Transitive(a, b, a);
      Irreflexive(a);
    }
  }

  lemma TotalScan(a: Tumbler, b: Tumbler, i: nat)
    requires a != b
    requires i <= |a.components| && i <= |b.components|
    requires forall j :: 0 <= j < i ==> a.components[j] == b.components[j]
    ensures LessThan(a, b) || LessThan(b, a)
    decreases (|a.components| - i) + (|b.components| - i)
  {
    if i == |a.components| && i < |b.components| {
      LessThanIntro(a, b, i);
    } else if i < |a.components| && i == |b.components| {
      LessThanIntro(b, a, i);
    } else if i < |a.components| && i < |b.components| {
      if a.components[i] < b.components[i] {
        LessThanIntro(a, b, i);
      } else if a.components[i] > b.components[i] {
        LessThanIntro(b, a, i);
      } else {
        TotalScan(a, b, i + 1);
      }
    }
  }

  lemma Total(a: Tumbler, b: Tumbler)
    requires a != b
    ensures LexicographicOrder(a, b) || LexicographicOrder(b, a)
  {
    TotalScan(a, b, 0);
  }

  // ---------------------------------------------------------------------------
  // T2 — IntrinsicComparison
  // ---------------------------------------------------------------------------

  ghost predicate IntrinsicComparison(a: Tumbler, b: Tumbler) {
    forall p: Tumbler, q: Tumbler ::
      |p.components| == |a.components| &&
      |q.components| == |b.components| &&
      (forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
        p.components[i] == a.components[i] && q.components[i] == b.components[i])
      ==> (LessThan(p, q) <==> LessThan(a, b))
  }

  lemma LessThanAtTransfer(a: Tumbler, b: Tumbler, p: Tumbler, q: Tumbler, k: nat)
    requires |p.components| == |a.components|
    requires |q.components| == |b.components|
    requires forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
      p.components[i] == a.components[i] && q.components[i] == b.components[i]
    requires LessThanAt(a, b, k)
    ensures LessThanAt(p, q, k)
  { }

  lemma IntrinsicComparisonHolds(a: Tumbler, b: Tumbler)
    ensures IntrinsicComparison(a, b)
  {
    forall p: Tumbler, q: Tumbler |
      |p.components| == |a.components| &&
      |q.components| == |b.components| &&
      (forall i :: 0 <= i < |a.components| && 0 <= i < |b.components| ==>
        p.components[i] == a.components[i] && q.components[i] == b.components[i])
      ensures LessThan(p, q) <==> LessThan(a, b)
    {
      if LessThan(a, b) {
        var k: nat :| LessThanAt(a, b, k);
        LessThanAtTransfer(a, b, p, q, k);
      }
      if LessThan(p, q) {
        var k: nat :| LessThanAt(p, q, k);
        LessThanAtTransfer(p, q, a, b, k);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // T3 — CanonicalRepresentation
  // ---------------------------------------------------------------------------

  ghost predicate ComponentEqual(a: Tumbler, b: Tumbler) {
    |a.components| == |b.components| &&
    forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i]
  }

  lemma CanonicalRepresentation(a: Tumbler, b: Tumbler)
    ensures ComponentEqual(a, b) <==> a == b
  { }

  // ---------------------------------------------------------------------------
  // TA6 — ZeroTumblerSentinel
  // ---------------------------------------------------------------------------

  ghost predicate IsZeroTumbler(t: Tumbler) {
    forall i :: 0 <= i < |t.components| ==> t.components[i] == 0
  }

  lemma ZeroNotValidAddress(t: Tumbler)
    requires IsZeroTumbler(t)
    ensures !PositiveTumbler(t)
  { }

  lemma ZeroLessThanPositive(s: Tumbler, t: Tumbler)
    requires IsZeroTumbler(s)
    requires PositiveTumbler(t)
    ensures LessThan(s, t)
  {
    var ap := ActionPoint(t);
    if |s.components| <= ap {
      LessThanIntro(s, t, |s.components|);
    } else {
      LessThanIntro(s, t, ap);
    }
  }
}
