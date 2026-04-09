// PermanenceFromFrames — LEMMA
//
// Every valid composite transition satisfies permanence properties
// P0 (content only grows), P1 (entities only grow), P2 (provenance only grows).
// Each elementary transition kind extends at most one collection and preserves
// the others via frame conditions. Transitivity over a finite sequence
// gives the composite all three permanence properties.

open util/ordering[State]

sig Entity {}
sig Content {}
sig Provenance {}

sig State {
  entities: set Entity,
  content: set Content,
  provenance: set Provenance
}

// --- Elementary transition kinds ---

// K.alpha: extends content, preserves entities and provenance
pred stepAlpha[s, s2: State] {
  s.content in s2.content
  s2.entities = s.entities
  s2.provenance = s.provenance
}

// K.delta: extends entities, preserves content and provenance
pred stepDelta[s, s2: State] {
  s.entities in s2.entities
  s2.content = s.content
  s2.provenance = s.provenance
}

// K.rho: extends provenance, preserves entities and content
pred stepRho[s, s2: State] {
  s.provenance in s2.provenance
  s2.entities = s.entities
  s2.content = s.content
}

// K.mu+ and other preserving kinds: all three preserved
pred stepPreserving[s, s2: State] {
  s2.entities = s.entities
  s2.content = s.content
  s2.provenance = s.provenance
}

// Any elementary step is one of the above
pred elementaryStep[s, s2: State] {
  stepAlpha[s, s2] or stepDelta[s, s2] or
  stepRho[s, s2] or stepPreserving[s, s2]
}

// --- Composite transition ---

// Valid composite: every consecutive pair is an elementary step
pred validComposite {
  all s: State - last | elementaryStep[s, next[s]]
}

// --- Permanence properties ---

pred P0[s, s2: State] { s.content in s2.content }
pred P1[s, s2: State] { s.entities in s2.entities }
pred P2[s, s2: State] { s.provenance in s2.provenance }

// --- Assertion: permanence holds for any valid composite ---

assert PermanenceFromFrames {
  validComposite implies (
    P0[first, last] and P1[first, last] and P2[first, last]
  )
}

check PermanenceFromFrames for 5 but exactly 4 State

// --- Non-vacuity: find a composite where all three collections grow ---

run NonVacuity {
  validComposite
  some last.entities - first.entities
  some last.content - first.content
  some last.provenance - first.provenance
} for 5 but exactly 4 State
