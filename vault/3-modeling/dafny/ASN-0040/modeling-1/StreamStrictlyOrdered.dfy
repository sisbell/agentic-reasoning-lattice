include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StreamStrictlyOrdered {
  import opened TumblerAlgebra

  // S0 — StreamStrictlyOrdered
  // (A i, j : 1 ≤ i < j : cᵢ < cⱼ)
  // where c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0)

  // Closed form of sibling stream S(p, d):
  //   c₁ = inc(p, d) = [p ++ zeros(d-1) ++ 1]
  //   cₙ₊₁ = inc(cₙ, 0) increments the last component
  // So cₙ = [p ++ zeros(d-1) ++ n].
  // Equivalence to the recursive AllocationInc definition proved below.
  ghost function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  lemma StreamStrictlyOrderedLemma(p: Tumbler, d: nat, i: nat, j: nat)
    requires d >= 1
    requires 1 <= i < j
    ensures LessThan(StreamElement(p, d, i), StreamElement(p, d, j))
  {
    LessThanIntro(StreamElement(p, d, i), StreamElement(p, d, j), |p.components| + d - 1);
  }

  // Equivalence: closed form matches the recursive AllocationInc definition
  lemma StreamMatchesInc(p: Tumbler, d: nat, n: nat)
    requires PositiveTumbler(p)
    requires |p.components| > 0
    requires d >= 1
    requires n >= 1
    ensures StreamElement(p, d, 1) == AllocationInc(p, d)
    ensures n >= 2 ==>
      PositiveTumbler(StreamElement(p, d, n - 1)) &&
      |StreamElement(p, d, n - 1).components| > 0 &&
      StreamElement(p, d, n) == AllocationInc(StreamElement(p, d, n - 1), 0)
  {
    if n >= 2 {
      var prev := StreamElement(p, d, n - 1);
      var last := |prev.components| - 1;
      assert prev.components[last] == n - 1;
      LastNonzeroAt(prev, last);
    }
  }
}
