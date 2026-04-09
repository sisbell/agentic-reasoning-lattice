-- A5.frame-doc: VersionCrossDocFrame
-- Property: all existing documents are unchanged by VersionCrossDoc.
-- (A d'' : d'' in Sigma.D : Sigma'.V(d'') = Sigma.V(d''))

sig Addr {}

sig Doc {}

sig State {
  docs: set Doc,
  -- V(d)(p) = a: document content as position -> address mapping
  content: Doc -> Int -> lone Addr
}

-- Content only defined for documents in the state
pred wellFormed[s: State] {
  all d: Doc | some s.content[d] implies d in s.docs
}

-- VersionCrossDoc: create a new version document
-- Core effects + frame on existing documents
pred VersionCrossDoc[s, s2: State, newDoc: Doc] {
  -- precondition: newDoc is fresh
  newDoc not in s.docs

  -- effect: newDoc added
  s2.docs = s.docs + newDoc

  -- effect: new doc has some content
  some s2.content[newDoc]

  -- A5.frame-doc: all existing documents unchanged
  all d: s.docs | s2.content[d] = s.content[d]
}

-- Frame property: existing document content is preserved
assert VersionCrossDocFrame {
  all s, s2: State, nd: Doc |
    (wellFormed[s] and VersionCrossDoc[s, s2, nd])
      implies (all d: s.docs | s2.content[d] = s.content[d])
}

-- Derived: existing docs are a subset of post-state docs
assert ExistingDocsPreserved {
  all s, s2: State, nd: Doc |
    VersionCrossDoc[s, s2, nd] implies s.docs in s2.docs
}

-- Derived: exactly one doc is added
assert ExactlyOneDocAdded {
  all s, s2: State, nd: Doc |
    VersionCrossDoc[s, s2, nd]
      implies s2.docs = s.docs + nd
}

-- Non-vacuity: the operation is satisfiable
run NonVacuity {
  some s, s2: State, nd: Doc |
    wellFormed[s] and VersionCrossDoc[s, s2, nd] and wellFormed[s2]
} for 4 but exactly 2 State, 4 Int

check VersionCrossDocFrame for 5 but exactly 2 State, 4 Int
check ExistingDocsPreserved for 5 but exactly 2 State, 4 Int
check ExactlyOneDocAdded for 5 but exactly 2 State, 4 Int
