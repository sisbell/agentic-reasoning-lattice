-- J0-VSpaceGrounded.als
-- Property J0 — VSpaceGrounded (INV, predicate(State))
--   (A d : d in D : rng(v(d)) ⊆ A)
-- Every v-space mapping target is an allocated address.

sig IAddr {}
sig Value {}
sig VPos {}

sig State {
  iota: IAddr -> lone Value,      -- I-space content (partial fn)
  docs: set IAddr,                -- document set (DocId = IAddr)
  vmap: IAddr -> VPos -> lone IAddr  -- v-space map per document
} {
  -- Def DocumentSet: D ⊆ A
  docs in iota.Value

  -- vmap domain restricted to documents
  (vmap.IAddr).VPos in docs
}

-- Def AllocatedAddresses: A = dom(iota)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- J0: VSpaceGrounded
pred VSpaceGrounded[s: State] {
  all d: s.docs | VPos.(d.(s.vmap)) in allocated[s]
}

assert J0 {
  all s: State | VSpaceGrounded[s]
}

-- Non-vacuity: a state with documents, mappings, and J0 satisfied
run NonVacuity {
  some s: State {
    some s.docs
    some s.vmap
    VSpaceGrounded[s]
  }
} for 5 but exactly 1 State

check J0 for 5 but exactly 1 State
