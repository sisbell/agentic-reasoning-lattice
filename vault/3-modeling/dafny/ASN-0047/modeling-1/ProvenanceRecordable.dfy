include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.ρ (pre) — ProvenanceRecordable
// a ∈ dom(C) ∧ d ∈ E_doc
module ProvenanceRecordable {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection for K.ρ precondition
  datatype State = State(
    C: set<Tumbler>,    // dom(C): allocated content addresses
    E: set<Tumbler>     // allocated entity addresses
  )

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  // K.ρ (pre): a ∈ dom(C) ∧ d ∈ E_doc
  ghost predicate ProvenanceRecordable(s: State, a: Tumbler, d: Tumbler) {
    a in s.C && d in E_doc(s)
  }
}
