include "Endset.dfy"

// Link — ASN-0043 (L3 — TripleEndsetStructure)
// A link value is a triple of endsets: (from, to, type)
module LinkDef {
  import opened Endset

  datatype Link = Link(from: Endset, to: Endset, typ: Endset)
}
