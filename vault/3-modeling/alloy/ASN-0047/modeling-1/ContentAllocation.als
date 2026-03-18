-- K.α — ContentAllocation (POST)
-- C' = C ∪ {a ↦ v} where a ∉ dom(C)
-- Frame: E' = E; (∀ d :: M'(d) = M(d)); R' = R

sig Address {}
sig Value {}
sig Entity {}
sig Span {}
sig Doc in Entity {}

sig State {
  content: Address -> lone Value,
  entities: set Entity,
  mapping: Doc -> Span -> lone Address,
  provenance: Address -> set Address
}

pred ContentAllocation[s, sPost: State, a: Address, v: Value] {
  -- precondition: a not in dom(C)
  a not in s.content.Value

  -- postcondition: C' = C ∪ {a ↦ v}
  sPost.content = s.content + (a -> v)

  -- frame: E' = E
  sPost.entities = s.entities

  -- frame: ∀ d :: M'(d) = M(d)
  sPost.mapping = s.mapping

  -- frame: R' = R
  sPost.provenance = s.provenance
}

-- Property 1: allocated address maps to the given value
assert AllocationMapsCorrectly {
  all s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v] implies
      sPost.content[a] = v
}

-- Property 2: existing content is preserved
assert AllocationPreservesExisting {
  all s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v] implies
      (all a2: Address - a | sPost.content[a2] = s.content[a2])
}

-- Property 3: domain grows by exactly one address
assert AllocationExtendsDomain {
  all s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v] implies
      sPost.content.Value = s.content.Value + a
}

-- Property 4: entities unchanged (frame verification)
assert AllocationFrameEntities {
  all s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v] implies
      sPost.entities = s.entities
}

-- Property 5: document mappings unchanged (frame verification)
assert AllocationFrameMapping {
  all s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v] implies
      sPost.mapping = s.mapping
}

-- Non-vacuity: can we perform a content allocation?
run NonVacuity {
  some s, sPost: State, a: Address, v: Value |
    ContentAllocation[s, sPost, a, v]
} for 4 but exactly 2 State

check AllocationMapsCorrectly for 5 but exactly 2 State
check AllocationPreservesExisting for 5 but exactly 2 State
check AllocationExtendsDomain for 5 but exactly 2 State
check AllocationFrameEntities for 5 but exactly 2 State
check AllocationFrameMapping for 5 but exactly 2 State
