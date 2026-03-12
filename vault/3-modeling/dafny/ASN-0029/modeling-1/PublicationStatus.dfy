include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module PublicationStatus {
  import opened Foundation

  // ASN-0029 Σ.pub — PublicationStatus (INV, State field)
  // Σ.pub : Σ.D → {private, published, privashed}
  // State extension: every document has exactly one publication status.

  datatype PubStatus = Private | Published | Privashed

  type PubMap = map<DocId, PubStatus>

  // Well-formedness: pub is a total function on exactly the document set
  ghost predicate ValidPub(s: State, pub: PubMap) {
    pub.Keys == s.docs
  }
}
