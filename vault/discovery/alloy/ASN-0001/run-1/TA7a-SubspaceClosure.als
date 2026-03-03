-- TA7a: SubspaceClosure
-- Ordinal-only formulation of V-space shift arithmetic.
-- Each position in subspace S1 is a single-component tumbler [x], x >= 0.
-- TumblerAdd:      [x] ⊕ [n] = [x + n]   (action point k=1, n > 0)
-- TumblerSubtract: [x] ⊖ [n] = [x − n]   (divergence k=1, or zero when x = n)
-- Closure: add result stays in S1; subtract result stays in S1 ∪ {[0]}.
--
-- Overflow guard: Alloy integers are finite-width. Each assertion includes
-- a witness that no wraparound occurred (plus[x,n] > x for add;
-- minus[x,n] < x for sub), so Alloy's modular arithmetic does not
-- produce spurious counterexamples.

sig Pos {
  ord: Int
}

-- S1: positions whose ordinal is non-negative
pred inS1[p: Pos] {
  p.ord >= 0
}

-- TumblerAdd on ordinals: [x] ⊕ [n] = [x + n]
fun ordAdd[x, n: Int]: Int {
  plus[x, n]
}

-- TumblerSubtract on ordinals: [x] ⊖ [n] = [x − n]
fun ordSub[x, n: Int]: Int {
  minus[x, n]
}

-- TA7a-Add: forward shift stays in S1
-- [x] ∈ S1, n > 0 => [x] ⊕ [n] = [x+n] ∈ S1  (i.e., x+n >= 0)
assert AddClosedInS1 {
  all p: Pos, n: Int |
    (inS1[p] and n > 0 and plus[p.ord, n] > p.ord) implies
      ordAdd[p.ord, n] >= 0
}

-- TA7a-Sub: backward shift stays in S1 ∪ {[0]}
-- [x] ∈ S1, n > 0, x >= n => [x] ⊖ [n] = [x-n] >= 0
assert SubClosedInS1 {
  all p: Pos, n: Int |
    (inS1[p] and n > 0 and p.ord >= n and minus[p.ord, n] < p.ord) implies
      ordSub[p.ord, n] >= 0
}

-- Non-vacuity: witness with both add and sub preconditions active
run SubspaceClosure_NV {
  some p: Pos, n: Int |
    inS1[p] and p.ord > 0 and n > 0 and p.ord >= n
} for 5 but 5 Int

check AddClosedInS1 for 5 but 5 Int
check SubClosedInS1 for 5 but 5 Int
