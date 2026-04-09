-- A2-AccessibilityPartition.als
-- For any T4 address a and state Σ satisfying P2 (ReferentiallyComplete),
-- exactly one of: active, unreferenced, unallocated.

sig Addr {}

sig Doc {}

sig State {
  allocated: set Addr,           -- dom(Σ.I)
  ref: Doc -> set Addr           -- references: Σ.V(d)(p) values
}

-- P2 (ReferentiallyComplete): every referenced address is allocated
pred ReferentiallyComplete[s: State] {
  all d: Doc | d.(s.ref) in s.allocated
}

-- reachable(a) ≡ some document references a
pred reachable[s: State, a: Addr] {
  a in Doc.(s.ref)
}

-- (i) active: allocated and reachable
pred active[s: State, a: Addr] {
  a in s.allocated and reachable[s, a]
}

-- (ii) unreferenced: allocated but not reachable
pred unreferenced[s: State, a: Addr] {
  a in s.allocated and not reachable[s, a]
}

-- (iii) unallocated: not in dom(I)
pred unallocated[s: State, a: Addr] {
  a not in s.allocated
}

-- A2: the three categories are exhaustive and mutually exclusive
assert AccessibilityPartition {
  all s: State | ReferentiallyComplete[s] implies
    all a: Addr |
      -- exhaustive
      (active[s, a] or unreferenced[s, a] or unallocated[s, a])
      and
      -- mutually exclusive (pairwise)
      not (active[s, a] and unreferenced[s, a])
      and
      not (active[s, a] and unallocated[s, a])
      and
      not (unreferenced[s, a] and unallocated[s, a])
}

-- Key sub-property: P2 rules out the fourth combination
assert ReachableImpliesAllocated {
  all s: State | ReferentiallyComplete[s] implies
    all a: Addr | reachable[s, a] implies a in s.allocated
}

check AccessibilityPartition for 5
check ReachableImpliesAllocated for 5

-- Non-vacuity: all three categories coexist in a single state
run ThreeCategories {
  some s: State | {
    ReferentiallyComplete[s]
    some a1: Addr | active[s, a1]
    some a2: Addr | unreferenced[s, a2]
    some a3: Addr | unallocated[s, a3]
  }
} for 5 but exactly 1 State
