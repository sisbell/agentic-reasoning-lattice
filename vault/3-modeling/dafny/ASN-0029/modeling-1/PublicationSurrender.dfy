include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module PublicationSurrenderModule {
  import opened Foundation

  // ASN-0029 D11 — PublicationSurrender (INV, predicate(State, DocId))
  // normative

  datatype PubStatus = Private | Published | Privashed
  datatype Session = Session(id: nat)

  // Extended state: Foundation.State + publication status + access rights
  datatype DocState = DocState(
    base: State,
    pub: map<DocId, PubStatus>,
    sessions: set<Session>,
    readers: map<DocId, set<Session>>,
    linkers: map<DocId, set<Session>>,
    transcluders: map<DocId, set<Session>>
  )

  // D11 — PublicationSurrender
  //
  // Σ.pub(d) = published ⟹
  //   (a) any session may read d
  //   (b) any session may create links into d (incoming links)
  //   (c) any session may transclude from d (quotation)
  //   (d) withdrawal requires extraordinary process
  //
  // DIVERGENCE: Part (d) is a transition invariant already captured by D10
  // (PublicationMonotonicity). This predicate captures the single-state
  // access-rights obligation (a)-(c). The universe of sessions is modeled
  // as an explicit finite set (ds.sessions) since Dafny's set type cannot
  // express universal quantification over an unbounded datatype.
  ghost predicate PublicationSurrender(ds: DocState, d: DocId) {
    d in ds.base.docs && d in ds.pub &&
    d in ds.readers && d in ds.linkers && d in ds.transcluders &&
    (ds.pub[d] == Published ==>
      // (a) any session may read d
      ds.sessions <= ds.readers[d] &&
      // (b) any session may create links into d
      ds.sessions <= ds.linkers[d] &&
      // (c) any session may transclude from d
      ds.sessions <= ds.transcluders[d])
  }
}
