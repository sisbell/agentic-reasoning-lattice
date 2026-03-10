-- P2 — ReferentiallyComplete (INV)
-- Every v-space reference points to an allocated i-space address.
-- all d in D, 1 <= p <= n_d : V(d)(p) in dom(I)

sig Addr {}
sig Byte {}
sig Doc {}
sig Pos {}

sig State {
  ispace: Addr -> lone Byte,
  docs: set Doc,
  vspace: Doc -> Pos -> lone Addr
}

pred wellFormed[s: State] {
  -- vspace only defined for existing documents
  all d: Doc - s.docs | no d.(s.vspace)
  -- every document has at least one position
  all d: s.docs | some d.(s.vspace)
}

pred referentiallyComplete[s: State] {
  all d: s.docs, p: Pos |
    let a = d.(s.vspace)[p] |
      some a implies a in (s.ispace).Byte
}

assert P2_ReferentiallyComplete {
  all s: State |
    wellFormed[s] implies referentiallyComplete[s]
}

-- Non-vacuity: well-formed and referentially complete state exists
run NonVacuity {
  some s: State |
    wellFormed[s] and referentiallyComplete[s]
} for 4 but exactly 1 State

check P2_ReferentiallyComplete for 5 but exactly 1 State
