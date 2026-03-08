-- DomainPreservation
-- REARRANGE preserves dom(v(d)): dom(Σ'.v(d)) = dom(Σ.v(d))

sig IAddr {}
sig VPos {}

sig State {
  v: VPos -> lone IAddr
}

one sig Perm {
  pi: VPos -> lone VPos
}

pred rearrange[s, sPost: State] {
  let D = (s.v).IAddr, p = Perm.pi {
    -- pi is a bijection on dom(s.v)
    p in D -> D
    all q: D | one q.p
    all q: D | one p.q
    -- post-state v-map is pre-state composed with inverse permutation
    sPost.v = ~p . (s.v)
  }
}

assert DomainPreservation {
  all s, sPost: State |
    rearrange[s, sPost] implies
      (sPost.v).IAddr = (s.v).IAddr
}

-- Non-vacuity: a non-trivial rearrangement exists
run NonVacuity {
  some s, sPost: State |
    s != sPost and rearrange[s, sPost]
} for 4 but exactly 2 State, 4 Int

check DomainPreservation for 5 but exactly 2 State, 5 Int
