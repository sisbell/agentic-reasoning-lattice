include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// L10 — TypeHierarchyByContainment
// Every extension of prefix p falls within coverage of span (p, UnitDisplacement(|p|)).
// A single span query rooted at p matches every subtype of p.
// Derived from T1, T5.
module TypeHierarchyByContainment {
  import opened TumblerAlgebra

  // Construct the unit displacement at depth n: n-1 zeros followed by 1.
  // Action point is n-1; TumblerAdd(p, UnitDisplacement(n)) increments the
  // last component of p by 1.
  function UnitDisplacement(n: nat): Tumbler
    requires n >= 1
  {
    Tumbler(Zeros(n - 1) + [1])
  }

  lemma UnitDisplacementPositive(n: nat)
    requires n >= 1
    ensures PositiveTumbler(UnitDisplacement(n))
    ensures ActionPoint(UnitDisplacement(n)) == n - 1
  {
    assert UnitDisplacement(n).components[n - 1] == 1;
  }

  // L10 — TypeHierarchyByContainment
  // For any prefix p with |p| >= 1 and any c extending p:
  //   p <= c < p ⊕ UnitDisplacement(|p|)
  lemma TypeHierarchyByContainment(p: Tumbler, c: Tumbler)
    requires |p.components| >= 1
    requires IsPrefix(p, c)
    ensures LessEq(p, c)
    ensures PositiveTumbler(UnitDisplacement(|p.components|))
    ensures ActionPoint(UnitDisplacement(|p.components|)) < |p.components|
    ensures LessThan(c, TumblerAdd(p, UnitDisplacement(|p.components|)))
  {
    var n := |p.components|;
    UnitDisplacementPositive(n);
    var w := UnitDisplacement(n);
    var q := TumblerAdd(p, w);

    // p <= c
    if p != c {
      LessThanIntro(p, c, n);
    }

    // c < p ⊕ w
    LessThanIntro(c, q, n - 1);
  }
}
