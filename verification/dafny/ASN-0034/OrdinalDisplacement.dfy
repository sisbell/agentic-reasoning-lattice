// ASN-0034: OrdinalDisplacement — definition
// For natural number n ≥ 1 and depth m ≥ 1, the ordinal displacement
// δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at
// positions 1 through m − 1, and n at position m.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"

module OrdinalDisplacement {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened ActionPoint

  function OrdinalDisplacement(n: nat, m: nat): Tumbler
    requires n >= 1
    requires m >= 1
    ensures InT(OrdinalDisplacement(n, m))
    ensures Length(OrdinalDisplacement(n, m)) == m
    ensures PositiveTumbler.PositiveTumbler(OrdinalDisplacement(n, m))
    ensures ActionPoint.ActionPoint(OrdinalDisplacement(n, m)) == m
  {
    var t := Tumbler(seq(m - 1, _ => 0 as Carrier) + [n]);
    assert Component(t, m) == n;
    t
  }
}
