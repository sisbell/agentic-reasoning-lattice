// ASN-0034: Divergence — Divergence
// For distinct tumblers a, b ∈ T, divergence(a, b) is the index of
// the first divergence: either the smallest k ≤ min(#a, #b) with
// aₖ ≠ bₖ, or min(#a, #b) + 1 when all shared components agree.
include "./CarrierSetDefinition.dfy"

module Divergence {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  function FirstMismatch(a: Tumbler, b: Tumbler, start: nat, m: nat): nat
    requires InT(a) && InT(b)
    requires m <= Length(a) && m <= Length(b)
    requires 1 <= start <= m + 1
    decreases m + 1 - start
  {
    if start > m then m + 1
    else if Component(a, start) != Component(b, start) then start
    else FirstMismatch(a, b, start + 1, m)
  }

  function Divergence(a: Tumbler, b: Tumbler): nat
    requires InT(a) && InT(b)
    requires a != b
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    FirstMismatch(a, b, 1, m)
  }
}
