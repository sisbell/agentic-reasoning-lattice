-- T7-SubspaceDisjointness
-- The subspace identifier (E₁, the first component of the element field)
-- permanently separates the address space into disjoint regions.
-- No tumbler in subspace s₁ can equal a tumbler in subspace s₂ ≠ s₁.
--
-- The element field is decomposed into E₁ (subspace) and the remaining
-- components (E₂, E₃, ...).  Value equality requires all components to
-- match, so different E₁ immediately implies distinct tumblers.

--------------------------------------------------------------
-- Domain types
--------------------------------------------------------------

sig NodeVal {}
sig UserVal {}
sig DocVal {}
sig SubspaceId {}      -- E₁: first component of element field
sig ElemTail {}        -- remaining element components (E₂, E₃, ...)

--------------------------------------------------------------
-- Tumbler: four fields with E₁ broken out
--------------------------------------------------------------

sig Tumbler {
  nodeF:     one NodeVal,
  userF:     one UserVal,
  docF:      one DocVal,
  subspace:  one SubspaceId,
  elemTail:  one ElemTail
}

--------------------------------------------------------------
-- Value equality (component-wise)
--------------------------------------------------------------

pred valueEq[a, b: Tumbler] {
  a.nodeF    = b.nodeF
  a.userF    = b.userF
  a.docF     = b.docF
  a.subspace = b.subspace
  a.elemTail = b.elemTail
}

--------------------------------------------------------------
-- T7: different subspace ⟹ different tumbler
--------------------------------------------------------------

assert SubspaceDisjointness {
  all a, b: Tumbler |
    not (a.subspace = b.subspace) implies not valueEq[a, b]
}

--------------------------------------------------------------
-- Contrapositive view: value equality preserves subspace
--------------------------------------------------------------

assert SubspaceIsFunction {
  all a, b: Tumbler |
    valueEq[a, b] implies a.subspace = b.subspace
}

--------------------------------------------------------------
-- Non-vacuity: two tumblers in distinct subspaces exist
--------------------------------------------------------------

run NonVacuity {
  some disj a, b: Tumbler |
    not (a.subspace = b.subspace)
} for 4 but exactly 2 Tumbler, 2 SubspaceId

--------------------------------------------------------------
-- Checks
--------------------------------------------------------------

check SubspaceDisjointness for 5
check SubspaceIsFunction for 5
