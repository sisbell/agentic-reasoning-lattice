include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module UnboundedComponents {

  import opened TumblerAlgebra

  // T0 — UnboundedComponents (INV, predicate(Tumbler))
  // axiom on carrier set

  // Constructive witness: replace component i with value v
  function WithComponent(t: Tumbler, i: nat, v: nat): Tumbler
    requires 0 <= i < |t.components|
    ensures |WithComponent(t, i, v).components| == |t.components|
    ensures WithComponent(t, i, v).components[i] == v
    ensures forall j :: 0 <= j < |t.components| && j != i ==>
              WithComponent(t, i, v).components[j] == t.components[j]
  {
    Tumbler(t.components[..i] + [v] + t.components[i+1..])
  }

  // Per-position unboundedness — also serves as trigger for outer quantifier
  ghost predicate UnboundedAt(t: Tumbler, i: int, M: int) {
    (0 <= i < |t.components| && M >= 0) ==>
    exists t': Tumbler ::
      |t'.components| == |t.components| &&
      t'.components[i] > M &&
      (forall j :: 0 <= j < |t.components| && j != i ==>
         t'.components[j] == t.components[j])
  }

  ghost predicate UnboundedComponents(t: Tumbler) {
    forall i, M :: UnboundedAt(t, i, M)
  }

  lemma UnboundedComponentsHolds(t: Tumbler)
    ensures UnboundedComponents(t)
  {
    forall i, M
      ensures UnboundedAt(t, i, M)
    {
      if 0 <= i < |t.components| && M >= 0 {
        var t' := WithComponent(t, i, M + 1);
      }
    }
  }
}
