include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "NamespaceDisjointness.dfy"
include "StreamStrictlyOrdered.dfy"

// B8 — GlobalUniqueness (ASN-0040)
module BaptismGlobalUniqueness {
  import opened TumblerAlgebra
  import ND = NamespaceDisjointness
  import SSO = StreamStrictlyOrdered

  // B8 — GlobalUniqueness
  // Distinct baptismal acts produce distinct addresses.
  //
  // A baptismal act is identified by (parent, depth, stream-index).
  // Case 1 — different namespace (p, d): B7 gives disjointness.
  // Case 2 — same namespace, different index: S0 gives strict ordering.
  //
  // DIVERGENCE: The ASN derives B8 from B1 (ContiguousPrefix), B4
  // (NamespaceSerialized), and B7 (NamespaceDisjointness). B1+B4 together
  // ensure that serialized baptisms in the same namespace produce distinct
  // stream indices. The Dafny model assumes the distinct-index conclusion
  // directly (the (p, d, n) triple differs) rather than modeling the
  // serialization protocol.
  lemma GlobalUniqueness(
    p1: Tumbler, d1: nat, n1: nat,
    p2: Tumbler, d2: nat, n2: nat
  )
    requires ND.ValidBaptismDepth(p1, d1)
    requires ND.ValidBaptismDepth(p2, d2)
    requires n1 >= 1 && n2 >= 1
    requires p1 != p2 || d1 != d2 || n1 != n2
    ensures ND.StreamElement(p1, d1, n1) != ND.StreamElement(p2, d2, n2)
  {
    if p1 != p2 || d1 != d2 {
      ND.NamespaceDisjointness(p1, d1, p2, d2, n1, n2);
    } else {
      if n1 < n2 {
        SSO.StreamStrictlyOrderedLemma(p1, d1, n1, n2);
      } else {
        SSO.StreamStrictlyOrderedLemma(p1, d1, n2, n1);
      }
    }
  }
}
