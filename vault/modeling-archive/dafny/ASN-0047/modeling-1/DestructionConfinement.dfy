// P5 — DestructionConfinement
module DestructionConfinement {

  datatype ProvPair = ProvPair(addr: nat, doc: nat)

  datatype State = State(
    C: map<nat, nat>,
    E: set<nat>,
    M: map<nat, map<nat, nat>>,
    R: set<ProvPair>
  )

  // --- Elementary transitions (frame conditions) ---

  // K.α: content allocation — extends C, frames E, R, M
  ghost predicate IsContentAllocation(s: State, s': State) {
    (forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]) &&
    s'.E == s.E && s'.R == s.R && s'.M == s.M
  }

  // K.δ: entity creation — extends E, frames C, R, M
  ghost predicate IsEntityCreation(s: State, s': State) {
    s.E <= s'.E &&
    s'.C == s.C && s'.R == s.R && s'.M == s.M
  }

  // K.μ⁺: arrangement extension — modifies M, frames C, E, R
  ghost predicate IsArrangementExtension(s: State, s': State) {
    s'.C == s.C && s'.E == s.E && s'.R == s.R
  }

  // K.μ⁻: arrangement contraction — modifies M, frames C, E, R
  ghost predicate IsArrangementContraction(s: State, s': State) {
    s'.C == s.C && s'.E == s.E && s'.R == s.R
  }

  // K.ρ: provenance recording — extends R, frames C, E, M
  ghost predicate IsProvenanceRecording(s: State, s': State) {
    s.R <= s'.R &&
    s'.C == s.C && s'.E == s.E && s'.M == s.M
  }

  ghost predicate ElementaryStep(s: State, s': State) {
    IsContentAllocation(s, s') ||
    IsEntityCreation(s, s') ||
    IsArrangementExtension(s, s') ||
    IsArrangementContraction(s, s') ||
    IsProvenanceRecording(s, s')
  }

  // --- Destruction confinement predicates ---

  ghost predicate ContentPreserved(s: State, s': State) {
    forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  }

  ghost predicate EntityPreserved(s: State, s': State) {
    s.E <= s'.E
  }

  ghost predicate ProvenancePreserved(s: State, s': State) {
    s.R <= s'.R
  }

  ghost predicate DestructionConfinementProp(s: State, s': State) {
    ContentPreserved(s, s') &&
    EntityPreserved(s, s') &&
    ProvenancePreserved(s, s')
  }

  // --- Per-elementary-step preservation ---

  lemma ElementaryPreservation(s: State, s': State)
    requires ElementaryStep(s, s')
    ensures DestructionConfinementProp(s, s')
  { }

  // --- Transitivity of preservation ---

  lemma PreservationTransitive(s1: State, s2: State, s3: State)
    requires DestructionConfinementProp(s1, s2)
    requires DestructionConfinementProp(s2, s3)
    ensures DestructionConfinementProp(s1, s3)
  { }

  // --- Composite transitions ---

  ghost predicate ValidComposite(trace: seq<State>) {
    |trace| >= 2 &&
    forall i :: 0 <= i < |trace| - 1 ==> ElementaryStep(trace[i], trace[i + 1])
  }

  // P5 — DestructionConfinement
  // derived from elementary frames; generalises S9
  lemma DestructionConfinement(trace: seq<State>)
    requires ValidComposite(trace)
    ensures DestructionConfinementProp(trace[0], trace[|trace| - 1])
    decreases |trace|
  {
    if |trace| == 2 {
      ElementaryPreservation(trace[0], trace[1]);
    } else {
      ElementaryPreservation(trace[0], trace[1]);
      DestructionConfinement(trace[1..]);
      PreservationTransitive(trace[0], trace[1], trace[|trace| - 1]);
    }
  }
}
