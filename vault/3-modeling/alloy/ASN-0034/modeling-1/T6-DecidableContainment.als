-- T6-DecidableContainment
-- For any two tumblers, field-level containment checks are decidable
-- from the addresses alone, and form a consistent hierarchy.

-- Abstract field values
sig NodeVal {}
sig UserVal {}
sig ElemVal {}

-- Document values form a forest (for prefix ordering)
sig DocVal {
  parent: lone DocVal
}

-- Acyclicity (separate fact — sig facts implicitly deref fields)
fact DocAcyclic {
  all d: DocVal | d not in d.^parent
}

-- A tumbler with its parsed fields (per FieldParsing definition).
-- Field hierarchy: elem requires doc, doc requires user.
-- Every tumbler has a node field.
sig Tumbler {
  node: one NodeVal,
  user: lone UserVal,
  doc: lone DocVal,
  elem: lone ElemVal
} {
  some elem implies some doc
  some doc implies some user
}

-----------------------------------------------------------
-- T6(a): same node field
-----------------------------------------------------------
pred sameNode[a, b: Tumbler] {
  a.node = b.node
}

-----------------------------------------------------------
-- T6(b): same node and user fields
-----------------------------------------------------------
pred sameNodeUser[a, b: Tumbler] {
  a.node = b.node
  a.user = b.user
}

-----------------------------------------------------------
-- T6(c): same node, user, and document fields
-----------------------------------------------------------
pred sameNodeUserDoc[a, b: Tumbler] {
  a.node = b.node
  a.user = b.user
  a.doc = b.doc
}

-----------------------------------------------------------
-- T6(d): document field of a is a prefix of document
-- field of b (structural subordination)
-----------------------------------------------------------
pred docFieldPrefix[a, b: Tumbler] {
  some a.doc and some b.doc
  a.doc in b.doc.*parent
}

-----------------------------------------------------------
-- Assertions
-----------------------------------------------------------

-- Containment hierarchy: (c) => (b) => (a)
assert HierarchyConsistency {
  all a, b: Tumbler |
    (sameNodeUserDoc[a, b] implies sameNodeUser[a, b]) and
    (sameNodeUser[a, b] implies sameNode[a, b])
}

-- Document prefix is reflexive for tumblers that have doc fields
assert DocPrefixReflexive {
  all t: Tumbler |
    some t.doc implies docFieldPrefix[t, t]
}

-- Document prefix is transitive
assert DocPrefixTransitive {
  all a, b, c: Tumbler |
    (docFieldPrefix[a, b] and docFieldPrefix[b, c])
      implies docFieldPrefix[a, c]
}

-- Mutual prefix implies same document field (antisymmetry)
assert DocPrefixAntisymmetric {
  all a, b: Tumbler |
    (docFieldPrefix[a, b] and docFieldPrefix[b, a])
      implies a.doc = b.doc
}

-- Same document field implies mutual prefix
assert SameDocImpliesMutualPrefix {
  all a, b: Tumbler |
    (some a.doc and some b.doc and a.doc = b.doc)
      implies (docFieldPrefix[a, b] and docFieldPrefix[b, a])
}

-----------------------------------------------------------
-- Non-vacuity
-----------------------------------------------------------
run NonVacuity {
  some disj a, b, c: Tumbler |
    sameNode[a, b] and not sameNodeUser[a, b] and
    docFieldPrefix[a, c] and not docFieldPrefix[c, a]
} for 5

-----------------------------------------------------------
-- Checks
-----------------------------------------------------------
check HierarchyConsistency for 5
check DocPrefixReflexive for 5
check DocPrefixTransitive for 5
check DocPrefixAntisymmetric for 5
check SameDocImpliesMutualPrefix for 5
