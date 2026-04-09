include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"
include "../../../../proofs/DocumentOntology/DocumentOntology.dfy"

module VersionForestModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened DocumentOntology

  // ASN-0029 D14 — VersionForest (INV, predicate(State))
  // includes parent membership

  // Covering parent: p is the immediate predecessor of d under ≺.
  // No document q sits strictly between p and d.
  ghost predicate IsCoveringParent(p: DocId, d: DocId) {
    DocLevelPrefix(p, d) &&
    !exists q :: DocLevelPrefix(p, q) && DocLevelPrefix(q, d)
  }

  // D14: the covering relation of ≺ restricted to Σ.D forms a forest.
  // Membership invariant: if d has a structural parent, that parent is live.
  ghost predicate VersionForest(s: State) {
    forall d :: d in s.docs ==>
      forall p :: IsCoveringParent(p, d) ==> p in s.docs
  }
}
