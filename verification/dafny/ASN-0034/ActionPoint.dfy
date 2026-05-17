// ASN-0034: ActionPoint — definition
// The action point of a positive tumbler w is the least index k whose
// component is nonzero:
//   k = min{i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"

module ActionPointModule {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened NatCarrierSet

  function ActionPointFromIndex(w: Tumbler, k: nat): nat
    requires InT(w)
    requires 1 <= k <= Length(w)
    requires exists i :: k <= i <= Length(w) && Component(w, i) != 0
    ensures k <= ActionPointFromIndex(w, k) <= Length(w)
    ensures Component(w, ActionPointFromIndex(w, k)) != 0
    ensures forall j :: k <= j < ActionPointFromIndex(w, k) ==> Component(w, j) == 0
    decreases Length(w) - k
  {
    if Component(w, k) != 0 then k
    else ActionPointFromIndex(w, k + 1)
  }

  function ActionPoint(w: Tumbler): nat
    requires InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    ensures 1 <= ActionPoint(w) <= Length(w)
    ensures Component(w, ActionPoint(w)) != 0
    ensures forall j :: 1 <= j < ActionPoint(w) ==> Component(w, j) == 0
  {
    ActionPointFromIndex(w, 1)
  }
}
