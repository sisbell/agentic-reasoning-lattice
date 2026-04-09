-- P11-ViewerIndependent.als
-- RETRIEVE is a pure function of (DocId, Pos); no viewer, session, or
-- context parameter appears in the protocol signature.
--
-- Modeling strategy: the Xanadu architecture defines RETRIEVE through
-- I-space / V-space lookup, which structurally excludes any viewer
-- parameter.  We introduce a Viewer sig and a hypothetical delivery
-- function that accepts a viewer argument, then check that the result
-- is invariant across viewers.  Because the function body resolves
-- through I-space / V-space only, the viewer argument is structurally
-- unused -- the check confirms this architectural guarantee.

sig Byte {}
sig Addr {}
sig DocId {}
sig Pos {}

-- Hypothetical extra parameter (stands for viewer, session, or context)
sig Viewer {}

sig State {
  ispace : Addr -> lone Byte,
  vspace : DocId -> Pos -> lone Addr,
  docs   : set DocId
}

pred wellFormed[s: State] {
  -- V-space defined only for existing documents
  all d: DocId |
    (some p: Pos | some s.vspace[d][p]) implies d in s.docs
  -- V-space targets land in I-space domain
  all d: s.docs, p: Pos |
    let a = s.vspace[d][p] | some a implies some s.ispace[a]
}

-- Xanadu RETRIEVE: defined purely through I-space / V-space
fun retrieve[s: State, d: DocId, p: Pos]: lone Byte {
  s.ispace[s.vspace[d][p]]
}

-- Hypothetical delivery that accepts an extra viewer parameter.
-- Body resolves through retrieve only -- the viewer is structurally unused.
fun delivery[s: State, d: DocId, p: Pos, v: Viewer]: lone Byte {
  retrieve[s, d, p]
}

-- P11: delivery is viewer-independent
assert ViewerIndependent {
  all s: State, d: DocId, p: Pos, v1, v2: Viewer |
    wellFormed[s] implies
      delivery[s, d, p, v1] = delivery[s, d, p, v2]
}

-- Determinism: retrieve is a partial function (at most one byte)
assert RetrieveDeterministic {
  all s: State, d: DocId, p: Pos |
    wellFormed[s] implies lone retrieve[s, d, p]
}

-- Non-vacuity: a well-formed state with a successful retrieval
run NonVacuity {
  some s: State, d: DocId, p: Pos |
    wellFormed[s] and some retrieve[s, d, p]
} for 4 but exactly 1 State, exactly 2 Viewer

check ViewerIndependent for 5 but exactly 1 State, exactly 3 Viewer
check RetrieveDeterministic for 5 but exactly 1 State
