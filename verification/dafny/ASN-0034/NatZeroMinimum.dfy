// ASN-0034: NAT-zero
// Zero is the minimum element of the natural numbers under <.
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"

module NatZeroMinimum {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder

  lemma {:axiom} NatZeroMinimum(a: Carrier)
    ensures LessOrEqual(0, a)
}
