include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module ProvenanceWellTyped {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection for provenance well-typedness
  datatype State = State(E: set<Tumbler>, R: set<(Tumbler, Tumbler)>)

  // E_doc = {e ∈ E : IsDocument(e)}
  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  // ---------------------------------------------------------------------------
  // Σ.R — ProvenanceWellTyped
  //
  // R ⊆ T_elem × E_doc
  // The pair (a, d) ∈ R records that document d has, at some point in the
  // system's history, contained I-address a in its arrangement.
  // ---------------------------------------------------------------------------

  ghost predicate ProvenanceWellTyped(s: State) {
    forall p :: p in s.R ==>
      TumblerHierarchy.ElementAddress(p.0) && p.1 in E_doc(s)
  }
}
