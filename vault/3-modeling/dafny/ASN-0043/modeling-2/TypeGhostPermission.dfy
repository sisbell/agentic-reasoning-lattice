include "LinkStore.dfy"

// L9 — TypeGhostPermission
module TypeGhostPermission {
  import opened LinkStore
  import opened TumblerAlgebra
  import TumblerAddition

  // Unit-depth displacement: |ℓ| = n, zeros at 0..n-2, value 1 at n-1
  function UnitDepthDisplacement(n: nat): Tumbler
    requires n >= 1
    ensures |UnitDepthDisplacement(n).components| == n
  {
    Tumbler(Zeros(n - 1) + [1])
  }

  lemma UnitDepthPositive(n: nat)
    requires n >= 1
    ensures PositiveTumbler(UnitDepthDisplacement(n))
  {
    assert UnitDepthDisplacement(n).components[n - 1] == 1;
  }

  // DIVERGENCE: The ASN quantifies over all conforming states Σ and proves
  // Σ' preserves L0–L14. This model captures the structural core: given a
  // fresh ghost address g distinct from link address a, the type span
  // (g, ℓ_g) is well-formed and g lies in its coverage but outside all
  // entity stores. Invariant preservation requires modeling T9 and L0–L14.
  // Precondition a != g follows from L0/T7: g is in the content subspace,
  // a in the link subspace.
  lemma TypeGhostPermission(
    contentDom: set<Tumbler>,
    store: Store,
    g: Tumbler,
    a: Tumbler
  )
    requires |g.components| >= 1
    requires g !in contentDom
    requires g !in store
    requires a !in store
    requires a != g
    ensures WellFormedSpan(Span(g, UnitDepthDisplacement(|g.components|)))
    ensures LessThan(g, TumblerAdd(g, UnitDepthDisplacement(|g.components|)))
    ensures g !in store[a := Link({}, {}, {Span(g, UnitDepthDisplacement(|g.components|))})]
  {
    UnitDepthPositive(|g.components|);
    TumblerAddition.StrictIncrease(g, UnitDepthDisplacement(|g.components|));
  }
}
