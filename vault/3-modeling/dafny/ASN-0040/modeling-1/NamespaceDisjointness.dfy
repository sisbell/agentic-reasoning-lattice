include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module NamespaceDisjointness {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // B7 — NamespaceDisjointness
  // For distinct valid pairs (p, d) != (p', d'), S(p, d) ∩ S(p', d') = ∅.
  // Three cases: (1) different element lengths, (2) same parent length forces
  // p1 == p2 and d1 == d2, (3) zero-separator vs T4 last-component.

  ghost function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  predicate ValidBaptismDepth(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    (d == 1 || d == 2) &&
    TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
  }

  lemma NamespaceDisjointness(
    p1: Tumbler, d1: nat, p2: Tumbler, d2: nat,
    n1: nat, n2: nat
  )
    requires ValidBaptismDepth(p1, d1)
    requires ValidBaptismDepth(p2, d2)
    requires p1 != p2 || d1 != d2
    requires n1 >= 1 && n2 >= 1
    ensures StreamElement(p1, d1, n1) != StreamElement(p2, d2, n2)
  {
    if |p1.components| + d1 != |p2.components| + d2 {
      // Case 1: different element lengths (T3)
      assert |StreamElement(p1, d1, n1).components| != |StreamElement(p2, d2, n2).components|;
    } else if |p1.components| == |p2.components| {
      // Case 2: same parent length → d1 == d2 → p1 != p2
      assert d1 == d2;
      SameParentLengthCase(p1, d1, p2, d2, n1, n2);
    } else if |p1.components| < |p2.components| {
      ZeroSeparatorCase(p1, d1, p2, d2, n1, n2);
    } else {
      ZeroSeparatorCase(p2, d2, p1, d1, n2, n1);
    }
  }

  // Case 2: same parent length, same depth, different parents.
  // Elements differ because the parent prefix differs.
  lemma SameParentLengthCase(
    p1: Tumbler, d1: nat, p2: Tumbler, d2: nat,
    n1: nat, n2: nat
  )
    requires ValidBaptismDepth(p1, d1)
    requires ValidBaptismDepth(p2, d2)
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

  // Case 3: |ps| < |pl|, same element length → ds=2, dl=1, |pl|=|ps|+1.
  // At position |ps|: S(ps,2) has 0 (separator); S(pl,1) has pl's last component > 0 (T4).
  lemma ZeroSeparatorCase(
    ps: Tumbler, ds: nat, pl: Tumbler, dl: nat,
    ns: nat, nl: nat
  )
    requires ValidBaptismDepth(ps, ds)
    requires ValidBaptismDepth(pl, dl)
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
}
