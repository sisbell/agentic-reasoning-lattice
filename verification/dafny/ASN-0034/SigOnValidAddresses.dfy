// ASN-0034: TA5-SigValid — SigOnValidAddresses
// For every valid address t satisfying T4, sig(t) = #t.
include "./HierarchicalParsing.dfy"
include "./LastSignificantPosition.dfy"

module SigOnValidAddresses {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened LastSignificantPosition

  lemma SigOnValidAddresses(t: Tumbler)
    requires InT(t)
    requires HierarchicalParsing.HierarchicalParsing(t)
    ensures LastSignificantPosition.LastSignificantPosition(t) == Length(t)
  { }
}
