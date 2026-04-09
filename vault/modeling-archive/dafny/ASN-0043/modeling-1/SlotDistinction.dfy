include "Link.dfy"

// L6 — SlotDistinction
// The three endsets occupy structurally distinguished positions.
// (F, G, Θ) ≠ (G, F, Θ) when F ≠ G. Follows from datatype equality.
module SlotDistinction {
  import opened Endset
  import opened LinkDef

  ghost predicate SlotDistinction(lnk: Link) {
    forall F: Endset, G: Endset, Theta: Endset ::
      lnk == Link(F, G, Theta) && F != G ==>
      Link(F, G, Theta) != Link(G, F, Theta)
  }

  lemma SlotDistinctionHolds(lnk: Link)
    ensures SlotDistinction(lnk)
  { }
}
