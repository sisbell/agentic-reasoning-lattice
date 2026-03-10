-- RearrangeISpacePreserved.als
-- Property A3.frame-I: Rearrange preserves the I-space
-- Σ'.I = Σ.I

sig Addr {}
sig Char {}

sig Doc {
  slots: seq Addr
}

sig State {
  ispace: Addr -> lone Char,
  docs: set Doc
}

fun nd[d: Doc]: Int {
  #(d.slots)
}

-- sigma is a bijection on {0, ..., n-1}
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

-- Full state transition: Rearrange one document, I-space unchanged
pred RearrangeOp[s, sPost: State, d: Doc, dPost: Doc, sigma: Int -> Int] {
  Rearrange[s, d, dPost, sigma]
  -- state transition: swap d for dPost in docs
  sPost.docs = (s.docs - d) + dPost
  -- frame: I-space preserved
  sPost.ispace = s.ispace
}

assert RearrangeISpacePreserved {
  all s, sPost: State, d, dPost: Doc, sigma: Int -> Int |
    RearrangeOp[s, sPost, d, dPost, sigma] implies sPost.ispace = s.ispace
}

-- Non-vacuity: find a rearrange on a non-empty document with non-empty I-space
run FindRearrange {
  some s, sPost: State, d, dPost: Doc, sigma: Int -> Int |
    RearrangeOp[s, sPost, d, dPost, sigma] and some d.slots and some s.ispace
} for 4 but exactly 2 State, exactly 2 Doc, 4 seq, 5 Int

check RearrangeISpacePreserved for 5 but exactly 2 State, exactly 2 Doc, 4 seq, 5 Int
