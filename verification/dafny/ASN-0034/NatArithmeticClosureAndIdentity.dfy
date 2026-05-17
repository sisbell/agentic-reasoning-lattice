// ASN-0034: NAT-closure
// ℕ is closed under successor and binary addition, with 0 as additive identity.
include "./NatCarrierSet.dfy"

module NatArithmeticClosureAndIdentity {
  import opened NatCarrierSet

  lemma {:axiom} AdditionClosure(m: Carrier, n: Carrier)
    ensures InCarrier(m + n)

  lemma {:axiom} OneInCarrier()
    ensures InCarrier(1)

  lemma {:axiom} LeftAdditiveIdentity(n: Carrier)
    ensures 0 + n == n

  lemma {:axiom} RightAdditiveIdentity(n: Carrier)
    ensures n + 0 == n

  lemma {:axiom} SuccessorPositivity(n: Carrier)
    ensures 0 < n + 1

  lemma ZeroLessThanOne()
    ensures 0 < 1
  {
    SuccessorPositivity(0);
    LeftAdditiveIdentity(1);
  }
}
