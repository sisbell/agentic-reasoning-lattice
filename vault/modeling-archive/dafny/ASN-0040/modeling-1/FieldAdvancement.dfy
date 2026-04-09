include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

module FieldAdvancement {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import TumblerAllocation

  // B5 — FieldAdvancement
  // zeros(inc(p, d)) = zeros(p) + (d − 1)

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
}
