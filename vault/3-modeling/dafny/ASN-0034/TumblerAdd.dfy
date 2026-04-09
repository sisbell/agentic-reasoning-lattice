include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"

module TumblerAdd {
  // TumblerAdd — PositionAdvanceOperation
  // (a ⊕ w)ᵢ = aᵢ for i < k, (a ⊕ w)ₖ = aₖ + wₖ, (a ⊕ w)ᵢ = wᵢ for i > k

  import opened CarrierSetDefinition
  import opened PositiveTumbler

  function FindFirstNonZero(s: seq<nat>, i: nat): (k: nat)
    requires exists j :: i <= j < |s| && s[j] != 0
    ensures i <= k < |s|
    ensures s[k] != 0
    ensures forall j :: i <= j < k ==> s[j] == 0
    decreases |s| - i
  {
    if s[i] != 0 then i
    else FindFirstNonZero(s, i + 1)
  }

  function ActionPoint(w: Tumbler): (k: nat)
    requires ValidTumbler(w)
    requires IsPositive(w)
    ensures k < |w.components|
    ensures w.components[k] != 0
    ensures forall i :: 0 <= i < k ==> w.components[i] == 0
  {
    FindFirstNonZero(w.components, 0)
  }

  function TumblerAdd(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires ActionPoint(w) < |a.components|
    ensures |r.components| == |w.components|
    ensures ValidTumbler(r)
  {
    var k := ActionPoint(w);
    Tumbler(
      a.components[..k] + [a.components[k] + w.components[k]] + w.components[k+1..]
    )
  }
}
