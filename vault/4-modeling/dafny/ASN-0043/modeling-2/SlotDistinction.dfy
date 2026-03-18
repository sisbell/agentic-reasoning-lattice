// L6 — SlotDistinction (ASN-0043)
// (A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))
// Follows from datatype equality: Link fields are positional.

include "Link.dfy"

module SlotDistinction {
  import opened LinkDef
  import opened Endset

  ghost predicate SlotDistinction(F: Endset, G: Endset, Theta: Endset) {
    F != G ==> Link(F, G, Theta) != Link(G, F, Theta)
  }

  lemma SlotDistinctionHolds(F: Endset, G: Endset, Theta: Endset)
    ensures SlotDistinction(F, G, Theta)
  { }
}
