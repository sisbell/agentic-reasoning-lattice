// N14 — NoNodeMutableState (INV, predicate(Tumbler))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module NoNodeMutableState {
  import opened TumblerAlgebra

  // Extensional node contents — defined by prefix membership in the
  // global address space, not by any per-node record.
  ghost function NodeContents(n: Tumbler, addressSpace: set<Tumbler>): set<Tumbler> {
    set a | a in addressSpace && IsPrefix(n, a)
  }

  // N14 — NoNodeMutableState
  // A node carries no mutable state. Its identity is its tumbler address
  // (permanent, by T8) and its contents are defined extensionally as
  // addresses carrying the node's tumbler as a prefix — determined by
  // the global address space, not by any per-node record. No per-node
  // counter, capability list, or configuration survives across operations.
  //
  // In the functional model, this holds by construction: Tumbler is a
  // pure datatype with structural equality and no mutable fields.
  // The predicate captures the extensional observation: a node's
  // contents depend only on which addresses carry its prefix in the
  // global space — no hidden per-node state can cause variation.
  ghost predicate NoNodeMutableState(n: Tumbler) {
    forall S1: set<Tumbler>, S2: set<Tumbler> ::
      (forall a :: IsPrefix(n, a) ==> (a in S1 <==> a in S2)) ==>
      NodeContents(n, S1) == NodeContents(n, S2)
  }

  // The predicate holds for every tumbler — true by construction.
  lemma NoNodeMutableStateHolds(n: Tumbler)
    ensures NoNodeMutableState(n)
  { }
}
