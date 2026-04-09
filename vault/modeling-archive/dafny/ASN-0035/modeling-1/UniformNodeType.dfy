// N13 — UniformNodeType (INV, predicate(Tumbler))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module UniformNodeType {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // There is exactly one type of node. Node membership is determined
  // solely by address structure: positive tumbler, no zero separators.
  // No type tag, subclass, or content-based discriminant exists.
  ghost predicate UniformNodeType(n: Tumbler) {
    PositiveTumbler(n) &&
    TumblerHierarchy.ZeroCount(n.components) == 0
  }

  lemma ZeroCountAllPositive(s: seq<nat>)
    requires forall i :: 0 <= i < |s| ==> s[i] > 0
    ensures TumblerHierarchy.ZeroCount(s) == 0
    decreases |s|
  {
    if |s| > 0 {
      ZeroCountAllPositive(s[1..]);
    }
  }

  // The only criterion for node membership is all-positive components.
  // Any tumbler satisfying this is a node — no further structural
  // distinction applies regardless of depth, position, or content.
  lemma AllPositiveTumblerIsNode(n: Tumbler)
    requires |n.components| >= 1
    requires forall i :: 0 <= i < |n.components| ==> n.components[i] > 0
    ensures UniformNodeType(n)
  {
    ZeroCountAllPositive(n.components);
  }
}
