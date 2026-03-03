-- T7 — SubspaceDisjointness
-- The subspace identifier (first component of the element field, E₁)
-- permanently separates the address space into disjoint regions.
-- No tumbler in subspace s₁ can equal a tumbler in subspace s₂ ≠ s₁.
-- Property: a.E₁ ≠ b.E₁ ⟹ a ≠ b

-- Abstract component values (stand-ins for natural numbers)
sig Val {}

-- Zero is the distinguished separator between tumbler fields
one sig Zero extends Val {}

-- A tumbler is structured as four segments separated by zero markers:
--   nodeField . 0 . userField . 0 . docField . 0 . [e1, elemTail...]
-- We model the four segments directly; e1 is the subspace identifier.
sig Tumbler {
  nodeField: set Val,
  userField: set Val,
  docField:  set Val,
  e1:        one Val,   -- first element-field component: the subspace
  elemTail:  set Val    -- remaining element components after e1
}

-- Subspace identifiers are nonzero (they name an actual subspace)
fact SubspaceNonzero {
  all t: Tumbler | not (t.e1 in Zero)
}

-- Extract the subspace identifier from a tumbler
fun subspace[t: Tumbler]: Val {
  t.e1
}

-- T7: Tumblers in different subspaces are necessarily distinct.
-- Proof sketch: e1 is a total function on Tumbler; if a = b then a.e1 = b.e1.
-- Contrapositive: a.e1 ≠ b.e1 implies a ≠ b.
assert SubspaceDisjointness {
  all a, b: Tumbler |
    not (subspace[a] = subspace[b]) implies not (a = b)
}

-- Non-vacuity: tumblers in two distinct subspaces can coexist
run FindDistinctSubspaces {
  some disj a, b: Tumbler | not (subspace[a] = subspace[b])
} for 5 but exactly 2 Tumbler

check SubspaceDisjointness for 5 but exactly 2 Tumbler
