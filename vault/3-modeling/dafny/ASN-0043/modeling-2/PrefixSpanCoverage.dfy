// PrefixSpanCoverage — ASN-0043
// Derived from T1, T5, T12
//
// For any tumbler x with |x.components| >= 1, the unit-depth span (x, ℓ_x)
// covers exactly the set {t : IsPrefix(x, t)}.

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerOrder.dfy"

module PrefixSpanCoverage {
  import opened TumblerAlgebra
  import TumblerOrder

  // Unit-depth displacement: [0, ..., 0, 1] with same length as x
  function UnitDepthDisplacement(x: Tumbler): Tumbler
    requires |x.components| >= 1
    ensures |UnitDepthDisplacement(x).components| == |x.components|
    ensures PositiveTumbler(UnitDepthDisplacement(x))
    ensures ActionPoint(UnitDepthDisplacement(x)) == |x.components| - 1
  {
    var n := |x.components|;
    var cs := Zeros(n - 1) + [1];
    assert cs[n - 1] == 1;
    Tumbler(cs)
  }

  // Inclusion: prefix implies in span [x, x ⊕ ℓ_x)
  lemma PrefixImpliesInSpan(x: Tumbler, t: Tumbler)
    requires |x.components| >= 1
    requires IsPrefix(x, t)
    ensures LessEq(x, t)
    ensures LessThan(t, TumblerAdd(x, UnitDepthDisplacement(x)))
  {
    var n := |x.components|;
    var ux := UnitDepthDisplacement(x);
    var end := TumblerAdd(x, ux);
    if x == t {
      LessThanIntro(t, end, n - 1);
    } else {
      LessThanIntro(x, t, n);
      LessThanIntro(t, end, n - 1);
    }
  }

  // Exclusion: in span implies prefix
  lemma InSpanImpliesPrefix(x: Tumbler, t: Tumbler)
    requires |x.components| >= 1
    requires LessEq(x, t)
    requires LessThan(t, TumblerAdd(x, UnitDepthDisplacement(x)))
    ensures IsPrefix(x, t)
  { }

  // PrefixSpanCoverage: coverage({(x, ℓ_x)}) = {t : IsPrefix(x, t)}
  lemma PrefixSpanCoverageLemma(x: Tumbler, t: Tumbler)
    requires |x.components| >= 1
    ensures IsPrefix(x, t) <==>
            (LessEq(x, t) && LessThan(t, TumblerAdd(x, UnitDepthDisplacement(x))))
  {
    if IsPrefix(x, t) {
      PrefixImpliesInSpan(x, t);
    }
    if LessEq(x, t) && LessThan(t, TumblerAdd(x, UnitDepthDisplacement(x))) {
      InSpanImpliesPrefix(x, t);
    }
  }
}
