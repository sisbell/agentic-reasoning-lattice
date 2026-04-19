-- T6 (DecidableContainment): for any two T4-valid tumblers a, b,
-- the following are decidable from the addresses alone:
-- (a) same node field
-- (b) same node and user fields
-- (c) same node, user, and document-lineage fields
-- (d) document field of a is a prefix of document field of b
--
-- Models tumblers at the decomposed-field level (T4 guarantees
-- unique field extraction). Each field is a non-empty sequence
-- of strictly positive naturals. Zero separators are implicit
-- in the decomposition.

open util/integer

------------------------------------------------------------
-- Domain: fields and tumblers
------------------------------------------------------------

-- A field is a non-empty finite sequence of positive naturals
sig Field {
  vals: seq Int
} {
  some vals
  all i: vals.inds | vals[i] >= 1
}

-- Tumbler decomposed into fields per T4.
-- Node always present; user/doc/elem present in hierarchical order.
-- zeros(t) = 0: node only
-- zeros(t) = 1: node, user
-- zeros(t) = 2: node, user, doc
-- zeros(t) = 3: node, user, doc, elem
sig Tumbler {
  node: one Field,
  user: lone Field,
  doc: lone Field,
  elem: lone Field
} {
  -- T4: fields present in hierarchical order
  some doc implies some user
  some elem implies some doc
}

------------------------------------------------------------
-- T6 predicates (formal contract translation)
------------------------------------------------------------

-- T6(a): same node field.
-- Returns YES iff N(a) = N(b) componentwise.
pred sameNode[a, b: Tumbler] {
  a.node.vals = b.node.vals
}

-- T6(b): same node and user fields.
-- Returns YES iff zeros(a) >= 1 and zeros(b) >= 1 and
-- N(a) = N(b) and U(a) = U(b).
-- Returns NO if either tumbler lacks a user field.
pred sameNodeUser[a, b: Tumbler] {
  some a.user and some b.user
  a.node.vals = b.node.vals
  a.user.vals = b.user.vals
}

-- T6(c): same node, user, and document-lineage fields.
-- Returns YES iff zeros(a) >= 2 and zeros(b) >= 2 and
-- N(a) = N(b) and U(a) = U(b) and D(a) = D(b).
-- Returns NO if either tumbler lacks a document field.
pred sameNodeUserDoc[a, b: Tumbler] {
  some a.doc and some b.doc
  a.node.vals = b.node.vals
  a.user.vals = b.user.vals
  a.doc.vals = b.doc.vals
}

-- T6(d): document-field prefix.
-- Returns YES iff zeros(a) >= 2 and zeros(b) >= 2 and
-- #D(a) <= #D(b) and (A k: 1 <= k <= #D(a): D(a)_k = D(b)_k).
-- Returns NO if either tumbler lacks a document field.
pred docPrefix[a, b: Tumbler] {
  some a.doc and some b.doc
  #(a.doc.vals) =< #(b.doc.vals)
  all i: a.doc.vals.inds | a.doc.vals[i] = b.doc.vals[i]
}

------------------------------------------------------------
-- Assertions: structural properties from the contract
------------------------------------------------------------

-- Containment hierarchy: (c) implies (b) implies (a)
assert ContainmentHierarchy {
  all a, b: Tumbler |
    (sameNodeUserDoc[a, b] implies sameNodeUser[a, b]) and
    (sameNodeUser[a, b] implies sameNode[a, b])
}

-- Equality-based checks are symmetric
assert EqualitySymmetry {
  all a, b: Tumbler |
    (sameNode[a, b] iff sameNode[b, a]) and
    (sameNodeUser[a, b] iff sameNodeUser[b, a]) and
    (sameNodeUserDoc[a, b] iff sameNodeUserDoc[b, a])
}

-- Document prefix is a preorder: reflexive
assert PrefixReflexive {
  all t: Tumbler |
    some t.doc implies docPrefix[t, t]
}

-- Document prefix is a preorder: transitive
assert PrefixTransitive {
  all a, b, c: Tumbler |
    (docPrefix[a, b] and docPrefix[b, c]) implies docPrefix[a, c]
}

-- Document prefix is antisymmetric on field values:
-- mutual prefix implies identical document fields
assert PrefixAntisymmetric {
  all a, b: Tumbler |
    (docPrefix[a, b] and docPrefix[b, a]) implies
      a.doc.vals = b.doc.vals
}

-- Same document-lineage implies mutual doc prefix
assert SameDocImpliesMutualPrefix {
  all a, b: Tumbler |
    sameNodeUserDoc[a, b] implies
      (docPrefix[a, b] and docPrefix[b, a])
}

-- Missing-field guarantee: if either lacks a user field,
-- sameNodeUser must return NO
assert MissingUserReturnsNo {
  all a, b: Tumbler |
    (no a.user or no b.user) implies not sameNodeUser[a, b]
}

-- Missing-field guarantee: if either lacks a doc field,
-- sameNodeUserDoc and docPrefix must return NO
assert MissingDocReturnsNo {
  all a, b: Tumbler |
    (no a.doc or no b.doc) implies
      (not sameNodeUserDoc[a, b] and not docPrefix[a, b])
}

------------------------------------------------------------
-- Non-vacuity
------------------------------------------------------------

-- Instance: two tumblers sharing node but differing in user
run FindSameNodeDiffUser {
  some disj a, b: Tumbler |
    sameNode[a, b] and some a.user and some b.user
    and a.user.vals != b.user.vals
} for 4 but exactly 2 Tumbler, 3 seq

-- Instance: strict document prefix (proper containment)
run FindStrictDocPrefix {
  some disj a, b: Tumbler |
    docPrefix[a, b] and not docPrefix[b, a]
} for 4 but exactly 2 Tumbler, 3 seq

-- Instance: one tumbler at node level, one at element level
run FindMixedLevels {
  some disj a, b: Tumbler |
    no a.user and some b.elem
} for 4 but exactly 2 Tumbler, 3 seq

------------------------------------------------------------
-- Checks
------------------------------------------------------------

check ContainmentHierarchy for 5 but 3 seq
check EqualitySymmetry for 5 but 3 seq
check PrefixReflexive for 5 but 3 seq
check PrefixTransitive for 5 but 3 seq
check PrefixAntisymmetric for 5 but 3 seq
check SameDocImpliesMutualPrefix for 5 but 3 seq
check MissingUserReturnsNo for 5 but 3 seq
check MissingDocReturnsNo for 5 but 3 seq
