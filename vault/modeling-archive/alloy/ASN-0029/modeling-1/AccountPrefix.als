-- AccountPrefix.als
-- ASN-0029: account(d) = max≼ {a ∈ AccountAddr : a ≼ d}
-- The account prefix extracts the unique account-level ancestor
-- from any address at or below account depth.

sig Tumbler {
  zeros: Int,
  parent: lone Tumbler
}

-- Tumbler addresses form a tree ordered by zero-separator depth
fact TreeStructure {
  -- acyclic
  no t: Tumbler | t in t.^parent

  -- non-negative zeros
  all t: Tumbler | t.zeros >= 0

  -- root (node-level) iff zeros = 0
  all t: Tumbler | t.zeros = 0 iff no t.parent

  -- each parent step decrements zeros by exactly one
  all t: Tumbler | some t.parent implies
    t.parent.zeros = minus[t.zeros, 1]
}

-- AccountAddr: tumblers with exactly one zero-separator (form N.0.U)
fun AccountAddr: set Tumbler {
  { t: Tumbler | t.zeros = 1 }
}

-- account(d): the unique AccountAddr on the prefix path of d
fun account[d: Tumbler]: set Tumbler {
  AccountAddr & d.*parent
}

-- Every address at or below account level has exactly one account prefix
assert AccountPrefixTotal {
  all d: Tumbler | d.zeros >= 1 implies one account[d]
}

-- account is idempotent on AccountAddr
assert AccountIdempotent {
  all a: AccountAddr | account[a] = a
}

-- account(d) is stable under nesting: account(d) = account(parent(d))
-- for any address strictly below account level
assert AccountPrefixStable {
  all d: Tumbler | d.zeros >= 2 implies
    account[d] = account[d.parent]
}

-- Non-vacuity: model with node, account, and document levels
run NonVacuity {
  some d: Tumbler | d.zeros = 2
  #Tumbler > 2
} for 5 but 4 Int

check AccountPrefixTotal for 6 but 4 Int
check AccountIdempotent for 6 but 4 Int
check AccountPrefixStable for 6 but 4 Int
