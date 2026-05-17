// ASN-0034: NAT-addassoc
// Addition on ℕ is associative.
include "./NatCarrierSet.dfy"

module NatAdditionAssociative {
  import opened NatCarrierSet

  lemma {:axiom} NatAdditionAssociative(a: Carrier, b: Carrier, c: Carrier)
    ensures (a + b) + c == a + (b + c)
}
