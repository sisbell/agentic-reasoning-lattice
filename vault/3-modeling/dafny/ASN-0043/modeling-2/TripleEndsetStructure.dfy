include "LinkStore.dfy"

// L3 — TripleEndsetStructure (ASN-0043)
// Encoded in type definition: every link is a triple (from, to, type)
// where each component is an endset (finite set of well-formed spans).
module TripleEndsetStructure {
  import opened LinkStore

  // L3 holds by construction: the Link datatype enforces triple structure.
  // Every Link value decomposes into exactly three endset components.
  lemma TripleEndsetStructure(link: Link)
    ensures exists f: Endset, g: Endset, theta: Endset :: link == Link(f, g, theta)
  { }
}
