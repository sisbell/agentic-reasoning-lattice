-- P9: FreshPositions — new positions map to freshly allocated addresses
--
-- Checks whether freshness of inserted addresses follows from
-- structural insert constraints alone. Insert allocates fresh
-- addresses and extends the vmap with shifting, but does NOT
-- constrain new positions to use fresh addresses specifically.
-- P9 asserts that constraint; a counterexample demonstrates
-- P9 is a necessary postcondition.

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

    -- new positions p..p+k-1: each has exactly one address
    -- NOTE: deliberately unconstrained WHICH address
    all j: Int | (j >= p and j < plus[p, k]) implies
      one s2.vmap[j]

    -- shifted positions: old [p..len] move to [p+k..len+k]
    all j: Int | (j >= plus[p, k] and j =< plus[len[s], k]) implies
      s2.vmap[j] = s.vmap[minus[j, k]]

    -- no positions outside 1..len+k
    all j: Int | (j < 1 or j > plus[len[s], k]) implies
      no s2.vmap[j]
  }
}

-- P9: every new position maps to a fresh address
assert FreshPositions {
  all s, s2: State, p: Int, fresh: set Addr |
    (wellFormed[s] and Insert[s, s2, p, fresh]) implies
      (let k = #fresh |
        all j: Int | (j >= p and j < plus[p, k]) implies
          s2.vmap[j] in fresh)
}

run NonVacuity {
  some s, s2: State, p: Int, fresh: set Addr |
    wellFormed[s] and Insert[s, s2, p, fresh]
} for 5 but exactly 2 State, 5 Int

check FreshPositions for 5 but exactly 2 State, 5 Int
