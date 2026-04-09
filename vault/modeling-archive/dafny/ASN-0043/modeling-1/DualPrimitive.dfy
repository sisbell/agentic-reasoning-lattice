include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// L14 — DualPrimitive
module DualPrimitive {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // State — the two entity domains
  datatype State = State(
    contentDomain: set<Tumbler>,
    linkDomain: set<Tumbler>
  )

  // The set of all entity addresses
  function EntityDomain(sigma: State): set<Tumbler> {
    sigma.contentDomain + sigma.linkDomain
  }

  // L14 — DualPrimitive
  // Content and links are the two primitive entity types with disjoint domains.
  // dom(Σ.C) ∩ dom(Σ.L) = ∅
  ghost predicate DualPrimitive(sigma: State) {
    sigma.contentDomain !! sigma.linkDomain
  }
}
