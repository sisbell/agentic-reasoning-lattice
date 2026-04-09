-- P5-DestructionConfinement.als
-- LEMMA: For every state transition Sigma -> Sigma':
--   (a) dom(C') ⊇ dom(C) and C'(a) = C(a) for all a in dom(C)
--   (b) E' ⊇ E
--   (c) R' ⊇ R
-- Only M (document arrangements) can lose information.
-- Proof: by case analysis on five elementary transitions, then transitivity.

open util/ordering[State]

sig Addr {}
sig Content {}
sig Prov {}

sig State {
  C: Addr -> lone Content,   -- content store (partial function)
  E: set Addr,               -- entity set
  R: set Prov,               -- provenance records
  M: Addr -> set Addr         -- document arrangements
}

// --- Elementary transition kinds ---

// K.alpha: allocate content at fresh address — extends C, frames E, R, M
pred stepAlpha[s, s2: State] {
  some a: Addr, v: Content |
    no s.C[a] and s2.C = s.C + a -> v
  s2.E = s.E
  s2.R = s.R
  s2.M = s.M
}

// K.delta: create entity — extends E, frames C, R, M
pred stepDelta[s, s2: State] {
  some a: Addr |
    a not in s.E and s2.E = s.E + a
  s2.C = s.C
  s2.R = s.R
  s2.M = s.M
}

// K.mu_plus: add mapping entry — extends M, frames C, E, R
pred stepMuPlus[s, s2: State] {
  some d, a: Addr |
    s2.M = s.M + d -> a
  s2.C = s.C
  s2.E = s.E
  s2.R = s.R
}

// K.mu_minus: remove mapping entry — shrinks M, frames C, E, R
pred stepMuMinus[s, s2: State] {
  some d, a: Addr |
    a in s.M[d] and s2.M = s.M - d -> a
  s2.C = s.C
  s2.E = s.E
  s2.R = s.R
}

// K.rho: record provenance — extends R, frames C, E, M
pred stepRho[s, s2: State] {
  some p: Prov |
    p not in s.R and s2.R = s.R + p
  s2.C = s.C
  s2.E = s.E
  s2.M = s.M
}

// An elementary step is one of the five kinds
pred elementaryStep[s, s2: State] {
  stepAlpha[s, s2] or stepDelta[s, s2] or
  stepMuPlus[s, s2] or stepMuMinus[s, s2] or
  stepRho[s, s2]
}

// --- Composite transition ---

// Valid composite: every consecutive pair is an elementary step
pred validComposite {
  all s: State - last | elementaryStep[s, next[s]]
}

// --- Destruction confinement sub-properties ---

// (a) Content only grows and existing values preserved
pred ContentPreserved[s, s2: State] {
  s.C in s2.C
}

// (b) Entity set only grows
pred EntityPreserved[s, s2: State] {
  s.E in s2.E
}

// (c) Provenance only grows
pred ProvenancePreserved[s, s2: State] {
  s.R in s2.R
}

// --- Assertions ---

// P5: all three permanence conditions hold for any valid composite
assert P5_DestructionConfinement {
  validComposite implies (
    ContentPreserved[first, last] and
    EntityPreserved[first, last] and
    ProvenancePreserved[first, last]
  )
}

// P5 per elementary step: each step individually satisfies (a)-(c)
assert P5_Elementary {
  all s, s2: State |
    elementaryStep[s, s2] implies (
      ContentPreserved[s, s2] and
      EntityPreserved[s, s2] and
      ProvenancePreserved[s, s2]
    )
}

// --- Non-vacuity ---

// Find a composite where M shrinks but C, E, R all grow
run NonVacuity {
  validComposite
  some last.C - first.C
  some last.E - first.E
  some last.R - first.R
  some first.M - last.M
} for 5 but exactly 5 State

check P5_Elementary for 5 but exactly 2 State
check P5_DestructionConfinement for 5 but exactly 5 State
