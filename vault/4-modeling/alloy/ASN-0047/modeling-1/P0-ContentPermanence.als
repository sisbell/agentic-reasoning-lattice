-- P0-ContentPermanence.als
-- Property: content is permanent — once an address has content,
-- it is never removed or modified in any subsequent state.
-- (A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))

sig Address {}
sig Value {}

sig State {
  C: Address -> lone Value
}

-- The content-permanence predicate
pred ContentPermanence[s, s2: State] {
  all a: Address | some s.C[a] implies s2.C[a] = s.C[a]
}

-- Elementary transition: add new content at a fresh address
pred AddContent[s, s2: State, a: Address, v: Value] {
  -- precondition: address not yet allocated
  no s.C[a]
  -- postcondition: address maps to value
  s2.C[a] = v
  -- frame: all other content unchanged
  all a2: Address - a | s2.C[a2] = s.C[a2]
}

-- Elementary transition: non-content operation (entity creation, fork, etc.)
pred NonContentStep[s, s2: State] {
  s2.C = s.C
}

-- A valid elementary transition either adds content or leaves it unchanged
pred ValidStep[s, s2: State] {
  (some a: Address, v: Value | AddContent[s, s2, a, v])
  or NonContentStep[s, s2]
}

-- P0: every valid step preserves content permanence
assert P0_ContentPermanence {
  all s, s2: State |
    ValidStep[s, s2] implies ContentPermanence[s, s2]
}

-- Non-vacuity: find an AddContent step where pre-state already has content
run NonVacuity {
  some s, s2: State, a: Address, v: Value |
    some s.C and AddContent[s, s2, a, v]
} for 4 but exactly 2 State

check P0_ContentPermanence for 5 but exactly 2 State
