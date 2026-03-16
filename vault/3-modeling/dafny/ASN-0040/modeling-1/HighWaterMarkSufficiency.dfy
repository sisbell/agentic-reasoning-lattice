include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// B2 — HighWaterMarkSufficiency
// next(B, p, d) = c_{hwm(B,p,d) + 1}
module HighWaterMarkSufficiency {
  import opened TumblerAlgebra

  // Closed-form n-th element of sibling stream S(p, d)
  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // B2 — HighWaterMarkSufficiency
  // Given B1 (children form a contiguous prefix of size m = hwm),
  // the next address to allocate is c_{m+1}.
  //
  // hwm = 0: next = inc(p, d) = c_1           (first child)
  // hwm = m > 0: next = inc(c_m, 0) = c_{m+1} (next sibling of greatest)
  //
  // Derived from B1: the contiguous-prefix invariant ensures
  // max(children) = c_m, reducing next to the stream recurrence.
  lemma HighWaterMarkSufficiency(p: Tumbler, d: nat, m: nat)
    requires PositiveTumbler(p) && |p.components| > 0
    requires d >= 1
    ensures m == 0 ==> AllocationInc(p, d) == StreamElement(p, d, 1)
    ensures m >= 1 ==>
      PositiveTumbler(StreamElement(p, d, m)) &&
      |StreamElement(p, d, m).components| > 0 &&
      AllocationInc(StreamElement(p, d, m), 0) == StreamElement(p, d, m + 1)
  {
    if m >= 1 {
      var se := StreamElement(p, d, m);
      assert se.components[|se.components| - 1] == m;
    }
  }
}
