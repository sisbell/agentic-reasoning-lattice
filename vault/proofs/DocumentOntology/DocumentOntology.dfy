module DocumentOntology {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  datatype PubStatus = Private | Published | Privashed

  datatype DocState = DocState(base: State, pub: map<DocId, PubStatus>)

  predicate ValidDocAddr(d: Tumbler) {
    HierarchicalParsing.CountZeros(d.components) == 2
  }

  ghost predicate DocLevelPrefix(ds: DocId, dv: DocId) {
    IsPrefix(ds, dv) && ds != dv && ValidDocAddr(ds) && ValidDocAddr(dv)
  }
}
