// N0 — GhostElement (LEMMA, lemma)
// ASN-0035: Node Ontology — derived from T12

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"
include "BaptizedNodes.dfy"

module GhostElement {
  import opened TumblerAlgebra
  import TumblerAddition
  import BaptizedNodes

  // A node address is a valid span start regardless of system state.
  // SpanWellDefined is purely arithmetic — no State parameter exists.
  // The witness Tumbler([1]) is a unit-length span at the node's deepest level.
  lemma GhostElement(n: Tumbler)
    requires BaptizedNodes.NodeAddress(n)
    ensures TumblerAddition.SpanWellDefined(n, Tumbler([1]))
  {
    assert Tumbler([1]).components[0] != 0;
  }
}
