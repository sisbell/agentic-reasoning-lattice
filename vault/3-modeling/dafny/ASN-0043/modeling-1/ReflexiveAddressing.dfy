include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerOrder.dfy"

// L13 — ReflexiveAddressing
// coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}
// Derived from L1, T1, T12.
module ReflexiveAddressing {
  import opened TumblerAlgebra
  import TumblerOrder

  // Unit displacement at depth n: n-1 zeros followed by 1
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

  // Inclusion: b ≼ c ==> b ≤ c < b ⊕ ℓ_b
  lemma Inclusion(b: Tumbler, c: Tumbler)
    requires |b.components| >= 1
    requires IsPrefix(b, c)
    ensures PositiveTumbler(UnitDisplacement(|b.components|))
    ensures ActionPoint(UnitDisplacement(|b.components|)) < |b.components|
    ensures LessEq(b, c)
    ensures LessThan(c, TumblerAdd(b, UnitDisplacement(|b.components|)))
  {
    UnitDisplacementPositive(|b.components|);
    if b != c {
      LessThanIntro(b, c, |b.components|);
    }
    LessThanIntro(c, TumblerAdd(b, UnitDisplacement(|b.components|)), |b.components| - 1);
  }

  // Exclusion: b ≤ t < b ⊕ ℓ_b ==> b ≼ t
  lemma Exclusion(b: Tumbler, t: Tumbler)
    requires |b.components| >= 1
    requires PositiveTumbler(UnitDisplacement(|b.components|))
    requires ActionPoint(UnitDisplacement(|b.components|)) < |b.components|
    requires LessEq(b, t)
    requires LessThan(t, TumblerAdd(b, UnitDisplacement(|b.components|)))
    ensures IsPrefix(b, t)
  { }

  // L13 — ReflexiveAddressing
  lemma ReflexiveAddressing(b: Tumbler, t: Tumbler)
    requires |b.components| >= 1
    ensures PositiveTumbler(UnitDisplacement(|b.components|))
    ensures ActionPoint(UnitDisplacement(|b.components|)) < |b.components|
    ensures IsPrefix(b, t) <==>
            (LessEq(b, t) && LessThan(t, TumblerAdd(b, UnitDisplacement(|b.components|))))
  {
    UnitDisplacementPositive(|b.components|);
    if IsPrefix(b, t) {
      Inclusion(b, t);
    }
    if LessEq(b, t) && LessThan(t, TumblerAdd(b, UnitDisplacement(|b.components|))) {
      Exclusion(b, t);
    }
  }
}
