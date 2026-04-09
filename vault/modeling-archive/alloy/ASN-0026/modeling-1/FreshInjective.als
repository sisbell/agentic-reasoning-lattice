-- P9: FreshInjective — new positions map to distinct addresses
--
-- Strengthens Insert so new positions use fresh addresses
-- (as FreshPositions establishes), then checks whether
-- injectivity over the inserted range follows.  A counterexample
-- shows injectivity is a necessary additional postcondition:
-- two positions can share the same fresh address.

sig Addr {}

sig State {
  dom_I: set Addr,
  vmap: Int -> lone Addr
}

fun len[s: State]: Int {
  #(s.vmap)
}

pred wellFormed[s: State] {
  -- positions are exactly the dense interval 1..len
  all i: Int | some s.vmap[i] iff (i >= 1 and i =< len[s])
  -- every mapped address is in the I-space domain
  Int.(s.vmap) in s.dom_I
}

pred Insert[s, s2: State, p: Int, fresh: set Addr] {
  -- preconditions
  p >= 1
  p =< plus[len[s], 1]
  no (fresh & s.dom_I)
  some fresh

  let k = #fresh {
    -- I-space domain extends with fresh
    s2.dom_I = s.dom_I + fresh

    -- positions before p: unchanged
    all j: Int | (j >= 1 and j < p) implies
      s2.vmap[j] = s.vmap[j]

    -- new positions p..p+k-1: each maps to a fresh address
    -- NOTE: does not require distinct addresses across positions
    all j: Int | (j >= p and j < plus[p, k]) implies
      (one s2.vmap[j] and s2.vmap[j] in fresh)

    -- shifted positions: old [p..len] move to [p+k..len+k]
    all j: Int | (j >= plus[p, k] and j =< plus[len[s], k]) implies
      s2.vmap[j] = s.vmap[minus[j, k]]

    -- no positions outside 1..len+k
    all j: Int | (j < 1 or j > plus[len[s], k]) implies
      no s2.vmap[j]
  }
}

-- P9: every pair of new positions maps to distinct addresses
assert FreshInjective {
  all s, s2: State, p: Int, fresh: set Addr |
    (wellFormed[s] and Insert[s, s2, p, fresh]) implies
      (let k = #fresh |
        all j1, j2: Int |
          (j1 >= p and j1 < plus[p, k] and
           j2 >= p and j2 < plus[p, k] and
           not (j1 = j2))
            implies not (s2.vmap[j1] = s2.vmap[j2]))
}

run NonVacuity {
  some s, s2: State, p: Int, fresh: set Addr |
    wellFormed[s] and Insert[s, s2, p, fresh] and #fresh > 1
} for 5 but exactly 2 State, 5 Int

check FreshInjective for 5 but exactly 2 State, 5 Int
