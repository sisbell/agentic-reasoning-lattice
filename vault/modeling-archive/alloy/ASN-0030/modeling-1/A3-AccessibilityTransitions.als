-- A3-AccessibilityTransitions.als
-- Which transitions between accessibility states are permitted/forbidden
-- under address permanence (P1).
--
-- States:
--   (i)   active:       allocated and reachable
--   (ii)  unreferenced: allocated and not reachable
--   (iii) unallocated:  not allocated
--
-- Transitions:
--   (a) iii -> i    permitted
--   (b) i   -> ii   permitted
--   (c) ii  -> i    permitted by invariants
--   (d) i   -> iii  forbidden (violates P1)
--   (e) ii  -> iii  forbidden (violates P1)
--   (f) iii -> ii   composite: (a) then (b)

sig Addr {}

sig Doc {}

sig State {
  allocated: set Addr,
  ref: Doc -> set Addr
}

-- P1 (address permanence): allocated set only grows
pred Permanence[s, s2: State] {
  s.allocated in s2.allocated
}

-- P2 (referentially complete): every referenced address is allocated
pred ReferentiallyComplete[s: State] {
  all d: Doc | d.(s.ref) in s.allocated
}

-- Accessibility predicates (from A2)
pred active[s: State, a: Addr] {
  a in s.allocated and a in Doc.(s.ref)
}

pred unreferenced[s: State, a: Addr] {
  a in s.allocated and a not in Doc.(s.ref)
}

pred unallocated[s: State, a: Addr] {
  a not in s.allocated
}

-- Frame: all addresses other than a are unchanged
pred frame[s, s2: State, a: Addr] {
  all a2: Addr - a {
    a2 in s.allocated iff a2 in s2.allocated
    all d: Doc | a2 in d.(s.ref) iff a2 in d.(s2.ref)
  }
}

-- (a) iii -> i: allocate and reference
pred trans_a[s, s2: State, a: Addr] {
  unallocated[s, a]
  active[s2, a]
  Permanence[s, s2]
  ReferentiallyComplete[s2]
  frame[s, s2, a]
}

-- (b) i -> ii: drop all references
pred trans_b[s, s2: State, a: Addr] {
  active[s, a]
  unreferenced[s2, a]
  Permanence[s, s2]
  ReferentiallyComplete[s2]
  frame[s, s2, a]
}

-- (c) ii -> i: re-reference an allocated address
pred trans_c[s, s2: State, a: Addr] {
  unreferenced[s, a]
  active[s2, a]
  Permanence[s, s2]
  ReferentiallyComplete[s2]
  frame[s, s2, a]
}

-- (d) i -> iii: deallocate a reachable address (forbidden)
pred trans_d[s, s2: State, a: Addr] {
  active[s, a]
  unallocated[s2, a]
  Permanence[s, s2]
  frame[s, s2, a]
}

-- (e) ii -> iii: deallocate an unreferenced address (forbidden)
pred trans_e[s, s2: State, a: Addr] {
  unreferenced[s, a]
  unallocated[s2, a]
  Permanence[s, s2]
  frame[s, s2, a]
}

-- (f) iii -> ii: composite via (a) then (b)
pred trans_f[s, sMid, s2: State, a: Addr] {
  trans_a[s, sMid, a]
  trans_b[sMid, s2, a]
}

---------------------------------------------------------------
-- ASSERTIONS: (d) and (e) are forbidden under Permanence
---------------------------------------------------------------

assert TransD_Forbidden {
  no s, s2: State, a: Addr | trans_d[s, s2, a]
}

assert TransE_Forbidden {
  no s, s2: State, a: Addr | trans_e[s, s2, a]
}

check TransD_Forbidden for 5 but exactly 2 State
check TransE_Forbidden for 5 but exactly 2 State

---------------------------------------------------------------
-- NON-VACUITY: permitted transitions are achievable
---------------------------------------------------------------

run FindTransA {
  some s, s2: State, a: Addr |
    ReferentiallyComplete[s] and trans_a[s, s2, a]
} for 4 but exactly 2 State

run FindTransB {
  some s, s2: State, a: Addr |
    ReferentiallyComplete[s] and trans_b[s, s2, a]
} for 4 but exactly 2 State

run FindTransC {
  some s, s2: State, a: Addr |
    ReferentiallyComplete[s] and trans_c[s, s2, a]
} for 4 but exactly 2 State

run FindTransF {
  some s, sMid, s2: State, a: Addr |
    ReferentiallyComplete[s] and trans_f[s, sMid, s2, a]
} for 5 but exactly 3 State
