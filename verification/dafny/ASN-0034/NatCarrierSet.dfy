// ASN-0034: NAT-carrier
// The carrier set for the component domain is ℕ (the natural numbers).
module NatCarrierSet {

  type Carrier = nat

  lemma {:axiom} NatCarrierSet()
    ensures exists c: Carrier :: c == 0
}
