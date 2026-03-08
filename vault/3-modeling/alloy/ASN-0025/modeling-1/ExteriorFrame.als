-- ExteriorFrame
-- REARRANGE cut positions c1 < c2 < ... < ck (k in {3,4}) are text-subspace positions.
-- Text positions outside [c1, ck) are unchanged:
-- (A q : q in dom(S.v(d)) and q is text and (q < c1 or q >= ck) : S'.v(d)(q) = S.v(d)(q))

sig IAddr {}

-- Text positions with ordinals for ordering
sig TextPos {
  ord: Int
} {
  ord > 0
}

fact UniqueOrdinals {
  all disj p, q: TextPos | p.ord != q.ord
}

sig State {
  v: TextPos -> lone IAddr
}

-- A position is exterior to the cut range: before c1 or at/after ck
pred exterior[q: TextPos, cuts: set TextPos] {
  (all c: cuts | q.ord < c.ord)
  or
  (all c: cuts | q.ord >= c.ord)
}

-- REARRANGE with exterior frame postcondition
pred Rearrange[s, sPost: State, cuts: set TextPos] {
  -- k in {3, 4}
  #cuts >= 3
  #cuts =< 4

  -- cut positions are in the domain
  all c: cuts | some s.v[c]

  -- Exterior frame
  all q: TextPos |
    ((some s.v[q]) and exterior[q, cuts])
    implies
    (sPost.v[q] = s.v[q])
}

-- Assert: exterior frame preserves individual position mappings
assert ExteriorFramePreserved {
  all s, sPost: State, cuts: set TextPos, q: TextPos |
    (Rearrange[s, sPost, cuts] and (some s.v[q]) and exterior[q, cuts])
    implies
    (sPost.v[q] = s.v[q])
}

-- Assert: address set reachable from exterior positions is unchanged
assert ExteriorAddressSetPreserved {
  all s, sPost: State, cuts: set TextPos |
    Rearrange[s, sPost, cuts]
    implies
    (let ext = {q: TextPos | (some s.v[q]) and exterior[q, cuts]} |
      ext.(s.v) = ext.(sPost.v))
}

-- Assert (negative): without frame, exterior can change — expect counterexample
assert UncheckedExteriorPreserved {
  all s, sPost: State, cuts: set TextPos, q: TextPos |
    ((#cuts >= 3) and (#cuts =< 4) and (some s.v[q]) and exterior[q, cuts])
    implies
    (sPost.v[q] = s.v[q])
}

-- Non-vacuity: a rearrangement where interior positions change
run FindRearrange {
  some s, sPost: State, cuts: set TextPos |
    Rearrange[s, sPost, cuts] and s.v != sPost.v
} for 5 but exactly 2 State, 5 Int

check ExteriorFramePreserved for 5 but exactly 2 State, 5 Int
check ExteriorAddressSetPreserved for 5 but exactly 2 State, 5 Int
check UncheckedExteriorPreserved for 5 but exactly 2 State, 5 Int
