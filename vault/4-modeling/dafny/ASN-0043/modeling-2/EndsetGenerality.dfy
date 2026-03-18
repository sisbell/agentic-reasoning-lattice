include "LinkStore.dfy"

// L4 — EndsetGenerality (ASN-0043)
// Derived from L3, T12; reclassified from INV.
// Every span in every endset of a valid link satisfies T12 — and T12 is
// the ONLY constraint. No restriction confines spans to a single document,
// prevents self-reference, or excludes cross-subspace addressing.
module EndsetGenerality {
  import opened LinkStore
  import opened TumblerAlgebra

  // L4: every span in every endset of a well-formed link satisfies T12
  lemma EndsetGenerality(store: Store, a: Tumbler, sp: Span)
    requires WellFormedStore(store)
    requires a in store
    requires sp in store[a].from || sp in store[a].to || sp in store[a].typ
    ensures WellFormedSpan(sp)
  { }

  // Absence of additional constraints: any T12-valid span can appear in
  // any endset slot of a well-formed link. This witnesses parts (a)–(c):
  // cross-document, intra-document, and cross-subspace spans are all valid.
  lemma EndsetGeneralityWitness(sp: Span)
    requires WellFormedSpan(sp)
    ensures WellFormedLink(Link({sp}, {sp}, {sp}))
  { }
}
