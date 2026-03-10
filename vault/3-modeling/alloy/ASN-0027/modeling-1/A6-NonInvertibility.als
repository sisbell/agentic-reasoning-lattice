-- A6 — NonInvertibility
-- DELETE then INSERT at the same position cannot restore the original
-- addresses, because INSERT introduces fresh addresses.

sig Addr {}

sig State {
  vals: Int -> lone Addr
}

-- All addresses appearing in state s
fun addrsOf[s: State]: set Addr {
  Int.(s.vals)
}

-- State s is a contiguous 1-indexed sequence of length n
pred hasLength[s: State, n: Int] {
  n >= 0
  all i: Int | some s.vals[i] iff (1 =< i and i =< n)
}

-- Each position maps to a distinct address
pred injective[s: State] {
  all i, j: Int |
    (some s.vals[i] and some s.vals[j] and s.vals[i] = s.vals[j])
    implies i = j
}

-- DELETE: remove k entries at positions p..p+k-1, shift remainder left
pred Delete[s0, s1: State, n0, p, k: Int] {
  hasLength[s0, n0]
  injective[s0]
  k >= 1
  1 =< p
  plus[p, minus[k, 1]] =< n0
  let n1 = minus[n0, k] {
    hasLength[s1, n1]
    -- below p: unchanged
    all i: Int | (1 =< i and i < p) implies s1.vals[i] = s0.vals[i]
    -- from p onward: shifted left by k
    all i: Int | (p =< i and i =< n1) implies s1.vals[i] = s0.vals[plus[i, k]]
  }
}

-- INSERT: place k fresh addresses at positions p..p+k-1, shift rest right
pred Insert[s1, s2: State, n1, p, k: Int, fresh: set Addr] {
  hasLength[s1, n1]
  k >= 1
  1 =< p
  p =< plus[n1, 1]
  #fresh = k
  let n2 = plus[n1, k] {
    hasLength[s2, n2]
    -- below p: unchanged
    all i: Int | (1 =< i and i < p) implies s2.vals[i] = s1.vals[i]
    -- inserted range: each position gets a distinct fresh address
    all i: Int | (p =< i and i < plus[p, k]) implies s2.vals[i] in fresh
    all a: fresh | one i: Int | (p =< i and i < plus[p, k]) and s2.vals[i] = a
    -- above inserted range: shifted from s1
    all i: Int | (plus[p, k] =< i and i =< n2) implies
      s2.vals[i] = s1.vals[minus[i, k]]
  }
}

-- A6: after delete then insert with globally fresh addresses,
-- the values at affected positions differ from the originals
assert NonInvertibility {
  all s0, s1, s2: State, n0, p, k: Int, fresh: set Addr |
    (Delete[s0, s1, n0, p, k]
     and Insert[s1, s2, minus[n0, k], p, k, fresh]
     and no (fresh & addrsOf[s0]))
    implies
    (all j: Int | (0 =< j and j < k) implies
      not (s2.vals[plus[p, j]] = s0.vals[plus[p, j]]))
}

-- Non-vacuity: find a scenario where delete-then-insert occurs
run NonVacuity {
  some s0, s1, s2: State, n0, p, k: Int, fresh: set Addr |
    Delete[s0, s1, n0, p, k]
    and Insert[s1, s2, minus[n0, k], p, k, fresh]
    and no (fresh & addrsOf[s0])
} for 6 but exactly 3 State, 4 Int

check NonInvertibility for 6 but exactly 3 State, 4 Int
