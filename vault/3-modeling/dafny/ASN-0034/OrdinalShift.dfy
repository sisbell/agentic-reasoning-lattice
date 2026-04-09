include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./TumblerAdd.dfy"

module OrdinalShift {
  // OrdinalShift — OrdinalShift (DEF)
  // shift(v, n) = v ⊕ δ(n, m) where m = #v

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd

  // δ(n, m) — ordinal displacement [0, ..., 0, n] of length m
  function Displacement(n: nat, m: nat): (d: Tumbler)
    requires n >= 1
    requires m >= 1
    ensures ValidTumbler(d)
    ensures |d.components| == m
    ensures d.components[m - 1] == n
    ensures forall i :: 0 <= i < m - 1 ==> d.components[i] == 0
    ensures IsPositive(d)
  {
    Tumbler(seq(m - 1, _ => 0) + [n])
  }

  function OrdinalShift(v: Tumbler, n: nat): (r: Tumbler)
    requires ValidTumbler(v)
    requires n >= 1
    ensures ValidTumbler(r)
    ensures |r.components| == |v.components|
    ensures forall i :: 0 <= i < |v.components| - 1 ==> r.components[i] == v.components[i]
    ensures r.components[|v.components| - 1] == v.components[|v.components| - 1] + n
    ensures r.components[|v.components| - 1] >= 1
  {
    var m := |v.components|;
    var delta := Displacement(n, m);
    TA.TumblerAdd(v, delta)
  }
}
