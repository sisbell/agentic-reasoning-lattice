// ASN-0034: T0(b) — UnboundedLength
// For every M ∈ ℕ there exists t ∈ T with Length(t) > M.
include "./CarrierSetDefinition.dfy"

module UnboundedLength {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  function TumblerOfLength(n: nat): Tumbler
    requires n >= 1
    ensures InT(TumblerOfLength(n))
    ensures Length(TumblerOfLength(n)) == n
  {
    Tumbler(seq(n, _ => 0 as Carrier))
  }

  lemma UnboundedLength(M: nat)
    ensures exists t: Tumbler :: InT(t) && Length(t) > M
  {
    var t := TumblerOfLength(M + 1);
  }
}
