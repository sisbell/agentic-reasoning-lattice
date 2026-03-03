-- T6 — DecidableContainment
--
-- Tumblers carry structured addresses: node, user, and document fields.
-- The four containment comparisons (a)-(d) are decidable from the address
-- values alone — each is a total, structurally-defined predicate.

sig Comp {}

sig Tumbler {
  nodeF: seq Comp,
  userF: seq Comp,
  docF:  seq Comp
}

-- (a) Same node field
pred sameNode[a, b: Tumbler] {
  a.nodeF = b.nodeF
}

-- (b) Same node and user fields
pred sameNodeUser[a, b: Tumbler] {
  a.nodeF = b.nodeF
  a.userF = b.userF
}

-- (c) Same node, user, and document-lineage fields
pred sameNodeUserDoc[a, b: Tumbler] {
  a.nodeF = b.nodeF
  a.userF = b.userF
  a.docF  = b.docF
}

-- (d) Document field of a is a prefix of the document field of b
pred docPrefixOf[a, b: Tumbler] {
  a.docF.inds in b.docF.inds
  all i: a.docF.inds | a.docF[i] = b.docF[i]
}

-- Containment hierarchy: finer agreement implies coarser
assert T6_HierarchyDocToNodeUser {
  all a, b: Tumbler | sameNodeUserDoc[a, b] implies sameNodeUser[a, b]
}

assert T6_HierarchyNodeUserToNode {
  all a, b: Tumbler | sameNodeUser[a, b] implies sameNode[a, b]
}

-- docPrefixOf is a partial order (reflexive, antisymmetric, transitive)
assert T6d_PrefixReflexive {
  all a: Tumbler | docPrefixOf[a, a]
}

assert T6d_PrefixAntisymmetric {
  all a, b: Tumbler |
    (docPrefixOf[a, b] and docPrefixOf[b, a]) implies a.docF = b.docF
}

assert T6d_PrefixTransitive {
  all a, b, c: Tumbler |
    (docPrefixOf[a, b] and docPrefixOf[b, c]) implies docPrefixOf[a, c]
}

-- Equal doc fields imply mutual prefix (converse of antisymmetry)
assert T6d_EqualMeansMutualPrefix {
  all a, b: Tumbler |
    a.docF = b.docF implies (docPrefixOf[a, b] and docPrefixOf[b, a])
}

-- Non-vacuity: witness tumblers at distinct containment levels
run T6_Witness {
  some disj a, b: Tumbler | sameNode[a, b] and not sameNodeUser[a, b]
  some disj c, d: Tumbler | docPrefixOf[c, d] and not (c.docF = d.docF)
} for 5 but 4 Tumbler, 4 Comp

check T6_HierarchyDocToNodeUser   for 5 but exactly 2 Tumbler, 4 Comp
check T6_HierarchyNodeUserToNode  for 5 but exactly 2 Tumbler, 4 Comp
check T6d_PrefixReflexive         for 5 but exactly 2 Tumbler, 4 Comp
check T6d_PrefixAntisymmetric     for 5 but exactly 2 Tumbler, 4 Comp
check T6d_PrefixTransitive        for 5 but exactly 3 Tumbler, 4 Comp
check T6d_EqualMeansMutualPrefix  for 5 but exactly 2 Tumbler, 4 Comp
