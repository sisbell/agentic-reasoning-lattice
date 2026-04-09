-- REF-STABILITY (RefStability): After any operation whose write target
-- is d_s, a distinct document d_t that shares I-addresses with d_s
-- retains all its V-space addresses in the I-space domain.

sig Addr {}
sig Byte {}
sig Doc {}
sig Pos {}

sig State {
  ispace : Addr -> lone Byte,       -- partial function Addr -> Byte
  vspace : Doc -> Pos -> lone Addr,  -- per-doc partial function Pos -> Addr
  docs   : set Doc                   -- existing documents
}

-- P2: every V-space address is allocated in I-space
pred wellFormed[s: State] {
  all d: s.docs, p: Pos |
    some s.vspace[d][p] implies s.vspace[d][p] in s.ispace.Byte
}

-- P1: I-space domain never shrinks
pred ispaceMonotonic[s, sPost: State] {
  s.ispace.Byte in sPost.ispace.Byte
}

-- P7: non-target documents have identical V-space
pred nonTargetPreserved[s, sPost: State, target: Doc] {
  all d: s.docs - target | sPost.vspace[d] = s.vspace[d]
}

-- Two documents share at least one I-address
pred sharesAddrs[s: State, ds, dt: Doc] {
  some a: Addr |
    a in Pos.(s.vspace[ds]) and a in Pos.(s.vspace[dt])
}

-- Generic operation: writes to target, satisfies P1 and P7
pred operation[s, sPost: State, target: Doc] {
  target in s.docs
  target in sPost.docs
  s.docs - target in sPost.docs
  ispaceMonotonic[s, sPost]
  nonTargetPreserved[s, sPost, target]
}

-- REF-STABILITY: d_t's V-space addresses remain valid after operation on d_s
assert RefStability {
  all s, sPost: State, ds, dt: Doc |
    (wellFormed[s]
     and ds != dt
     and dt in s.docs
     and sharesAddrs[s, ds, dt]
     and operation[s, sPost, ds])
    implies
    (all p: Pos |
       some sPost.vspace[dt][p] implies
         sPost.vspace[dt][p] in sPost.ispace.Byte)
}

-- Non-vacuity: a reachable scenario with shared addresses
run NonVacuity {
  some s, sPost: State, ds, dt: Doc |
    wellFormed[s]
    and ds != dt
    and dt in s.docs
    and sharesAddrs[s, ds, dt]
    and operation[s, sPost, ds]
    and some p: Pos | some s.vspace[dt][p]
} for 4 but exactly 2 State

check RefStability for 5 but exactly 2 State
