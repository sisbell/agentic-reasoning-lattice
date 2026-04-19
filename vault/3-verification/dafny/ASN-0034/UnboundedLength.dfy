include "./CarrierSetDefinition.dfy"

module UnboundedLength {
  // T0(b) — UnboundedLength

  import opened CarrierSetDefinition

  function TumblerOfLength(n: nat): Tumbler
    requires n >= 1
    ensures |TumblerOfLength(n).components| == n
    ensures ValidTumbler(TumblerOfLength(n))
  {
    Tumbler(seq(n, _ => 0))
  }

  lemma UnboundedLength(M: nat)
    ensures exists t: Tumbler :: ValidTumbler(t) && |t.components| > M
  {
    var t := TumblerOfLength(M + 1);
  }
}
