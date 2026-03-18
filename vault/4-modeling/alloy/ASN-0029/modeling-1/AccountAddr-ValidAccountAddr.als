-- AccountAddr-ValidAccountAddr.als
-- ASN-0029: AccountAddr = {a in T : zeros(a) = 1}
-- Account addresses are tumblers with exactly one zero separator (form N.0.U).

sig Tumbler {
  zeros: Int
}

-- Address levels: 0=node, 1=account, 2=document, 3=element
fact ValidZeros {
  all t: Tumbler | t.zeros >= 0 and t.zeros =< 3
}

-- AccountAddr is the subset of tumblers with exactly one zero
sig AccountAddr in Tumbler {}

fact AccountAddrDef {
  AccountAddr = { t: Tumbler | t.zeros = 1 }
}

-- Main property: membership iff zeros = 1
assert ValidAccountAddr {
  all t: Tumbler |
    t in AccountAddr iff t.zeros = 1
}

-- Derived: account addresses are disjoint from document-level addresses
assert AccountDisjointFromDoc {
  no t: Tumbler | t in AccountAddr and t.zeros = 2
}

-- Derived: non-account tumblers are exactly those with zeros != 1
assert ComplementCharacterization {
  all t: Tumbler |
    t not in AccountAddr iff t.zeros != 1
}

-- Non-vacuity: satisfiable with accounts and non-accounts
run NonVacuity {
  some AccountAddr
  some Tumbler - AccountAddr
} for 5 but 4 Int

check ValidAccountAddr for 5 but 4 Int
check AccountDisjointFromDoc for 5 but 4 Int
check ComplementCharacterization for 5 but 4 Int
