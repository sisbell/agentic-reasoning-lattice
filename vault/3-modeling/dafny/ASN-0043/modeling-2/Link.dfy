// Link — Link datatype definition (ASN-0043)
// Link = (from : Endset, to : Endset, type : Endset)

include "Endset.dfy"

module LinkDef {
  import opened Endset

  // Link: triple of endsets (from, to, type)
  datatype Link = Link(from: Endset, to: Endset, typ: Endset)

  ghost predicate WellFormedLink(link: Link) {
    WellFormedEndset(link.from) &&
    WellFormedEndset(link.to) &&
    WellFormedEndset(link.typ)
  }
}
