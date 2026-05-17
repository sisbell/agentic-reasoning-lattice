// ASN-0034: T4 — HierarchicalParsing
// Valid address tumblers satisfy positional conditions on the component
// sequence: zeros(t) ≤ 3; no two adjacent zeros; t₁ ≠ 0; t_{#t} ≠ 0.
include "./CarrierSetDefinition.dfy"

module HierarchicalParsing {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  function CountZeros(s: seq<Carrier>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + CountZeros(s[1..])
  }

  function Zeros(t: Tumbler): nat
  {
    CountZeros(t.components)
  }

  predicate HierarchicalParsing(t: Tumbler)
    requires InT(t)
  {
    Zeros(t) <= 3 &&
    (forall i :: 1 <= i < Length(t) ==>
       !(Component(t, i) == 0 && Component(t, i + 1) == 0)) &&
    Component(t, 1) != 0 &&
    Component(t, Length(t)) != 0
  }
}
