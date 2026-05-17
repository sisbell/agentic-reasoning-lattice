// ASN-0034: NAT-wellorder
// The natural numbers are well-ordered under <: every non-empty subset
// of ℕ has a least element.
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"

module NatWellOrdering {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder

  lemma {:axiom} NatWellOrdering(S: set<Carrier>)
    requires S != {}
    ensures exists m :: m in S && forall x :: x in S ==> LessOrEqual(m, x)
}
