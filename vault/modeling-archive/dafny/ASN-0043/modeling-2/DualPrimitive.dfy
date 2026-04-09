include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// L14 — DualPrimitive (ASN-0043)
module DualPrimitive {
  import opened TumblerAlgebra

  // State projection: content and link domains
  datatype State = State(
    contentDom: set<Tumbler>,
    linkDom: set<Tumbler>
  )

  // Entity domain: union of content and link stores
  function EntityDomain(sigma: State): set<Tumbler> {
    sigma.contentDom + sigma.linkDom
  }

  // L14: content and links are the two primitive entity types;
  // their domains are disjoint. The entity domain is exactly
  // dom(Σ.C) ∪ dom(Σ.L) — no other state component maps addresses
  // to entity values.
  ghost predicate DualPrimitive(sigma: State) {
    sigma.contentDom !! sigma.linkDom
  }

  // Every entity address belongs to exactly one of the two stores
  lemma ExclusiveMembership(sigma: State, a: Tumbler)
    requires DualPrimitive(sigma)
    requires a in EntityDomain(sigma)
    ensures (a in sigma.contentDom) != (a in sigma.linkDom)
  { }
}
