-- T6-DecidableContainment
-- For any two tumblers, field-level containment relationships
-- are decidable from the addresses alone.
--
-- Tumbler structure: N1...Na.0.U1...Ub.0.D1...Dc.0.E1...Ed
-- The fields(t) function extracts four fields separated by zero delimiters.
-- Since field components are positive and zeros serve only as delimiters,
-- the extraction is unambiguous and deterministic.

--------------------------------------------------------------
-- Abstract field values
--------------------------------------------------------------

sig NodeVal {}
sig UserVal {}
sig ElemVal {}

-- Document field values form a forest (prefix tree).
-- parent encodes that one doc-field sequence extends another by one level.
sig DocVal {
  parent: lone DocVal
} {
  this not in this.^@parent
}

sig Tumbler {
  nodeF: one NodeVal,
  userF: one UserVal,
  docF: one DocVal,
  elemF: one ElemVal
}

--------------------------------------------------------------
-- (a) Same node field
--------------------------------------------------------------

pred sameNode[a, b: Tumbler] {
  a.nodeF = b.nodeF
}

--------------------------------------------------------------
-- (b) Same node and user fields
--------------------------------------------------------------

pred sameNodeUser[a, b: Tumbler] {
  a.nodeF = b.nodeF
  a.userF = b.userF
}

--------------------------------------------------------------
-- (c) Same node, user, and document fields
--------------------------------------------------------------

pred sameNodeUserDoc[a, b: Tumbler] {
  a.nodeF = b.nodeF
  a.userF = b.userF
  a.docF = b.docF
}

--------------------------------------------------------------
-- (d) Document field of a is a prefix of document field of b
--     (structural subordination within a document family)
--------------------------------------------------------------

pred docPrefix[a, b: Tumbler] {
  a.docF in b.docF.*parent
}

--------------------------------------------------------------
-- Containment checks form a strict nesting hierarchy:
-- (c) => (b) => (a)
--------------------------------------------------------------

assert ContainmentHierarchy {
  all a, b: Tumbler |
    (sameNodeUserDoc[a, b] implies sameNodeUser[a, b]) and
    (sameNodeUser[a, b] implies sameNode[a, b])
}

--------------------------------------------------------------
-- Document prefix is a partial order
--------------------------------------------------------------

assert DocPrefixReflexive {
  all t: Tumbler | docPrefix[t, t]
}

assert DocPrefixTransitive {
  all a, b, c: Tumbler |
    (docPrefix[a, b] and docPrefix[b, c]) implies docPrefix[a, c]
}

assert DocPrefixAntisymmetric {
  all a, b: Tumbler |
    (docPrefix[a, b] and docPrefix[b, a]) implies a.docF = b.docF
}

--------------------------------------------------------------
-- Same document field iff mutual prefix
--------------------------------------------------------------

assert SameDocIffMutualPrefix {
  all a, b: Tumbler |
    (a.docF = b.docF) iff (docPrefix[a, b] and docPrefix[b, a])
}

--------------------------------------------------------------
-- Non-vacuity: demonstrate all four containment levels
--------------------------------------------------------------

run ShowContainmentLevels {
  some disj a, b, c, d: Tumbler {
    -- a,b share node but differ on user
    sameNode[a, b]
    not sameNodeUser[a, b]
    -- a,c share node+user but differ on doc
    sameNodeUser[a, c]
    not sameNodeUserDoc[a, c]
    -- d's doc field is a strict prefix of a's doc field
    docPrefix[d, a]
    d.docF != a.docF
  }
} for 5

check ContainmentHierarchy for 5
check DocPrefixReflexive for 5
check DocPrefixTransitive for 5
check DocPrefixAntisymmetric for 5
check SameDocIffMutualPrefix for 5
