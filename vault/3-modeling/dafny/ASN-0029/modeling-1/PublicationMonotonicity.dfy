include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module PublicationMonotonicity {
  import opened Foundation

  // Publication status per document
  datatype PubStatus = Private | Published | Privashed

  // D10 — PublicationMonotonicity (INV, predicate(State, State))
  // [Σ.pub(d) = published ⟹ Σ'.pub(d) = published]
  // Once a document is published, it remains published across every
  // state transition. Unconditional over all protocol operations.
  ghost predicate PublicationMonotonicity(
    pub: map<DocId, PubStatus>,
    pub': map<DocId, PubStatus>
  ) {
    forall d :: d in pub && pub[d] == Published ==>
      d in pub' && pub'[d] == Published
  }
}
