// ASN-0034: NAT-addbound
// For every m, n ∈ ℕ, the sum m + n is bounded below by each operand:
// m + n ≥ n (right dominance) and m + n ≥ m (left dominance).
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatZeroMinimum.dfy"
include "./NatArithmeticClosureAndIdentity.dfy"
include "./NatAdditionOrderAndSuccessor.dfy"

module NatAdditionDominatesOperands {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder
  import opened NatZeroMinimum
  import opened NatArithmeticClosureAndIdentity
  import opened NatAdditionOrderAndSuccessor

  lemma NatAdditionDominatesOperands(m: Carrier, n: Carrier)
    ensures GreaterOrEqual(m + n, n)
    ensures GreaterOrEqual(m + n, m)
  { }
}
