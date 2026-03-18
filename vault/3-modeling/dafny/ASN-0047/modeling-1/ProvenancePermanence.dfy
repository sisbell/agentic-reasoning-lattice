include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ProvenancePermanence {
  import opened TumblerAlgebra

  // Minimal state projection: only the provenance relation is needed for P2
  datatype State = State(R: set<(Tumbler, Tumbler)>)

  // ---------------------------------------------------------------------------
  // P2 — ProvenancePermanence
  //
  // (A Σ → Σ' :: R ⊆ R')
  // Transition invariant: provenance records are never removed.
  // ---------------------------------------------------------------------------

  ghost predicate ProvenancePermanence(s: State, s': State) {
    s.R <= s'.R
  }

  // Transitivity: permanence composes across transition sequences
  lemma ProvenancePermanenceTransitive(s1: State, s2: State, s3: State)
    requires ProvenancePermanence(s1, s2)
    requires ProvenancePermanence(s2, s3)
    ensures ProvenancePermanence(s1, s3)
  { }
}
