-- P6-ExistentialCoherence
-- Property: (A a in dom(C) :: origin(a) in E_doc)
-- Every content element's origin is a document entity.

-- Address hierarchy: entities are node/account/doc; elements are content-level
abstract sig Address {}
sig NodeAddr, AccountAddr, DocAddr extends Address {}
sig ElemAddr extends Address {}

sig State {
  -- allocated entities (nodes, accounts, documents)
  entities: set Address,
  -- content domain: element addresses with allocated content
  content: set ElemAddr,
  -- origin: maps each content element to its owning document
  origin: ElemAddr -> lone DocAddr
}

-- Structural well-formedness (not including the invariant under test)
pred wellFormed[s: State] {
  -- entities are organisational addresses only
  s.entities in NodeAddr + AccountAddr + DocAddr
  -- every content element has exactly one origin
  all a: s.content | one s.origin[a]
  -- origin only defined for content elements
  all a: ElemAddr - s.content | no s.origin[a]
}

-- The invariant under test
pred ExistentialCoherence[s: State] {
  all a: s.content | s.origin[a] in s.entities & DocAddr
}

-- Initial state: empty content domain
pred init[s: State] {
  no s.content
  s.entities in NodeAddr + AccountAddr + DocAddr
}

-- K.alpha: allocate a new element under a document
pred AllocateElement[s, sPost: State, a: ElemAddr, d: DocAddr] {
  -- precondition
  a not in s.content
  d in s.entities & DocAddr

  -- postcondition
  sPost.content = s.content + a
  sPost.origin = s.origin + (a -> d)

  -- frame: entities unchanged
  sPost.entities = s.entities
}

-- Other transitions: preserve content membership (P0) and entity membership (P1)
pred OtherStep[s, sPost: State] {
  -- P0: content permanence
  s.content in sPost.content
  sPost.content = s.content
  -- P1: entity permanence
  s.entities in sPost.entities
  -- origins preserved for existing content
  all a: s.content | sPost.origin[a] = s.origin[a]
}

-----------------------------------------------------------------------
-- Checks
-----------------------------------------------------------------------

-- Base case: initial state satisfies P6
assert P6_Base {
  all s: State |
    (init[s] and wellFormed[s]) implies ExistentialCoherence[s]
}

-- Inductive step: K.alpha preserves P6
assert P6_Inductive_Alloc {
  all s, sPost: State, a: ElemAddr, d: DocAddr |
    (wellFormed[s] and ExistentialCoherence[s] and AllocateElement[s, sPost, a, d])
      implies ExistentialCoherence[sPost]
}

-- Inductive step: other transitions preserve P6
assert P6_Inductive_Other {
  all s, sPost: State |
    (wellFormed[s] and ExistentialCoherence[s] and OtherStep[s, sPost])
      implies ExistentialCoherence[sPost]
}

-- Non-vacuity: a reachable state with content satisfying both wellFormed and P6
run NonVacuity {
  some s: State |
    some s.content and wellFormed[s] and ExistentialCoherence[s]
} for 5 but exactly 1 State

check P6_Base for 5 but exactly 1 State
check P6_Inductive_Alloc for 5 but exactly 2 State
check P6_Inductive_Other for 5 but exactly 2 State
