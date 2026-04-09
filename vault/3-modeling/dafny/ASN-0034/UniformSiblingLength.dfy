include "./AllocatorDiscipline.dfy"

module UniformSiblingLength {
  // T10a.1 — UniformSiblingLength (LEMMA)
  // Corollary of T10a, TA5: inc(·, 0) preserves length,
  // so all siblings produced under the allocator discipline
  // have uniform length.

  import opened AllocatorDiscipline

  // The n-th sibling: t₀, t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), …
  function NthSibling(t0: Tumbler, n: nat): Tumbler
    requires ValidTumbler(t0)
    ensures ValidTumbler(NthSibling(t0, n))
    decreases n
  {
    if n == 0 then t0
    else IncSibling(NthSibling(t0, n - 1))
  }

  lemma UniformSiblingLength(t0: Tumbler, n: nat)
    requires ValidTumbler(t0)
    ensures |NthSibling(t0, n).components| == |t0.components|
    decreases n
  {
    if n == 0 {
    } else {
      UniformSiblingLength(t0, n - 1);
    }
  }
}
