open util/ordering[Step]

-- Allocation time steps
sig Step {}

-- Tumbler: fixed-length sequence of 3 natural-number components
sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
}

-- Model natural numbers: all components non-negative
fact NonNegative {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Lexicographic strict less-than on tumblers
pred tlt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- Action point: index of first nonzero component in positive tumbler
fun actionPoint[w: Tumbler]: Int {
  (w.c1 > 0) => 1 else ((w.c2 > 0) => 2 else 3)
}

-- TumblerAdd: result = a + w
-- At action point k: copy a before k, add at k, copy w after k
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  let k = actionPoint[w] {
    k = 1 implies (
      result.c1 = plus[a.c1, w.c1] and
      result.c2 = w.c2 and
      result.c3 = w.c3
    )
    k = 2 implies (
      result.c1 = a.c1 and
      result.c2 = plus[a.c2, w.c2] and
      result.c3 = w.c3
    )
    k = 3 implies (
      result.c1 = a.c1 and
      result.c2 = a.c2 and
      result.c3 = plus[a.c3, w.c3]
    )
  }
}

-- Allocator: advances position via TumblerAdd at each step
-- Displacement is an explicit field to avoid expensive existential
sig Allocator {
  pos: Step -> one Tumbler,
  disp: Step -> lone Tumbler
}

fact AllocatorAdvances {
  all al: Allocator {
    -- No displacement at the last step
    no al.disp[last]
    -- At every non-last step, the displacement drives TumblerAdd
    all s: Step - last |
      tumblerAdd[al.pos[s], al.disp[s], al.pos[s.next]]
  }
}

-- T9: ForwardAllocation — within an allocator's stream,
-- earlier allocations produce strictly smaller addresses
assert ForwardAllocation {
  all al: Allocator, s1, s2: Step |
    lt[s1, s2] implies tlt[al.pos[s1], al.pos[s2]]
}

check ForwardAllocation for 4 but exactly 2 Step, exactly 1 Allocator, 4 Int

-- Non-vacuity: an allocator with forward-increasing positions exists
run NonVacuity {
  some al: Allocator, s1, s2: Step |
    lt[s1, s2] and tlt[al.pos[s1], al.pos[s2]]
} for 4 but exactly 2 Step, exactly 1 Allocator, 4 Int
