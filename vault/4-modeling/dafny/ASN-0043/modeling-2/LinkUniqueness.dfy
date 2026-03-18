include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerOrder.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

// L11a — LinkUniqueness
module LinkUniqueness {
  import opened TumblerAlgebra
  import TumblerOrder
  import TumblerAllocation

  // DIVERGENCE: The ASN derives L11a from T9 (forward allocation) and
  // GlobalUniqueness as a system-level property over all allocation events.
  // The Dafny model delegates to GlobalUniqueness's structural core: given
  // that the allocation system provides one of three discriminants, a ≠ b
  // follows. The T9 forward-allocation protocol is not modeled. The
  // IntrinsicComparison conclusion captures "reduces to tumbler comparison."
  lemma LinkUniqueness(a: Tumbler, b: Tumbler, pa: Tumbler, pb: Tumbler)
    requires IsPrefix(pa, a) && IsPrefix(pb, b)
    requires
      (LessThan(a, b) || LessThan(b, a))
      ||
      (!IsPrefix(pa, pb) && !IsPrefix(pb, pa))
      ||
      |a.components| != |b.components|
    ensures a != b
    ensures TumblerOrder.IntrinsicComparison(a, b)
  {
    TumblerOrder.IntrinsicComparisonHolds(a, b);
  }
}
