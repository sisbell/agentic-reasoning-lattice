-- ASN-0030  A4a pre — RearrangePre
-- Precondition for REARRANGE(d, cuts): d in Sigma.D

sig Addr {}

sig Document {}

sig Sigma {
  D : set Document,
  content : Document -> set Addr
} {
  -- content is defined only for documents in D
  content in D -> Addr
}

-- Precondition: d must be a document in the state
pred RearrangePre[s: Sigma, d: Document] {
  d in s.D
}

-- Rearrange with precondition
pred Rearrange[s, sPost: Sigma, d: Document] {
  RearrangePre[s, d]

  -- document set unchanged
  sPost.D = s.D

  -- d's addresses preserved as a set (rearrangement reorders, not adds/removes)
  sPost.content[d] = s.content[d]

  -- frame: other documents unchanged
  all d2: s.D - d | sPost.content[d2] = s.content[d2]
}

-- Rearrange WITHOUT precondition (for comparison)
pred RearrangeNoPre[s, sPost: Sigma, d: Document] {
  sPost.D = s.D
  sPost.content[d] = s.content[d]
  all d2: s.D - d | sPost.content[d2] = s.content[d2]
}

-- With precondition, d is always in D
assert PreGuaranteesDocMembership {
  all s, sPost: Sigma, d: Document |
    Rearrange[s, sPost, d] implies d in s.D
}

-- Without precondition, d might not be in D (expect counterexample)
assert NoPre_DocMayNotBeInD {
  all s, sPost: Sigma, d: Document |
    RearrangeNoPre[s, sPost, d] implies d in s.D
}

-- Non-vacuity: a valid Rearrange exists
run FindRearrange {
  some s, sPost: Sigma, d: Document |
    Rearrange[s, sPost, d] and some s.content[d]
} for 4 but exactly 2 Sigma

check PreGuaranteesDocMembership for 5 but exactly 2 Sigma
check NoPre_DocMayNotBeInD for 5 but exactly 2 Sigma
