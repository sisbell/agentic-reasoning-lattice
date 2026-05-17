// ASN-0034: NAT-addcompat
// Addition on ℕ is monotone with respect to order, and every natural is
// strictly less than its successor.
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"

module NatAdditionOrderAndSuccessor {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder

  lemma {:axiom} AdditionMonotonicity(m: Carrier, n: Carrier, p: Carrier)
    requires GreaterOrEqual(n, p)
    ensures GreaterOrEqual(m + n, m + p)

  lemma {:axiom} StrictSuccessor(n: Carrier)
    ensures Less(n, n + 1)
}
