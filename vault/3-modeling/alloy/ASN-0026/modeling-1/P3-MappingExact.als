-- P3-MappingExact.als
-- INV: RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p)) for all valid (d, p)

sig Addr {}
sig Byte {}
sig Doc {}

sig State {
  docs: set Doc,
  ispace: Addr -> lone Byte,
  vspace: Doc -> Int -> lone Addr
}

pred wellFormed[s: State] {
  -- V-space only defined for documents in the document set
  all d: Doc - s.docs | no s.vspace[d]

  -- V-space positions are positive
  all d: s.docs, p: Int |
    some s.vspace[d][p] implies p >= 1

  -- V-space positions are dense (no gaps from 1 to n_d)
  all d: s.docs, p: Int |
    some s.vspace[d][p] implies
      (all q: Int | (q >= 1 and q < p) implies some s.vspace[d][q])

  -- All V-space target addresses are allocated in I-space
  all d: s.docs, p: Int |
    some s.vspace[d][p] implies some s.ispace[s.vspace[d][p]]
}

-- RETRIEVE: two-level composition V then I
fun retrieve[s: State, d: Doc, p: Int]: lone Byte {
  s.ispace[s.vspace[d][p]]
}

-- P3: MappingExact
assert MappingExact {
  all s: State | wellFormed[s] implies
    all d: s.docs, p: Int |
      (p >= 1 and some s.vspace[d][p]) implies
        retrieve[s, d, p] = s.ispace[s.vspace[d][p]]
}

check MappingExact for 5 but exactly 1 State, 4 Int

-- Non-vacuity: well-formed state with documents and content
run NonVacuity {
  some s: State |
    wellFormed[s] and
    some d: s.docs, p: Int | some s.vspace[d][p]
} for 5 but exactly 1 State, 4 Int
