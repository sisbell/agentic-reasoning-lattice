-- D3-StructuralOwnership.als
-- Property D3: account(d) is computable from d's tumbler address alone,
-- without consulting any mutable state.
-- By T6 (DecidableContainment), same-owner is decidable from addresses.

sig Tumbler {
  zeros: Int,
  parent: lone Tumbler
}

fact TreeStructure {
  no t: Tumbler | t in t.^parent
  all t: Tumbler | t.zeros >= 0
  all t: Tumbler | t.zeros = 0 iff no t.parent
  all t: Tumbler | some t.parent implies
    t.parent.zeros = minus[t.zeros, 1]
}

fun AccountAddr: set Tumbler {
  { t: Tumbler | t.zeros = 1 }
}

fun DocAddr: set Tumbler {
  { t: Tumbler | t.zeros = 2 }
}

-- account(d): structural — depends only on address topology
fun account[d: Tumbler]: set Tumbler {
  AccountAddr & d.*parent
}

----------------------------------------------------------------------
-- Mutable state with hypothetical state-dependent ownership
----------------------------------------------------------------------

sig State {
  docs: set Tumbler,
  assignedOwner: Tumbler -> lone Tumbler
}

-- Any state-assigned owner must be a valid account ancestor
fact AssignedOwnerValid {
  all s: State, d: DocAddr & s.docs |
    some s.assignedOwner[d] implies
      s.assignedOwner[d] in AccountAddr & d.*parent
}

----------------------------------------------------------------------
-- D3 assertions
----------------------------------------------------------------------

-- D3a: account is a well-defined total function on document addresses
assert AccountWellDefined {
  all d: DocAddr | one account[d]
}

-- D3b: any valid state-assigned owner is forced to agree with
-- the structural account (the tree leaves no alternative)
assert StructuralOwnership {
  all s: State, d: DocAddr & s.docs |
    some s.assignedOwner[d] implies
      s.assignedOwner[d] = account[d]
}

-- D3c: same-owner decidable from addresses — shared account
-- reduces to shared parent in the address tree
assert SameOwnerDecidable {
  all d1, d2: DocAddr |
    (account[d1] = account[d2]) iff (d1.parent = d2.parent)
}

----------------------------------------------------------------------
-- Scope
----------------------------------------------------------------------

run NonVacuity {
  some d1, d2: DocAddr | d1 != d2 and account[d1] = account[d2]
  some s: State, d: DocAddr | d in s.docs and some s.assignedOwner[d]
} for 5 but 4 Int

check AccountWellDefined for 6 but 4 Int
check StructuralOwnership for 6 but 4 Int
check SameOwnerDecidable for 6 but 4 Int
