-- J2-LinkContiguity.als
-- LinkContiguity: link-position ordinals in each document form {1, ..., n}

sig IAddr {}

abstract sig Tag {}
one sig TextTag, LinkTag extends Tag {}

sig VPos {
  tag: one Tag,
  ord: one Int
} {
  ord > 0
}

-- VPos faithfully represents (Tag x N+): no duplicate (tag, ord) pairs
fact VPosDistinct {
  all disj p, q: VPos | p.tag != q.tag or p.ord != q.ord
}

sig State {
  docs: set IAddr,
  vmap: IAddr -> VPos -> lone IAddr
} {
  -- vmap only defined for documents
  all d: IAddr | (some q: VPos | some vmap[d][q]) implies d in docs
}

-- Link positions active in document d
fun linkPositions[s: State, d: IAddr]: set VPos {
  {q: VPos | q.tag = LinkTag and some s.vmap[d][q]}
}

-- J2: LinkContiguity
-- n distinct positive integers all =< n must be exactly {1, ..., n}
-- (by pigeonhole, combined with VPosDistinct and ord > 0)
pred LinkContiguity[s: State] {
  all d: s.docs |
    all q: linkPositions[s, d] |
      q.ord =< #linkPositions[s, d]
}

-- Consequence: no gaps in the ordinal sequence
assert ContiguityImpliesNoGaps {
  all s: State | LinkContiguity[s] implies
    all d: s.docs, q: linkPositions[s, d] |
      q.ord > 1 implies
        some q2: linkPositions[s, d] | q2.ord = minus[q.ord, 1]
}

-- Consequence: minimum ordinal is 1 when link positions exist
assert ContiguityImpliesMinOne {
  all s: State | LinkContiguity[s] implies
    all d: s.docs |
      some linkPositions[s, d] implies
        some q: linkPositions[s, d] | q.ord = 1
}

-- Non-vacuity: a state with multiple link positions satisfying contiguity
run NonVacuity {
  some s: State, d: s.docs |
    #linkPositions[s, d] > 1 and LinkContiguity[s]
} for 5 but exactly 1 State, 4 Int

check ContiguityImpliesNoGaps for 5 but exactly 1 State, 4 Int
check ContiguityImpliesMinOne for 5 but exactly 1 State, 4 Int
