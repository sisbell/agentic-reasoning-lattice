include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// P7 — ProvenanceGrounding
module ProvenanceGrounding {
  import opened TumblerAlgebra

  // Minimal state projection for P7
  datatype State = State(
    C: set<Tumbler>,              // dom(C): allocated content addresses
    R: set<(Tumbler, Tumbler)>    // provenance relation (address, document)
  )

  // P7 — ProvenanceGrounding
  // (A (a, d) ∈ R :: a ∈ dom(C))
  ghost predicate ProvenanceGrounded(s: State) {
    forall a, d :: (a, d) in s.R ==> a in s.C
  }

  // P0 — ContentPermanence (domain monotonicity)
  ghost predicate ContentMonotone(s: State, s': State) {
    s.C <= s'.C
  }

  // P2 — ProvenancePermanence
  ghost predicate ProvenanceMonotone(s: State, s': State) {
    s.R <= s'.R
  }

  // K.ρ (pre) — ProvenanceRecordable: new provenance entries require content
  ghost predicate NewProvenanceGrounded(s: State, s': State) {
    forall a, d :: (a, d) in s'.R && (a, d) !in s.R ==> a in s.C
  }

  // P7 — ProvenanceGrounding (base case)
  // R₀ = ∅, vacuously satisfied
  lemma ProvenanceGroundingBase(s: State)
    requires s.R == {}
    ensures ProvenanceGrounded(s)
  { }

  // P7 — ProvenanceGrounding (inductive step)
  // Derived from ProvenanceRecordable, P0, P2
  lemma ProvenanceGroundingInductive(s: State, s': State)
    requires ProvenanceGrounded(s)
    requires ContentMonotone(s, s')
    requires ProvenanceMonotone(s, s')
    requires NewProvenanceGrounded(s, s')
    ensures ProvenanceGrounded(s')
  { }
}
