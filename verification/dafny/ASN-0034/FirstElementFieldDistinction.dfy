// ASN-0034: T7 — FirstElementFieldDistinction
// If two element-level tumblers (zeros = 3) differ in their first
// element-field component, the tumblers themselves are distinct.
// Corollary of T3 (CanonicalRepresentation): equal tumblers produce
// equal results under any pure function of their components.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"
include "./UniqueParse.dfy"

module FirstElementFieldDistinction {
  import opened CarrierSetDefinition
  import opened HierarchicalParsing
  import opened UniqueParse
  import opened NatCarrierSet

  lemma FirstElementFieldDistinction(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires HierarchicalParsing.HierarchicalParsing(a)
    requires HierarchicalParsing.HierarchicalParsing(b)
    requires Zeros(a) == 3 && Zeros(b) == 3
    ensures Component(E(a), 1) != Component(E(b), 1) ==> a != b
  { }
}
