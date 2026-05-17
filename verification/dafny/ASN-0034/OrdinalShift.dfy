// ASN-0034: OrdinalShift — definition
// For a tumbler v of length m and natural number n ≥ 1:
//   shift(v, n) = v ⊕ δ(n, m)
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./OrdinalDisplacement.dfy"

module OrdinalShift {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened ActionPoint
  import TumblerAdd
  import OrdinalDisplacement

  function OrdinalShift(v: Tumbler, n: nat): (r: Tumbler)
    requires InT(v)
    requires n >= 1
    ensures InT(r)
    ensures Length(r) == Length(v)
    ensures forall i :: 1 <= i < Length(v) ==> Component(r, i) == Component(v, i)
    ensures Component(r, Length(v)) == Component(v, Length(v)) + n
    ensures Component(r, Length(v)) >= 1
  {
    TumblerAdd.TumblerAdd(v, OrdinalDisplacement.OrdinalDisplacement(n, Length(v)))
  }
}
