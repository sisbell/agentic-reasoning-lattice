-- RearrangeLength.als
-- Property A3.length: Rearrange preserves document length
-- |Σ'.V(d)| = n_d

sig Addr {}

sig Doc {
  slots: seq Addr
}

sig State {
  docs: set Doc
}

fun nd[d: Doc]: Int {
  #(d.slots)
}

-- sigma is a bijection on {0, ..., n-1} (0-indexed positions)
pred bijection[sigma: Int -> Int, n: Int] {
  let P = {i: Int | i >= 0 and i < n} | {
    all i: P | one i.sigma and i.sigma in P
    all i: Int - P | no i.sigma
    all disj i, j: P | i.sigma != j.sigma
  }
}

pred Rearrange[s: State, d: Doc, dPost: Doc, sigma: Int -> Int] {
  d in s.docs
  bijection[sigma, nd[d]]
  -- post content: dPost.slots[sigma(j)] = d.slots[j]
  all j: Int | j >= 0 and j < nd[d] implies
    dPost.slots[j.sigma] = d.slots[j]
  -- frame: no slots outside the permuted range
  all i: Int | some dPost.slots[i] implies (i >= 0 and i < nd[d])
}

assert RearrangeLength {
  all s: State, d, dPost: Doc, sigma: Int -> Int |
    Rearrange[s, d, dPost, sigma] implies nd[dPost] = nd[d]
}

-- Non-vacuity: find a valid rearrange on a non-empty document
run FindRearrange {
  some s: State, d, dPost: Doc, sigma: Int -> Int |
    Rearrange[s, d, dPost, sigma] and some d.slots
} for 4 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int

check RearrangeLength for 5 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int
