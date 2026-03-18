-- ContentAllocatable: K.α precondition
-- IsElement(a) ∧ origin(a) ∈ E_doc
-- Content allocation requires the target address to be element-level
-- and its origin document to be an allocated entity.

sig Tumbler {
  zeros: Int,
  origin: lone Tumbler   -- for elements: the parent document
}

fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }
pred IsElement[t: Tumbler]  { t.zeros >= 3 }

-- origin is defined exactly for elements, and maps to a document
fact OriginWellDefined {
  all t: Tumbler |
    IsElement[t] implies (some t.origin and IsDocument[t.origin])
  all t: Tumbler |
    not IsElement[t] implies no t.origin
}

-- State with entity set and allocated content
sig State {
  E: set Tumbler,           -- allocated entity addresses
  C: set Tumbler             -- allocated content (element addresses)
}

-- Entity set contains only non-element addresses
pred EntitySetValid[s: State] {
  all e: s.E | e.zeros =< 2
}

-- Derived stratum
fun E_doc[s: State]: set Tumbler {
  { e: s.E | IsDocument[e] }
}

-- Invariant: every content address is an element whose origin is in E_doc
pred ContentInvariant[s: State] {
  all a: s.C | IsElement[a] and a.origin in E_doc[s]
}

pred wellFormed[s: State] {
  EntitySetValid[s]
  ContentInvariant[s]
}

-- K.α precondition: ContentAllocatable
pred ContentAllocatable[s: State, a: Tumbler] {
  IsElement[a]
  a.origin in E_doc[s]
}

-- K.α: allocate content at element address a
pred AllocateContent[s, sPost: State, a: Tumbler] {
  ContentAllocatable[s, a]
  a not in s.C
  sPost.C = s.C + a
  sPost.E = s.E
}

-- Allocation without precondition (negative test)
pred AllocateContentNoPre[s, sPost: State, a: Tumbler] {
  a not in s.C
  sPost.C = s.C + a
  sPost.E = s.E
}

-- Property: K.α with precondition preserves well-formedness
assert AllocPreservesWF {
  all s, sPost: State, a: Tumbler |
    (wellFormed[s] and AllocateContent[s, sPost, a])
      implies wellFormed[sPost]
}

-- Negative: without precondition, well-formedness can break
assert NaiveAllocBreaksWF {
  all s, sPost: State, a: Tumbler |
    (wellFormed[s] and AllocateContentNoPre[s, sPost, a])
      implies wellFormed[sPost]
}

-- Non-vacuity: a valid allocation exists
run FindAlloc {
  some s, sPost: State, a: Tumbler |
    wellFormed[s] and AllocateContent[s, sPost, a]
} for 5 but exactly 2 State, 4 Int

check AllocPreservesWF for 5 but exactly 2 State, 4 Int
check NaiveAllocBreaksWF for 5 but exactly 2 State, 4 Int
