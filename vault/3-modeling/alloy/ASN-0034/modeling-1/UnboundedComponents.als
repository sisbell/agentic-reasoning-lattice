open util/ordering[Idx]

-- Positions within a tumbler (fixed-length model)
sig Idx {}

-- A tumbler: maps each position to a natural-number component
sig Tumbler {
  comp: Idx -> one Int
}

-- Components are natural numbers
fact NatComponents {
  all t: Tumbler, i: Idx | t.comp[i] >= 0
}

-- T0(a) UnboundedComponents: for every tumbler t and position i,
-- there exists a tumbler t' agreeing with t on all other positions
-- but with a strictly larger component at i.
-- This is the one-step version of: components range over all of N.
assert UnboundedComponents {
  all t: Tumbler, i: Idx |
    some t2: Tumbler |
      t2.comp[i] > t.comp[i]
      and (all j: Idx - i | t2.comp[j] = t.comp[j])
}

check UnboundedComponents for 5 but exactly 3 Idx, 5 Int

-- Non-vacuity: at least one well-formed tumbler exists
run NonVacuity {
  some t: Tumbler | some Idx
} for 5 but exactly 3 Idx, 5 Int
