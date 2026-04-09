include "./CarrierSetDefinition.dfy"

module AllocatorDisciplineNecessity {
  // T10a-N — AllocatorDisciplineNecessity (LEMMA from T1, TA5)
  // Necessity: relaxing the allocator discipline admits prefix-nested siblings.
  // Under the relaxed rule (any k ≥ 0 in sibling stream), a₁ = inc(b, 0)
  // and a₂ = inc(a₁, k') with k' > 0 satisfy a₁ ≺ a₂:
  // TA5(b): a₂ agrees with a₁ on all positions of a₁.
  // TA5(d): #a₂ = #a₁ + k' > #a₁.
  // This is T1 case (ii), violating the T10 precondition.

  import opened CarrierSetDefinition

  ghost predicate IsPrefix(p: Tumbler, q: Tumbler) {
    |p.components| <= |q.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == q.components[i]
  }

  // inc(t, 0): increment at last position (TA5c)
  function IncSibling(t: Tumbler): Tumbler
    requires ValidTumbler(t)
    ensures ValidTumbler(IncSibling(t))
    ensures |IncSibling(t).components| == |t.components|
  {
    var n := |t.components|;
    Tumbler(t.components[..n - 1] + [t.components[n - 1] + 1])
  }

  // inc(t, k) for k ≥ 1: extend by k positions (TA5d, structural only)
  function IncChildRaw(t: Tumbler, k: nat): Tumbler
    requires ValidTumbler(t)
    requires k >= 1
    ensures ValidTumbler(IncChildRaw(t, k))
    ensures |IncChildRaw(t, k).components| == |t.components| + k
  {
    Tumbler(t.components + seq(k - 1, _ => 0) + [1])
  }

  lemma AllocatorDisciplineNecessity(b: Tumbler, k: nat)
    requires ValidTumbler(b)
    requires k >= 1
    ensures IsPrefix(IncSibling(b), IncChildRaw(IncSibling(b), k))
    ensures IncSibling(b) != IncChildRaw(IncSibling(b), k)
  { }
}
