-- A8 — ReferencePermanence (LEMMA, lemma)
-- Property: Let a in dom(Sigma.I). For any finite sequence of operations
-- producing state Sigma_n:
--   (i)  a in dom(Sigma_n.I)
--   (ii) Sigma_n.I(a) = Sigma.I(a)
--
-- Follows from A1 (ISpaceFrame): each operation either preserves I-space
-- exactly (Delete, Rearrange, Copy, Version) or extends it (Insert, which
-- adds fresh addresses but preserves all existing mappings).

open util/ordering[State]

sig Address {}
sig Char {}

sig State {
  ispace: Address -> lone Char
}

-- Domain of I-space
fun idom[s: State]: set Address {
  (s.ispace).Char
}

-- INSERT effect on I-space: domain grows, existing mappings preserved
pred Insert[s, sPost: State] {
  idom[s] in idom[sPost]
  all a: idom[s] | sPost.ispace[a] = s.ispace[a]
  some idom[sPost] - idom[s]
}

-- PRESERVE: I-space unchanged (covers Delete, Rearrange, Copy, Version)
pred Preserve[s, sPost: State] {
  sPost.ispace = s.ispace
}

-- Each transition is either Insert or Preserve
pred step[s, sPost: State] {
  Insert[s, sPost] or Preserve[s, sPost]
}

-- Trace: consecutive states are linked by valid operations
fact trace {
  all s: State - last | step[s, s.next]
}

-- A8(i): domain permanence — address stays in dom(I)
assert ReferencePermanence_dom {
  all a: Address |
    a in idom[first] implies
      all s: State | a in idom[s]
}

-- A8(ii): value permanence — I(a) never changes
assert ReferencePermanence_val {
  all a: Address |
    a in idom[first] implies
      all s: State | s.ispace[a] = first.ispace[a]
}

-- Combined: both (i) and (ii)
assert ReferencePermanence {
  all a: Address |
    a in idom[first] implies
      all s: State | (a in idom[s] and s.ispace[a] = first.ispace[a])
}

-- Non-vacuity: find a trace where the initial state has a non-empty I-space
-- and at least one Insert occurs
run FindTrace {
  some idom[first]
  some s: State - last | Insert[s, s.next]
} for 5 but exactly 4 State

check ReferencePermanence_dom for 5 but exactly 4 State
check ReferencePermanence_val for 5 but exactly 4 State
check ReferencePermanence for 5 but exactly 4 State
