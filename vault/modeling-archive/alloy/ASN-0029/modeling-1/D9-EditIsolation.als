-- D9-EditIsolation.als
-- Property: editing one document's version map does not affect another's.
-- [op modifies Σ.V(d₁) ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₂) = Σ.V(d₂)]
--
-- Derived from P7 (CrossDocVIndependent): version maps are per-document.

sig DocAddr {}
sig Element {}
sig Value {}

sig State {
  V: DocAddr -> Element -> lone Value
}

-- System invariant from P7: every operation is scoped to a single document.
-- The operation modifies V(target) and leaves all other documents unchanged.
pred DocScopedOp[s, sPost: State, target: DocAddr] {
  -- the operation modifies V(target)
  sPost.V[target] != s.V[target]

  -- frame: all other documents' version maps are unchanged
  all d: DocAddr - target | sPost.V[d] = s.V[d]
}

-- D9: EditIsolation
-- If an operation modifies V(d1) and d1 != d2, then V(d2) is unchanged.
assert EditIsolation {
  all s, sPost: State, target, d2: DocAddr |
    (DocScopedOp[s, sPost, target] and target != d2) implies
      sPost.V[d2] = s.V[d2]
}

-- Non-vacuity: a document-scoped operation can occur
run FindDocScopedOp {
  some s, sPost: State, d: DocAddr |
    DocScopedOp[s, sPost, d]
} for 4 but exactly 2 State, 2 DocAddr, 2 Element, 1 Value

check EditIsolation for 5 but exactly 2 State
