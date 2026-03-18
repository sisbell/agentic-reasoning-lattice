include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// L0 — SubspacePartition (ASN-0043)
module SubspacePartition {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection: domains of content and link stores
  datatype State = State(
    contentDom: set<Tumbler>,
    linkDom: set<Tumbler>
  )

  // L0: all link addresses share subspace indicator sL, all content
  // addresses share subspace indicator sC, and sL ≠ sC.
  ghost predicate SubspacePartition(sigma: State, sL: nat, sC: nat) {
    sL != sC &&
    (forall a :: a in sigma.linkDom ==>
      TumblerHierarchy.HasElementField(a) && TumblerHierarchy.E1(a) == sL) &&
    (forall a :: a in sigma.contentDom ==>
      TumblerHierarchy.HasElementField(a) && TumblerHierarchy.E1(a) == sC)
  }

  // Derived: dom(Σ.L) ∩ dom(Σ.C) = ∅, by T7 (SubspaceDisjoint)
  lemma DisjointDomains(sigma: State, sL: nat, sC: nat)
    requires SubspacePartition(sigma, sL, sC)
    ensures sigma.linkDom !! sigma.contentDom
  { }
}
