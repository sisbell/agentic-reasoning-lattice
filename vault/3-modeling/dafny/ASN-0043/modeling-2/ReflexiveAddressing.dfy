include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixSpanCoverage.dfy"

// L13 — ReflexiveAddressing
module ReflexiveAddressing {
  import opened TumblerAlgebra
  import TumblerAddition
  import TumblerHierarchy
  import PrefixSpanCoverage

  // L13 — ReflexiveAddressing
  // For any element-level address b, the unit-depth span (b, ℓ_b) is
  // well-formed by T12 and covers exactly {t : b ≼ t}. In particular,
  // b itself is in the coverage — every link can be referenced by address.
  lemma ReflexiveAddressing(b: Tumbler)
    requires TumblerHierarchy.ElementAddress(b)
    ensures TumblerAddition.SpanWellDefined(b, PrefixSpanCoverage.UnitDepthDisplacement(b))
    ensures LessEq(b, b)
    ensures LessThan(b, TumblerAdd(b, PrefixSpanCoverage.UnitDepthDisplacement(b)))
  {
    PrefixSpanCoverage.PrefixImpliesInSpan(b, b);
  }

  // Coverage characterization: t is in [b, b ⊕ ℓ_b) iff b ≼ t
  lemma ReflexiveAddressingCoverage(b: Tumbler, t: Tumbler)
    requires TumblerHierarchy.ElementAddress(b)
    ensures IsPrefix(b, t) <==>
            (LessEq(b, t) &&
             LessThan(t, TumblerAdd(b, PrefixSpanCoverage.UnitDepthDisplacement(b))))
  {
    PrefixSpanCoverage.PrefixSpanCoverageLemma(b, t);
  }
}
