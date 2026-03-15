// N1 — IdentityByAssignment (INV, predicate(Tumbler))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerOrder.dfy"

module IdentityByAssignment {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import TumblerOrder

  // A node's identity is its tumbler address: positive, all components
  // positive (no zero separators). Identity is permanent (T8), positional
  // (determined by ancestry), and independent of content or operational state.
  ghost predicate IdentityByAssignment(n: Tumbler) {
    PositiveTumbler(n) &&
    TumblerHierarchy.ZeroCount(n.components) == 0
  }

  // Identity is intrinsic: two node addresses are the same node iff
  // they are the same tumbler (T3 — CanonicalRepresentation).
  lemma IdentityDeterminedByAddress(a: Tumbler, b: Tumbler)
    requires IdentityByAssignment(a)
    requires IdentityByAssignment(b)
    ensures a == b <==> TumblerOrder.ComponentEqual(a, b)
  {
    TumblerOrder.CanonicalRepresentation(a, b);
  }
}
