-- P2 — NoReuse (LEMMA)
-- Derived from P0 (ISpaceGrowth) ∧ P1 (ContentImmutability).
-- (A i, j : 0 ≤ i ≤ j ∧ a ∈ Σᵢ.A : Σⱼ.ι(a) = Σᵢ.ι(a))
-- Content at an allocated address is the same in any later state.

open util/ordering[State]

sig IAddr {}
sig Value {}

sig State {
  iota: IAddr -> lone Value        -- Σ.ι : IAddr ⇸ Value
}

-- Σ.A = dom(Σ.ι)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- P0 axiom on consecutive transitions: allocated addresses only grow
fact P0_ISpaceGrowth {
  all s: State - last |
    allocated[s] in allocated[s.next]
}

-- P1 axiom on consecutive transitions: content at allocated addresses is preserved
fact P1_ContentImmutability {
  all s: State - last |
    all a: allocated[s] | s.next.iota[a] = s.iota[a]
}

-- P2: content preserved across any span i ≤ j
assert P2_NoReuse {
  all si, sj: State |
    gte[sj, si] implies
      all a: allocated[si] | sj.iota[a] = si.iota[a]
}

-- Non-vacuity: a trace where allocation grows across steps
run NonVacuity {
  some s: State - last |
    some allocated[s]
    and some allocated[s.next] - allocated[s]
} for 4 but exactly 3 State

check P2_NoReuse for 5 but exactly 4 State
check P2_NoReuse for 5 but exactly 5 State
