-- P3-ArrangementMutability.als
-- Property: arrangements admit three modes of change —
-- extension, contraction, and reordering — while C, E, and R
-- are monotonic. Only M can shrink.

sig VAddr {}
sig IAddr {}
sig Doc {}

sig State {
  entities: set Doc,
  content: set IAddr,
  prov: set IAddr,
  arr: Doc -> VAddr -> lone IAddr
}

-- Arrangement only references existing entities and content
pred wellFormed[s: State] {
  all d: Doc, v: VAddr, i: IAddr |
    d -> v -> i in s.arr implies (d in s.entities and i in s.content)
}

-- Elementary operations --

-- K.delta: create a new entity
pred KCreate[s, s2: State, d: Doc] {
  d not in s.entities
  s2.entities = s.entities + d
  s2.content = s.content
  s2.prov = s.prov
  s2.arr = s.arr
}

-- K.gamma: register content address
pred KContent[s, s2: State, i: IAddr] {
  i not in s.content
  s2.content = s.content + i
  s2.entities = s.entities
  s2.prov = s.prov
  s2.arr = s.arr
}

-- K.mu+: add mapping to arrangement (extension)
pred KAddMap[s, s2: State, d: Doc, v: VAddr, i: IAddr] {
  d in s.entities
  i in s.content
  no s.arr[d][v]
  s2.arr = s.arr + (d -> v -> i)
  s2.entities = s.entities
  s2.content = s.content
  s2.prov = s.prov
}

-- K.mu-: remove mapping from arrangement (contraction)
pred KRemMap[s, s2: State, d: Doc, v: VAddr, i: IAddr] {
  d -> v -> i in s.arr
  s2.arr = s.arr - (d -> v -> i)
  s2.entities = s.entities
  s2.content = s.content
  s2.prov = s.prov
}

-- K.rho: record provenance
pred KProv[s, s2: State, i: IAddr] {
  i in s.content
  s2.prov = s.prov + i
  s2.entities = s.entities
  s2.content = s.content
  s2.arr = s.arr
}

-- Any single elementary step
pred Step[s, s2: State] {
  (some d: Doc | KCreate[s, s2, d])
  or (some i: IAddr | KContent[s, s2, i])
  or (some d: Doc, v: VAddr, i: IAddr | KAddMap[s, s2, d, v, i])
  or (some d: Doc, v: VAddr, i: IAddr | KRemMap[s, s2, d, v, i])
  or (some i: IAddr | KProv[s, s2, i])
}

-- Reorder: V-positions swap while preserving I-address multiset
pred Reorder[s, s2: State, d: Doc] {
  wellFormed[s]
  wellFormed[s2]
  d in s.entities
  -- frame: E, C, R unchanged
  s2.entities = s.entities
  s2.content = s.content
  s2.prov = s.prov
  -- frame: other documents unchanged
  all d2: Doc - d | d2.(s2.arr) = d2.(s.arr)
  -- multiset preservation: each I-addr has same count of V-positions
  all i: IAddr |
    #{v: VAddr | v -> i in d.(s.arr)} =
    #{v: VAddr | v -> i in d.(s2.arr)}
  -- mapping itself changed
  d.(s.arr) != d.(s2.arr)
}

-- Assertions: E, C, R are monotonic under any elementary step

assert P3_EntityMonotonic {
  all s, s2: State |
    (wellFormed[s] and Step[s, s2]) implies s.entities in s2.entities
}

assert P3_ContentMonotonic {
  all s, s2: State |
    (wellFormed[s] and Step[s, s2]) implies s.content in s2.content
}

assert P3_ProvMonotonic {
  all s, s2: State |
    (wellFormed[s] and Step[s, s2]) implies s.prov in s2.prov
}

-- Well-formedness preservation
assert P3_StepPreservesWF {
  all s, s2: State |
    (wellFormed[s] and Step[s, s2]) implies wellFormed[s2]
}

-- Non-vacuity: each mode of M-change is achievable

run FindExtension {
  some s, s2: State, d: Doc, v: VAddr, i: IAddr |
    wellFormed[s] and KAddMap[s, s2, d, v, i]
} for 4 but exactly 2 State

run FindContraction {
  some s, s2: State, d: Doc, v: VAddr, i: IAddr |
    wellFormed[s] and KRemMap[s, s2, d, v, i]
} for 4 but exactly 2 State

run FindReorder {
  some s, s2: State, d: Doc |
    Reorder[s, s2, d]
} for 4 but exactly 2 State

check P3_EntityMonotonic for 5 but exactly 2 State
check P3_ContentMonotonic for 5 but exactly 2 State
check P3_ProvMonotonic for 5 but exactly 2 State
check P3_StepPreservesWF for 5 but exactly 2 State
