-- D7a — DocumentScopedAllocation (POST, ensures)
--
-- INSERT on document d allocates fresh I-addresses scoped under d.
-- Each fresh address a satisfies: d ≼ a, separator at position #d+1, zeros(a) = 3.
-- Fresh addresses have the form d.0.E₁...Eδ with all Eᵢ > 0 and δ ≥ 1.

-- Tumbler address hierarchy abstracted by zeros count.
-- AccountAddr (zeros=1), DocAddr (zeros=2), ElemAddr (zeros=3).
abstract sig Addr {}

sig AccountAddr extends Addr {}

sig DocAddr extends Addr {
  account: one AccountAddr
}

sig ElemAddr extends Addr {
  doc: one DocAddr
}

-- Prefix relation ≼ derived from address hierarchy.
-- Reflexive; AccountAddr prefixes its DocAddrs and their ElemAddrs;
-- DocAddr prefixes its ElemAddrs.
pred isPrefix[a, b: Addr] {
  a = b
  or (a in AccountAddr and b in DocAddr and b.account = a)
  or (a in AccountAddr and b in ElemAddr and b.doc.account = a)
  or (a in DocAddr and b in ElemAddr and b.doc = a)
}

-- Allocation state: tracks which element addresses exist.
sig State {
  allocated: set ElemAddr
}

-- INSERT operation: allocates fresh element addresses under document d.
pred Insert[s, sPost: State, d: DocAddr, fresh: set ElemAddr] {
  -- precondition: none of fresh already allocated
  no fresh & s.allocated

  -- nonempty allocation
  some fresh

  -- frame: only fresh addresses added
  sPost.allocated = s.allocated + fresh

  -- D7a postcondition: every fresh address scoped under d
  all a: fresh | a.doc = d
}

-- Consequence 1: every fresh address is prefixed by the target document
assert FreshPrefixedByTarget {
  all s, sPost: State, d: DocAddr, fresh: set ElemAddr |
    Insert[s, sPost, d, fresh] implies
      (all a: fresh | isPrefix[d, a])
}

-- Consequence 2: fresh addresses inherit the target document's account
assert FreshInTargetAccount {
  all s, sPost: State, d: DocAddr, fresh: set ElemAddr |
    Insert[s, sPost, d, fresh] implies
      (all a: fresh | isPrefix[d.account, a])
}

-- Consequence 3: no fresh address is under a different document
assert FreshNotUnderOtherDoc {
  all s, sPost: State, d: DocAddr, fresh: set ElemAddr |
    Insert[s, sPost, d, fresh] implies
      (no a: fresh, d2: DocAddr - d | a.doc = d2)
}

-- Non-vacuity: a valid Insert exists
run FindInsert {
  some s, sPost: State, d: DocAddr, fresh: set ElemAddr |
    Insert[s, sPost, d, fresh]
} for 5 but exactly 2 State

check FreshPrefixedByTarget for 5 but exactly 2 State
check FreshInTargetAccount for 5 but exactly 2 State
check FreshNotUnderOtherDoc for 5 but exactly 2 State
