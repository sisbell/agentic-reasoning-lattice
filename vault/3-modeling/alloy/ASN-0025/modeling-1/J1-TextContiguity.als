-- J1-TextContiguity.als
-- TextContiguity: text-position ordinals in each document form {1, ..., n}

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

-- Text positions active in document d
fun textPositions[s: State, d: IAddr]: set VPos {
  {q: VPos | q.tag = TextTag and some s.vmap[d][q]}
}

-- J1: TextContiguity
-- n distinct positive integers all =< n must be exactly {1, ..., n}
-- (by pigeonhole, combined with VPosDistinct and ord > 0)
pred TextContiguity[s: State] {
  all d: s.docs |
    all q: textPositions[s, d] |
      q.ord =< #textPositions[s, d]
}

-- Consequence: no gaps in the ordinal sequence
assert ContiguityImpliesNoGaps {
  all s: State | TextContiguity[s] implies
    all d: s.docs, q: textPositions[s, d] |
      q.ord > 1 implies
        some q2: textPositions[s, d] | q2.ord = minus[q.ord, 1]
}

-- Consequence: minimum ordinal is 1 when text positions exist
assert ContiguityImpliesMinOne {
  all s: State | TextContiguity[s] implies
    all d: s.docs |
      some textPositions[s, d] implies
        some q: textPositions[s, d] | q.ord = 1
}

-- Non-vacuity: a state with multiple text positions satisfying contiguity
run NonVacuity {
  some s: State, d: s.docs |
    #textPositions[s, d] > 1 and TextContiguity[s]
} for 5 but exactly 1 State, 4 Int

check ContiguityImpliesNoGaps for 5 but exactly 1 State, 4 Int
check ContiguityImpliesMinOne for 5 but exactly 1 State, 4 Int
