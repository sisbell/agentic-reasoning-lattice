-- P4a — HistoricalFidelity (LEMMA)
-- Every provenance record (a, d) in R is historically justified:
-- there exists some state in the transition history where a was in ran(M(d)).
-- (A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))
--
-- Derivation: by induction on the transition sequence.
--   Base: R₀ = ∅; vacuously satisfied.
--   Step: for new (a, d) in R' \ R, J1' gives a ∈ ran(M'(d)) — post-state witnesses.
--         for (a, d) in R, inductive hypothesis provides prior witness; P2 preserves entry.

open util/ordering[State]

sig Address {}
sig Doc {}

sig State {
  docs: set Doc,                      -- E_doc: allocated documents
  arr: Doc -> set Address,            -- ran(M(d)): addresses in each document's arrangement
  prov: Address -> set Doc            -- R: provenance relation
}

-- Well-formedness: arrangements only for existing docs
pred wf[s: State] {
  all d: Doc | some s.arr[d] implies d in s.docs
}

-- Initial state: empty provenance
pred init[s: State] {
  wf[s]
  no s.prov
}

-- Valid step: P2 (prov monotonic) + J1' (new prov entries witnessed in M')
pred validStep[s, s2: State] {
  wf[s2]
  -- P2: provenance is append-only
  s.prov in s2.prov
  -- J1': every freshly added provenance pair (a, d) has a in ran(M'(d))
  all a: Address, d: Doc |
    (a -> d in s2.prov and a -> d not in s.prov) implies
      a in s2.arr[d]
}

-- Trace: init followed by valid steps
fact Traces {
  init[first]
  all s: State - last | validStep[s, s.next]
}

-- P4a: Historical Fidelity
-- For every (a, d) in R at any reachable state, some state in the
-- history (up to and including that state) witnesses a in ran(M(d)).
assert P4a_HistoricalFidelity {
  all s: State, a: Address, d: Doc |
    a -> d in s.prov implies
      (some sk: s.prevs + s | a in sk.arr[d])
}

check P4a_HistoricalFidelity for 5 but exactly 4 State

-- Non-vacuity: find a trace with non-empty provenance and a witnessing state
run NonVacuity {
  some s: State, a: Address, d: Doc |
    a -> d in s.prov and a in s.arr[d]
} for 4 but exactly 3 State
