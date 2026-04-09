-- P4 — CreationBasedIdentity
-- Distinct allocation acts produce distinct I-addresses.
-- Restatement of GlobalUniqueness from ASN-0001.

sig Addr {}

-- An allocation act: the event of allocating a fresh I-address.
-- Each act yields exactly one address.
sig Allocation {
  result: one Addr
}

-- The core axiom: distinct allocations produce distinct addresses.
-- This is the GlobalUniqueness guarantee from ASN-0001.
fact GlobalUniqueness {
  all disj a1, a2: Allocation | a1.result != a2.result
}

-- P4: CreationBasedIdentity — the property as an assertion.
-- If two allocations yield the same address, they are the same allocation.
assert CreationBasedIdentity {
  all a1, a2: Allocation |
    a1.result = a2.result implies a1 = a2
}

-- Equivalent contrapositive form: distinct allocations, distinct addresses.
assert CreationBasedIdentity_contra {
  all disj a1, a2: Allocation |
    a1.result != a2.result
}

-- Non-vacuity: multiple allocations can coexist, each with a distinct address.
run NonVacuity {
  #Allocation > 1
} for 5

check CreationBasedIdentity for 5
check CreationBasedIdentity_contra for 5
