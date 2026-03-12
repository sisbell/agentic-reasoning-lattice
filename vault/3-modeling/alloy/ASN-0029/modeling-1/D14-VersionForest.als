-- D14-VersionForest.als
-- Property: the covering relation of document-level prefix (≺)
-- restricted to live documents forms a forest.
--
-- parent(d) = max≼ {d' ∈ Σ.D : d' ≺ d}
--   (partial — undefined when no live strict prefix exists)
--
-- Forest: each live document has at most one covering parent.
-- Membership invariant: live documents are closed under structural parent.

sig Doc {
  -- d' in d.prefixes iff d' ≺ d (strict document-level prefix)
  prefixes : set Doc
}

-- ≺ is a strict partial order with the chain condition (forest order)
fact ForestOrder {
  -- irreflexive
  all d : Doc | d not in d.prefixes
  -- transitive
  prefixes.prefixes in prefixes
  -- chain: prefixes of any doc are totally ordered
  all a, b, d : Doc |
    (a in d.prefixes and b in d.prefixes) implies
      (a in b.prefixes or b in a.prefixes or a = b)
}

sig State {
  D : set Doc   -- live (allocated) documents
}

-- Structural parent: covering parent in the full Doc universe
fun structuralParent[d : Doc] : lone Doc {
  let anc = d.prefixes |
    anc - anc.prefixes
}

-- Live parent: covering parent restricted to live documents
fun liveParent[s : State, d : Doc] : lone Doc {
  let anc = s.D & d.prefixes |
    anc - anc.prefixes
}

-- VersionForest invariant: live set is closed under structural parent
pred VersionForest[s : State] {
  all d : s.D |
    let p = structuralParent[d] |
      some p implies p in s.D
}

-- Structural parent is unique (at most one)
assert StructuralParentUnique {
  all d : Doc | lone structuralParent[d]
}

-- Live parent is unique (at most one)
assert LiveParentUnique {
  all s : State, d : Doc | lone liveParent[s, d]
}

-- Live parent relation is acyclic
assert LiveParentAcyclic {
  all s : State |
    let pr = {d1 : Doc, d2 : Doc |
      d1 in s.D and d2 = liveParent[s, d1]} |
    no d : Doc | d in d.^pr
}

-- Under VersionForest, live parent equals structural parent for all live docs
assert VersionForestPreservesStructure {
  all s : State | VersionForest[s] implies
    (all d : s.D | liveParent[s, d] = structuralParent[d])
}

-- Non-vacuity: find a VersionForest with parent relationships
run FindVersionForest {
  some s : State {
    VersionForest[s]
    #s.D > 2
    some d : s.D | some liveParent[s, d]
  }
} for 6 but exactly 1 State

check StructuralParentUnique for 6
check LiveParentUnique for 6 but exactly 1 State
check LiveParentAcyclic for 6 but exactly 1 State
check VersionForestPreservesStructure for 6 but exactly 1 State
