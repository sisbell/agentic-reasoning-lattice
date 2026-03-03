open util/ordering[Tumbler]

-- Tumblers are abstract addresses; the ordering here instantiates tumbler comparison
-- (a < b iff TumblerAdd can produce b from a with a positive displacement).
sig Tumbler {}

-- Each allocator owns a non-overlapping address prefix and allocates from it sequentially.
sig Allocator {}

-- An allocation record: the pos-th address issued by owner.
sig AllocRec {
  owner : one Allocator,
  pos   : one Int,
  addr  : one Tumbler
}

-- System state: the set of allocation records accumulated so far.
sig State {
  active : set AllocRec
}

-- Structural wellformedness:
--   (owner, pos) pairs are unique, positions are non-negative, and per-allocator
--   indices are contiguous (no gaps).
pred wf[s: State] {
  all r1, r2: s.active |
    (r1.owner = r2.owner and r1.pos = r2.pos) implies r1 = r2
  all r: s.active | r.pos >= 0
  all r: s.active | r.pos > 0 implies
    some r2: s.active | r2.owner = r.owner and r2.pos = minus[r.pos, 1]
}

-- T9 — ForwardAllocation:
--   Within each allocator's sequence, addresses are strictly monotonically increasing.
--   Captures: (A a, b : same_allocator(a,b) ∧ allocated_before(a,b) : a < b)
pred ForwardAllocation[s: State] {
  all r1, r2: s.active |
    (r1.owner = r2.owner and r1.pos < r2.pos) implies lt[r1.addr, r2.addr]
}

-- Allocate: allocator al appends address t as its next allocation.
-- Precondition: t must exceed every address already issued by al.
-- This precondition is the operational guarantee that drives T9.
pred Allocate[s, sPost: State, al: Allocator, t: Tumbler] {
  -- Pre: forward allocation — t is strictly greater than all of al's prior addresses
  all r: s.active | r.owner = al implies lt[r.addr, t]
  -- Post: a fresh record is appended at the next sequential position
  let nxt = #{r: s.active | r.owner = al} |
  some nr: AllocRec - s.active {
    nr.owner = al
    nr.pos   = nxt
    nr.addr  = t
    sPost.active = s.active + nr
  }
}

-- T9 is preserved by every well-typed Allocate step.
assert AllocatePreservesT9 {
  all s, sPost: State, al: Allocator, t: Tumbler |
    (wf[s] and ForwardAllocation[s] and Allocate[s, sPost, al, t])
    implies ForwardAllocation[sPost]
}

-- Non-vacuity: a valid state satisfying T9 with at least two allocations per allocator exists.
run NonVacuous {
  some s: State |
    wf[s] and ForwardAllocation[s] and
    some al: Allocator | #{r: s.active | r.owner = al} >= 2
} for 5 but exactly 1 State, 4 Int

check AllocatePreservesT9 for 5 but exactly 2 State, 4 Int
