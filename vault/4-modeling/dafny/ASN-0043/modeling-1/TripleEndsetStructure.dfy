include "Link.dfy"

// L3 — TripleEndsetStructure
// Every link has exactly three endsets (from, to, type).
// Encoded in the datatype definition of Link.
module TripleEndsetStructure {
  import opened Endset
  import opened LinkDef

  lemma TripleEndsetStructure(link: Link)
    ensures exists F: Endset, G: Endset, Theta: Endset :: link == Link(F, G, Theta)
  { }
}
