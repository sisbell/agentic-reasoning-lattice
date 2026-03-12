include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module PublicationFrame {
  import opened Foundation

  datatype PubStatus = Private | Published | Privashed

  // D10-ext — PublicationFrame (FRAME, ensures)
  // For any ASN-0026 operation (INSERT, DELETE, COPY, REARRANGE):
  //   (A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))
  ghost predicate PublicationFrame(
    pub: map<DocId, PubStatus>,
    pub': map<DocId, PubStatus>
  ) {
    forall d :: d in pub ==>
      d in pub' && pub'[d] == pub[d]
  }
}
