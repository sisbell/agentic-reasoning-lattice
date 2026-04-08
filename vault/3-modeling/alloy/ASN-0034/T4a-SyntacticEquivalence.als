open util/ordering[Pos]

-- Each Pos atom is one position in the tumbler; the ordering
-- gives the sequence index (1-indexed in the spec, order-indexed here).
sig Pos {
  val: Int
}

-- T4 positive-component constraint: every component is a
-- non-negative integer (0 = field separator, >0 = field component).
fact positiveComponents {
  all p: Pos | p.val >= 0
}

-- Tumbler is non-empty.
fact nonEmpty {
  some Pos
}

pred isSep[p: Pos] {
  p.val = 0
}

pred isComp[p: Pos] {
  p.val > 0
}

-- Semantic predicate: non-empty field constraint.
-- Every present field (maximal contiguous run of components
-- between separators or tumbler boundaries) has >= 1 component.
pred nonEmptyFieldConstraint {
  -- First field non-empty: position 1 is a component
  isComp[first]

  -- Last field non-empty: last position is a component
  isComp[last]

  -- Interior fields: between any two consecutive separators
  -- (no separator strictly between them), at least one component exists
  all p, q: Pos |
    (isSep[p] and isSep[q] and lt[p, q]
     and no r: Pos | isSep[r] and lt[p, r] and lt[r, q])
    implies
    (some s: Pos | lt[p, s] and lt[s, q] and isComp[s])
}

-- Syntactic predicate: three conditions on the raw tumbler.
pred syntacticConditions {
  -- (i) no two zeros are adjacent
  all p: Pos | some p.next implies
    not (isSep[p] and isSep[p.next])

  -- (ii) t_1 != 0
  not isSep[first]

  -- (iii) t_{#t} != 0
  not isSep[last]
}

-- T4a forward: non-empty fields => syntactic conditions
assert forwardDirection {
  nonEmptyFieldConstraint implies syntacticConditions
}

-- T4a reverse: syntactic conditions => non-empty fields
assert reverseDirection {
  syntacticConditions implies nonEmptyFieldConstraint
}

-- T4a equivalence (both directions)
assert syntacticEquivalence {
  nonEmptyFieldConstraint iff syntacticConditions
}

-- Non-vacuity: find a multi-field tumbler satisfying the constraint
run nonVacuity {
  nonEmptyFieldConstraint
  some p: Pos | isSep[p]
} for 6 but 5 Int

check forwardDirection for 7 but 5 Int
check reverseDirection for 7 but 5 Int
check syntacticEquivalence for 7 but 5 Int
