include "./LexicographicOrder.dfy"

module ForwardAllocation {
  // T9 — ForwardAllocation (LEMMA, from T1, T10a, TA5)
  // Within a single allocator's sibling stream, each successive address
  // is strictly greater than its predecessor under T1.
  // (A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  // Sibling increment: inc(·, 0) increments the last component (T10a/TA5).
  // For T4-satisfying tumblers, sig(t) = last position, so this matches
  // TA5's inc(t, 0) with length preservation (TA5c).
  function SiblingInc(t: Tumbler): Tumbler
    requires ValidTumbler(t)
    ensures ValidTumbler(SiblingInc(t))
    ensures |SiblingInc(t).components| == |t.components|
  {
    var n := |t.components|;
    Tumbler(t.components[..n - 1] + [t.components[n - 1] + 1])
  }

  // TA5(a): each sibling increment is strictly increasing under T1.
  lemma SiblingIncStrictlyIncreasing(t: Tumbler)
    requires ValidTumbler(t)
    ensures LessThan(t, SiblingInc(t))
  { }

  // Allocator stream: base, then n applications of inc(·, 0).
  // Models T10a's constraint that siblings are produced exclusively by inc(·, 0).
  function AllocatorStream(base: Tumbler, n: nat): Tumbler
    requires ValidTumbler(base)
    ensures ValidTumbler(AllocatorStream(base, n))
    decreases n
  {
    if n == 0 then base
    else SiblingInc(AllocatorStream(base, n - 1))
  }

  // T9: Forward allocation — earlier allocations precede later ones.
  // Proof: each step is strictly increasing (TA5a), compose by transitivity (T1c).
  lemma ForwardAllocation(base: Tumbler, i: nat, j: nat)
    requires ValidTumbler(base)
    requires i < j
    ensures LessThan(AllocatorStream(base, i), AllocatorStream(base, j))
    decreases j - i
  {
    if j == i + 1 {
      SiblingIncStrictlyIncreasing(AllocatorStream(base, i));
    } else {
      ForwardAllocation(base, i, j - 1);
      SiblingIncStrictlyIncreasing(AllocatorStream(base, j - 1));
      LessThanTransitive(
        AllocatorStream(base, i),
        AllocatorStream(base, j - 1),
        AllocatorStream(base, j)
      );
    }
  }
}
