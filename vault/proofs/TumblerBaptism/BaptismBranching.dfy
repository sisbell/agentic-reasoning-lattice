// Branching properties (ASN-0040): S0, S1, B5, B5a, B7
// Structure of the fork — what a parent produces when it baptizes children.
module BaptismBranching {
  import opened TumblerAlgebra
  import opened TumblerBaptism
  import TumblerHierarchy
  import TumblerAllocation

  // ---------------------------------------------------------------------------
  // S0 — StreamStrictlyOrdered
  // ---------------------------------------------------------------------------

  lemma StreamStrictlyOrdered(p: Tumbler, d: nat, i: nat, j: nat)
    requires d >= 1
    requires 1 <= i < j
    ensures LessThan(StreamElement(p, d, i), StreamElement(p, d, j))
  {
    LessThanIntro(StreamElement(p, d, i), StreamElement(p, d, j), |p.components| + d - 1);
  }

  // ---------------------------------------------------------------------------
  // S1 — StreamExtendsParent
  // ---------------------------------------------------------------------------

  lemma StreamExtendsParent(p: Tumbler, d: nat, n: nat)
    requires d >= 1
    requires n >= 1
    ensures IsPrefix(p, StreamElement(p, d, n))
  { }

  // ---------------------------------------------------------------------------
  // B5 — FieldAdvancement
  // ---------------------------------------------------------------------------

  lemma ZeroCountZeros(n: nat)
    ensures TumblerHierarchy.ZeroCount(Zeros(n)) == n
    decreases n
  {
    if n == 0 {
    } else {
      assert Zeros(n)[1..] == Zeros(n - 1);
      ZeroCountZeros(n - 1);
    }
  }

  lemma FieldAdvancement(p: Tumbler, d: nat)
    requires PositiveTumbler(p)
    requires |p.components| > 0
    requires d >= 1
    ensures TumblerHierarchy.ZeroCount(AllocationInc(p, d).components) ==
            TumblerHierarchy.ZeroCount(p.components) + (d - 1)
  {
    var pc := p.components;
    var zs := Zeros(d - 1);
    var tail := zs + [1];
    assert AllocationInc(p, d).components == pc + tail;
    TumblerAllocation.ZeroCountConcat(pc, tail);
    TumblerAllocation.ZeroCountConcat(zs, [1]);
    ZeroCountZeros(d - 1);
  }

  // ---------------------------------------------------------------------------
  // B5a — SiblingZerosPreserved
  // ---------------------------------------------------------------------------

  lemma SiblingZerosPreserved(t: Tumbler)
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures TumblerHierarchy.ZeroCount(AllocationInc(t, 0).components) ==
            TumblerHierarchy.ZeroCount(t.components)
  {
    var s := LastNonzero(t);
    var tc := t.components;
    var rc := AllocationInc(t, 0).components;
    var prefix := tc[..s];
    var suffix := tc[s+1..];
    assert tc == prefix + [tc[s]] + suffix;
    TumblerAllocation.ZeroCountConcat(prefix, [tc[s]]);
    TumblerAllocation.ZeroCountConcat(prefix + [tc[s]], suffix);
    assert rc == prefix + [tc[s] + 1] + suffix;
    TumblerAllocation.ZeroCountConcat(prefix, [tc[s] + 1]);
    TumblerAllocation.ZeroCountConcat(prefix + [tc[s] + 1], suffix);
  }

  // ---------------------------------------------------------------------------
  // B7 — NamespaceDisjointness
  // ---------------------------------------------------------------------------

  lemma SameParentLengthCase(
    p1: Tumbler, d1: nat, p2: Tumbler, d2: nat,
    n1: nat, n2: nat
  )
    requires ValidBaptism(p1, d1)
    requires ValidBaptism(p2, d2)
    requires |p1.components| == |p2.components|
    requires d1 == d2
    requires p1 != p2
    requires n1 >= 1 && n2 >= 1
    ensures StreamElement(p1, d1, n1) != StreamElement(p2, d2, n2)
  {
    var e1 := StreamElement(p1, d1, n1);
    var e2 := StreamElement(p2, d2, n2);
    var len := |p1.components|;
    assert e1.components[..len] == p1.components;
    assert e2.components[..len] == p2.components;
  }

  lemma ZeroSeparatorCase(
    ps: Tumbler, ds: nat, pl: Tumbler, dl: nat,
    ns: nat, nl: nat
  )
    requires ValidBaptism(ps, ds)
    requires ValidBaptism(pl, dl)
    requires |ps.components| < |pl.components|
    requires |ps.components| + ds == |pl.components| + dl
    requires ns >= 1 && nl >= 1
    ensures StreamElement(ps, ds, ns) != StreamElement(pl, dl, nl)
  {
    var k := |ps.components|;
    assert ds == 2 && dl == 1;
    var es := StreamElement(ps, ds, ns);
    var el := StreamElement(pl, dl, nl);
    assert es.components[k] == 0;
    assert el.components[k] == pl.components[k];
    assert pl.components[k] != 0;
  }

  lemma NamespaceDisjointness(
    p1: Tumbler, d1: nat, p2: Tumbler, d2: nat,
    n1: nat, n2: nat
  )
    requires ValidBaptism(p1, d1)
    requires ValidBaptism(p2, d2)
    requires p1 != p2 || d1 != d2
    requires n1 >= 1 && n2 >= 1
    ensures StreamElement(p1, d1, n1) != StreamElement(p2, d2, n2)
  {
    if |p1.components| + d1 != |p2.components| + d2 {
      assert |StreamElement(p1, d1, n1).components| != |StreamElement(p2, d2, n2).components|;
    } else if |p1.components| == |p2.components| {
      assert d1 == d2;
      SameParentLengthCase(p1, d1, p2, d2, n1, n2);
    } else if |p1.components| < |p2.components| {
      ZeroSeparatorCase(p1, d1, p2, d2, n1, n2);
    } else {
      ZeroSeparatorCase(p2, d2, p1, d1, n2, n1);
    }
  }
}
