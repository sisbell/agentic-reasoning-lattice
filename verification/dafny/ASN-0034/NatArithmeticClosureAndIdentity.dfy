// ASN-0034: NAT-closure
// ℕ is closed under successor and binary addition, with 0 as additive identity.
include "./NatCarrierSet.dfy"

module NatArithmeticClosureAndIdentity {
  import opened NatCarrierSet

  lemma {:axiom} SuccessorClosure(n: Carrier)
    ensures InCarrier(n + 1)

  lemma {:axiom} AdditionClosure(m: Carrier, n: Carrier)
    ensures InCarrier(m + n)

  lemma {:axiom} AdditiveIdentity(n: Carrier)
    ensures 0 + n == n
}
