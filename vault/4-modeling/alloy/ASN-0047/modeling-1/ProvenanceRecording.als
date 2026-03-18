-- K.rho — ProvenanceRecording (POST, ensures)
-- R' = R ∪ {(a, d)} where a ∈ dom(C) ∧ d ∈ E_doc
-- Frame: C' = C; E' = E; (∀ d :: M'(d) = M(d))

sig Address {}
sig Value {}
sig Entity {}
sig Span {}
sig Doc in Entity {}

sig State {
  content: Address -> lone Value,    -- C: content map
  entities: set Entity,              -- E: allocated entities
  mapping: Doc -> Span -> lone Address,  -- M: document arrangements
  provenance: Address -> set Doc     -- R: provenance relation (element -> document)
}

-- dom(C): addresses with allocated content
fun domC[s: State]: set Address {
  s.content.Value
}

-- K.rho postcondition: record provenance (a, d)
pred ProvenanceRecording[s, sPost: State, a: Address, d: Doc] {
  -- precondition
  a in domC[s]
  d in s.entities

  -- postcondition: R' = R ∪ {(a, d)}
  sPost.provenance = s.provenance + (a -> d)

  -- frame: C' = C
  sPost.content = s.content

  -- frame: E' = E
  sPost.entities = s.entities

  -- frame: ∀ d :: M'(d) = M(d)
  sPost.mapping = s.mapping
}

-- Property 1: the new pair is in provenance
assert RecordingAddsEntry {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      d in sPost.provenance[a]
}

-- Property 2: existing provenance is preserved
assert RecordingPreservesExisting {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      s.provenance in sPost.provenance
}

-- Property 3: provenance grows by exactly the new pair
assert RecordingExactGrowth {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      sPost.provenance = s.provenance + (a -> d)
}

-- Property 4: content unchanged (frame verification)
assert RecordingFrameContent {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      sPost.content = s.content
}

-- Property 5: entities unchanged (frame verification)
assert RecordingFrameEntities {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      sPost.entities = s.entities
}

-- Property 6: mapping unchanged (frame verification)
assert RecordingFrameMapping {
  all s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d] implies
      sPost.mapping = s.mapping
}

-- Non-vacuity: a valid provenance recording exists
run NonVacuity {
  some s, sPost: State, a: Address, d: Doc |
    ProvenanceRecording[s, sPost, a, d]
} for 4 but exactly 2 State

check RecordingAddsEntry for 5 but exactly 2 State
check RecordingPreservesExisting for 5 but exactly 2 State
check RecordingExactGrowth for 5 but exactly 2 State
check RecordingFrameContent for 5 but exactly 2 State
check RecordingFrameEntities for 5 but exactly 2 State
check RecordingFrameMapping for 5 but exactly 2 State
