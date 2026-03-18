-- ASN-0047 / IsInitialState
-- Bounded check: initial state Sigma_0 = (C_0, E_0, M_0, R_0)

-- Entity address hierarchy (partition via extends)
abstract sig Entity {}
sig Node extends Entity {}
sig Account extends Entity {}
sig Document extends Entity {}

-- Content elements (distinct from entities)
sig Element {}

-- Provenance records
sig Record {}

-- Arrangement slot (position in a document's membership list)
sig Slot {}

sig State {
  content: set Element,                          -- C
  entities: set Entity,                          -- E
  arrangement: Document -> Slot -> lone Account, -- M
  provenance: set Record                         -- R
}

-- State well-formedness: arrangement only involves entities in E
pred WellFormed[s: State] {
  all d: Document, sl: Slot |
    some s.arrangement[d][sl] implies
      (d in s.entities and s.arrangement[d][sl] in s.entities)
}

-- IsInitialState predicate
pred IsInitialState[s: State] {
  no s.content                  -- C_0 = empty
  one s.entities                -- E_0 = {n_0}
  s.entities in Node            -- IsNode(n_0)
  no s.arrangement              -- M_0(d) = empty for all d
  no s.provenance               -- R_0 = empty
}

-- CurrentContainment: {(a, d) : d in E_doc and a in ran(M(d))}
fun Contains[s: State]: Account -> Document {
  {a: Account, d: s.entities & Document |
    a in Slot.(d.(s.arrangement))}
}

-- Initial state is well-formed
assert InitialIsWellFormed {
  all s: State | IsInitialState[s] implies WellFormed[s]
}

-- No documents exist in initial state
assert InitialNoDocuments {
  all s: State | IsInitialState[s] implies
    no (s.entities & Document)
}

-- No accounts exist in initial state
assert InitialNoAccounts {
  all s: State | IsInitialState[s] implies
    no (s.entities & Account)
}

-- Containment is empty in initial state
assert InitialEmptyContainment {
  all s: State | IsInitialState[s] implies
    no Contains[s]
}

-- Non-vacuity: an initial state can exist
run FindInitial {
  some s: State | IsInitialState[s]
} for 3 but exactly 1 State

check InitialIsWellFormed for 5 but exactly 1 State
check InitialNoDocuments for 5 but exactly 1 State
check InitialNoAccounts for 5 but exactly 1 State
check InitialEmptyContainment for 5 but exactly 1 State
