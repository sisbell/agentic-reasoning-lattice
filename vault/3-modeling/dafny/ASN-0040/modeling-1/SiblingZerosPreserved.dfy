include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

module SiblingZerosPreserved {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import TumblerAllocation

  // B5a — SiblingZerosPreserved
  // (A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))
  // Sibling increment preserves zero count: it only changes a non-zero
  // component to another non-zero value, leaving all zeros untouched.

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

    // tc == (prefix + [tc[s]]) + suffix
    assert tc == prefix + [tc[s]] + suffix;
    TumblerAllocation.ZeroCountConcat(prefix, [tc[s]]);
    TumblerAllocation.ZeroCountConcat(prefix + [tc[s]], suffix);

    // rc == (prefix + [tc[s]+1]) + suffix
    assert rc == prefix + [tc[s] + 1] + suffix;
    TumblerAllocation.ZeroCountConcat(prefix, [tc[s] + 1]);
    TumblerAllocation.ZeroCountConcat(prefix + [tc[s] + 1], suffix);
  }
}
