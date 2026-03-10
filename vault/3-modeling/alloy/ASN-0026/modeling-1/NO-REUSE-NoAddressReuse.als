-- NO-REUSE — NoAddressReuse
-- Address reuse is impossible: once allocated with content c,
-- an address is never freed (P1) and its content never changes (P0),
-- so it is never available for reallocation.

sig Addr {}
sig Byte {}

sig State {
  ispace: Addr -> lone Byte   -- partial function: I-space map
}

-- P0: Content immutability — allocated addresses keep their content
pred ContentImmutable[s, sPost: State] {
  all a: dom[s] | sPost.ispace[a] = s.ispace[a]
}

-- P1: Address permanence — allocated addresses stay allocated
pred AddressPermanent[s, sPost: State] {
  dom[s] in dom[sPost]
}

-- Domain of I-space: allocated addresses
fun dom[s: State]: set Addr {
  (s.ispace).Byte
}

-- Valid transition: satisfies both P0 and P1, may allocate new addresses
pred Step[s, sPost: State] {
  ContentImmutable[s, sPost]
  AddressPermanent[s, sPost]
}

-- An address is "reused" if it was allocated, then freed, then reallocated
-- with different content. Under P0+P1 this should be impossible.

-- Strong form: content at any allocated address never changes across a step
assert NoAddressReuse {
  all s, sPost: State |
    Step[s, sPost] implies
      (all a: dom[s] | sPost.ispace[a] = s.ispace[a])
}

-- Weaker form: an address allocated in s cannot appear in sPost
-- mapped to a different byte
assert NoContentChange {
  all s, sPost: State, a: Addr, c1, c2: Byte |
    (a -> c1 in s.ispace and Step[s, sPost] and a -> c2 in sPost.ispace)
      implies c1 = c2
}

-- Three-state form: no free-then-reallocate sequence
-- If a is allocated in s1, it remains allocated with same content in s3
-- after two arbitrary valid transitions
assert NoReuseTwoSteps {
  all s1, s2, s3: State |
    (Step[s1, s2] and Step[s2, s3]) implies
      (all a: dom[s1] | a in dom[s3] and s3.ispace[a] = s1.ispace[a])
}

-- Non-vacuity: a valid step exists where new addresses are allocated
run NonVacuity {
  some s, sPost: State |
    Step[s, sPost]
    and some dom[sPost] - dom[s]   -- at least one new allocation
} for 4 but exactly 2 State, 4 Int

check NoAddressReuse for 5 but exactly 2 State
check NoContentChange for 5 but exactly 2 State
check NoReuseTwoSteps for 5 but exactly 3 State
