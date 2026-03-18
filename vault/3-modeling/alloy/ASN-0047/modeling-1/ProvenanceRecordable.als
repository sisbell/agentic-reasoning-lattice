-- ProvenanceRecordable: K.rho precondition
-- a in dom(C) and d in E_doc
-- Recording provenance requires the element address to be allocated
-- content and the document to be an allocated document entity.

sig Tumbler {
  zeros: Int
}

fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }
pred IsElement[t: Tumbler]  { t.zeros >= 3 }

-- State with entity set, content domain, and provenance
sig State {
  E: set Tumbler,              -- allocated entity addresses
  C: set Tumbler,              -- dom(C): allocated content (element addresses)
  R: Tumbler -> Tumbler        -- provenance: (element, document)
}

-- Entity set contains only non-element addresses
pred EntitySetValid[s: State] {
  all e: s.E | e.zeros =< 2
}

-- Derived stratum
fun E_doc[s: State]: set Tumbler {
  { e: s.E | IsDocument[e] }
}

-- Content domain contains only elements
pred ContentDomainValid[s: State] {
  all a: s.C | IsElement[a]
}

-- Provenance well-typed: R subset T_elem x E_doc
pred ProvenanceWellTyped[s: State] {
  all a, d: Tumbler |
    (a -> d) in s.R implies
      (IsElement[a] and d in E_doc[s])
}

pred wellFormed[s: State] {
  EntitySetValid[s]
  ContentDomainValid[s]
  ProvenanceWellTyped[s]
}

-- K.rho precondition: ProvenanceRecordable
pred ProvenanceRecordable[s: State, a: Tumbler, d: Tumbler] {
  a in s.C        -- a in dom(C)
  d in E_doc[s]   -- d in E_doc
}

-- K.rho: record provenance with precondition
pred RecordProvenance[s, sPost: State, a: Tumbler, d: Tumbler] {
  ProvenanceRecordable[s, a, d]
  sPost.R = s.R + (a -> d)
  sPost.E = s.E
  sPost.C = s.C
}

-- K.rho without precondition (negative test)
pred RecordProvenanceNoPre[s, sPost: State, a: Tumbler, d: Tumbler] {
  sPost.R = s.R + (a -> d)
  sPost.E = s.E
  sPost.C = s.C
}

-- Property: K.rho with precondition preserves well-formedness
assert RecordProvPreservesWF {
  all s, sPost: State, a, d: Tumbler |
    (wellFormed[s] and RecordProvenance[s, sPost, a, d])
      implies wellFormed[sPost]
}

-- Negative: without precondition, well-formedness can break
assert NaiveRecordProvBreaksWF {
  all s, sPost: State, a, d: Tumbler |
    (wellFormed[s] and RecordProvenanceNoPre[s, sPost, a, d])
      implies wellFormed[sPost]
}

-- Non-vacuity: a valid provenance recording exists
run FindRecordProv {
  some s, sPost: State, a, d: Tumbler |
    wellFormed[s] and RecordProvenance[s, sPost, a, d]
} for 5 but exactly 2 State, 4 Int

check RecordProvPreservesWF for 5 but exactly 2 State, 4 Int
check NaiveRecordProvBreaksWF for 5 but exactly 2 State, 4 Int
