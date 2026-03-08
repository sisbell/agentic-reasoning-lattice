-- P4 — RearrangementContentInvariance
-- Rearrangement (permutation of v-positions) preserves the occurrence
-- count of each address in the v-space of document d.

sig IAddr {}
sig VPos {}

sig State {
  -- v(d) for a fixed document d: partial function from VPos to IAddr
  v: VPos -> lone IAddr
}

-- Permutation used by rearrangement
one sig Perm {
  pi: VPos -> lone VPos
}

pred rearrange[s, sPost: State] {
  let D = (s.v).IAddr, p = Perm.pi {
    -- pi is a bijection on dom(s.v)
    p in D -> D
    all q: D | one q.p       -- total on D
    all q: D | one p.q       -- injective (surjective follows on finite D)
    -- post-state v-map is pre-state v-map with positions permuted
    sPost.v = ~p . (s.v)
  }
}

-- P4: for every address, the count of positions mapping to it is unchanged
assert P4_RearrangementContentInvariance {
  all s, sPost: State |
    rearrange[s, sPost] implies
      all a: IAddr |
        #{p: VPos | p.(s.v) = a} = #{p: VPos | p.(sPost.v) = a}
}

-- Non-vacuity: a non-trivial rearrangement exists
run NonVacuity {
  some s, sPost: State |
    s != sPost and rearrange[s, sPost]
} for 4 but exactly 2 State, 4 Int

check P4_RearrangementContentInvariance for 5 but exactly 2 State, 5 Int
