-- UF-V: UniversalVFrame
-- Operations targeting document d leave all other documents' v-maps unchanged.
-- (A d' : d' in S.D and d' != d : S'.v(d') = S.v(d'))

sig IAddr {}
sig VPos {}

sig State {
  docs: set IAddr,
  vmap: IAddr -> VPos -> lone IAddr
} {
  -- vmap only defined for documents
  all d: IAddr | (some q: VPos | some vmap[d][q]) implies d in docs
}

-- UF-V frame predicate
pred UniversalVFrame[s, s2: State, target: IAddr] {
  all d: s.docs - target | s2.vmap[d] = s.vmap[d]
}

-- Address visibility in a document
pred visible[a: IAddr, d: IAddr, s: State] {
  some q: VPos | s.vmap[d][q] = a
}

-- Operation: modify a document (with UF-V frame)
pred ModifyDoc[s, s2: State, target: IAddr] {
  target in s.docs
  s2.docs = s.docs
  s2.vmap[target] != s.vmap[target]
  UniversalVFrame[s, s2, target]
}

-- Operation: create a new document (UF-V covers all pre-existing docs)
pred CreateDoc[s, s2: State, newDoc: IAddr] {
  newDoc not in s.docs
  s2.docs = s.docs + newDoc
  all d: s.docs | s2.vmap[d] = s.vmap[d]
}

-- Operation without frame (for negative check)
pred UncheckedModify[s, s2: State, target: IAddr] {
  target in s.docs
  s2.docs = s.docs
  s2.vmap[target] != s.vmap[target]
}

-- Assert: ModifyDoc preserves non-target v-maps
assert ModifyPreservesFrame {
  all s, s2: State, target: IAddr |
    ModifyDoc[s, s2, target] implies
      (all d: s.docs - target | s2.vmap[d] = s.vmap[d])
}

-- Assert: CreateDoc preserves pre-existing v-maps
assert CreatePreservesFrame {
  all s, s2: State, newDoc: IAddr |
    CreateDoc[s, s2, newDoc] implies
      (all d: s.docs | s2.vmap[d] = s.vmap[d])
}

-- Assert: UF-V preserves visibility in non-target documents
assert FramePreservesVisibility {
  all s, s2: State, target, d, a: IAddr |
    (ModifyDoc[s, s2, target] and d in s.docs and d != target) implies
      (visible[a, d, s] iff visible[a, d, s2])
}

-- Assert (negative): without UF-V, isolation can fail — expect counterexample
assert UncheckedPreservesOtherDocs {
  all s, s2: State, target: IAddr |
    UncheckedModify[s, s2, target] implies
      (all d: s.docs - target | s2.vmap[d] = s.vmap[d])
}

-- Non-vacuity: ModifyDoc with multiple documents
run FindModify {
  some s, s2: State, target: IAddr |
    ModifyDoc[s, s2, target] and #s.docs > 1
} for 5 but exactly 2 State

check ModifyPreservesFrame for 5 but exactly 2 State
check CreatePreservesFrame for 5 but exactly 2 State
check FramePreservesVisibility for 5 but exactly 2 State
check UncheckedPreservesOtherDocs for 5 but exactly 2 State
