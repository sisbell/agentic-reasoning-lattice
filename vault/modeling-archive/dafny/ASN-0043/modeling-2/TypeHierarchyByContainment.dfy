include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixSpanCoverage.dfy"

// L10 — TypeHierarchyByContainment
module TypeHierarchyByContainment {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import PrefixSpanCoverage

  // L10 — TypeHierarchyByContainment
  // A single span rooted at p covers all and only extensions of p.
  // By PrefixSpanCoverage: coverage({(p, ℓ_p)}) = {t : p ≼ t} = subtypes(p).
  // By T5: this set is contiguous under T1.
  lemma TypeHierarchyByContainment(p: Tumbler, t: Tumbler)
    requires |p.components| >= 1
    ensures IsPrefix(p, t) <==>
              (LessEq(p, t) &&
               LessThan(t, TumblerAdd(p, PrefixSpanCoverage.UnitDepthDisplacement(p))))
  {
    PrefixSpanCoverage.PrefixSpanCoverageLemma(p, t);
  }

  // Contiguity: subtypes(p) is a contiguous interval under T1 (T5)
  lemma SubtypesContiguous(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(p, a)
    requires IsPrefix(p, c)
    requires LessEq(a, b)
    requires LessEq(b, c)
    ensures IsPrefix(p, b)
  {
    TumblerHierarchy.ContiguousSubtrees(p, a, b, c);
  }
}
