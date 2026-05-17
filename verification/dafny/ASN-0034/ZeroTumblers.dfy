// ASN-0034: TA6 — ZeroTumblers
// No zero tumbler is a valid address.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"
include "./PositiveTumbler.dfy"
include "./LexicographicOrder.dfy"

module ZeroTumblers {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened PositiveTumbler
  import opened LexicographicOrder
  import opened NatStrictTotalOrder

  lemma ZeroTumblers(t: Tumbler)
    requires InT(t)
    requires ZeroTumbler(t)
    ensures !HierarchicalParsing.HierarchicalParsing(t)
  { }
}
