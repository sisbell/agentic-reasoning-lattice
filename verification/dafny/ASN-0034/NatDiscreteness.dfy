// ASN-0034: NAT-discrete
// The natural number order is discrete: no element lies strictly between a and a+1.
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"

module NatDiscreteness {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder

  lemma {:axiom} NatDiscreteness(a: Carrier, b: Carrier)
    requires Less(a, b)
    ensures LessOrEqual(a + 1, b)
}
