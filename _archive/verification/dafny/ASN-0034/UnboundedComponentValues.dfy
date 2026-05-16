include "./CarrierSetDefinition.dfy"

module UnboundedComponentValues {
  // T0(a) — UnboundedComponentValues
  // (A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))

  import opened CarrierSetDefinition

  function WithComponent(t: Tumbler, i: nat, v: nat): Tumbler
    requires 0 <= i < |t.components|
    ensures |WithComponent(t, i, v).components| == |t.components|
    ensures WithComponent(t, i, v).components[i] == v
    ensures forall j :: 0 <= j < |t.components| && j != i ==>
              WithComponent(t, i, v).components[j] == t.components[j]
  {
    Tumbler(t.components[..i] + [v] + t.components[i+1..])
  }

  lemma UnboundedComponentValues(t: Tumbler, i: nat, M: nat)
    requires ValidTumbler(t)
    requires 0 <= i < |t.components|
    ensures exists t': Tumbler ::
      ValidTumbler(t') &&
      |t'.components| == |t.components| &&
      t'.components[i] > M &&
      (forall j :: 0 <= j < |t.components| && j != i ==>
         t'.components[j] == t.components[j])
  {
    var t' := WithComponent(t, i, M + 1);
  }
}
