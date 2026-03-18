-- ProvenanceWellTyped: R ⊆ T_elem × E_doc
-- Provenance relation records (element-address, document) pairs.
-- The invariant requires every pair in R to have an element as first
-- component and a document entity as second component.

sig Tumbler {
  zeros: Int   -- number of zero separators determines level
}

fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }
pred IsElement[t: Tumbler]  { t.zeros >= 3 }

-- State with entity set, arrangement, and provenance
sig State {
  E: set Tumbler,                -- allocated entity addresses
  arrangement: Tumbler -> Tumbler,  -- doc -> element mapping
  R: Tumbler -> Tumbler             -- provenance: (element, document)
}

-- Entity set contains only non-element addresses
pred EntitySetValid[s: State] {
  all e: s.E | e.zeros =< 2
}

-- Derived strata
fun E_doc[s: State]: set Tumbler {
  { e: s.E | IsDocument[e] }
}

fun T_elem: set Tumbler {
  { t: Tumbler | IsElement[t] }
}

-- Arrangement well-formedness: maps documents to elements
pred arrangementWF[s: State] {
  all d, a: Tumbler |
    (d -> a) in s.arrangement implies
      (d in E_doc[s] and IsElement[a])
}

-- The invariant under test
pred ProvenanceWellTyped[s: State] {
  all a, d: Tumbler |
    (a -> d) in s.R implies
      (IsElement[a] and d in E_doc[s])
}

-- Combined well-formedness
pred wellFormed[s: State] {
  EntitySetValid[s]
  ProvenanceWellTyped[s]
  arrangementWF[s]
}

-- Elementary transition: create document (K.delta)
pred CreateDoc[s, sPost: State, d: Tumbler] {
  IsDocument[d]
  d not in s.E
  sPost.E = s.E + d
  no sPost.arrangement[d]
  all d2: Tumbler - d | sPost.arrangement[d2] = s.arrangement[d2]
  sPost.R = s.R
}

-- Elementary transition: add element to arrangement (K.mu+)
pred AddToArrangement[s, sPost: State, d: Tumbler, a: Tumbler] {
  d in E_doc[s]
  IsElement[a]
  sPost.arrangement[d] = s.arrangement[d] + a
  all d2: Tumbler - d | sPost.arrangement[d2] = s.arrangement[d2]
  sPost.E = s.E
  sPost.R = s.R
}

-- Elementary transition: record provenance (K.rho)
pred RecordProvenance[s, sPost: State, a: Tumbler, d: Tumbler] {
  d in E_doc[s]
  IsElement[a]
  sPost.R = s.R + (a -> d)
  sPost.E = s.E
  sPost.arrangement = s.arrangement
}

-- Fork composite: create d_new, populate from d_src, record provenance
pred Fork[s, sPost: State, dSrc: Tumbler, dNew: Tumbler] {
  -- preconditions
  dSrc in E_doc[s]
  some s.arrangement[dSrc]
  IsDocument[dNew]
  dNew not in s.E

  -- d_new created
  sPost.E = s.E + dNew

  -- new doc arrangement is nonempty subset of source elements
  sPost.arrangement[dNew] in s.arrangement[dSrc]
  some sPost.arrangement[dNew]

  -- source and others unchanged
  sPost.arrangement[dSrc] = s.arrangement[dSrc]
  all d2: Tumbler - dSrc - dNew | sPost.arrangement[d2] = s.arrangement[d2]

  -- provenance recorded for each element in new arrangement
  let newElems = sPost.arrangement[dNew] |
    sPost.R = s.R + (newElems -> dNew)
}

-- Assert: CreateDoc preserves ProvenanceWellTyped
assert CreateDocPreservesPWT {
  all s, sPost: State, d: Tumbler |
    (wellFormed[s] and CreateDoc[s, sPost, d]) implies
      ProvenanceWellTyped[sPost]
}

-- Assert: RecordProvenance preserves ProvenanceWellTyped
assert RecordProvenancePreservesPWT {
  all s, sPost: State, a, d: Tumbler |
    (wellFormed[s] and RecordProvenance[s, sPost, a, d]) implies
      ProvenanceWellTyped[sPost]
}

-- Assert: Fork preserves ProvenanceWellTyped
assert ForkPreservesPWT {
  all s, sPost: State, dSrc, dNew: Tumbler |
    (wellFormed[s] and Fork[s, sPost, dSrc, dNew]) implies
      ProvenanceWellTyped[sPost]
}

-- Non-vacuity: find a valid Fork that yields well-typed provenance
run FindFork {
  some s, sPost: State, dSrc, dNew: Tumbler |
    wellFormed[s] and Fork[s, sPost, dSrc, dNew] and ProvenanceWellTyped[sPost]
} for 5 but exactly 2 State, 4 Int

check CreateDocPreservesPWT for 5 but exactly 2 State, 4 Int
check RecordProvenancePreservesPWT for 5 but exactly 2 State, 4 Int
check ForkPreservesPWT for 5 but exactly 2 State, 4 Int
