-- A1-ISpaceFrame: I-space frame conditions for primitive operations
-- Each operation specifies exactly how I-space (identity space) transitions.

sig Address {}
sig Char {}

sig State {
  ispace: Address -> lone Char
}

-- Domain of I-space: addresses that map to some character
fun idom[s: State]: set Address {
  (s.ispace).Char
}

-- INSERT: extend I-space with fresh address-char pairs
pred Insert[s, sPost: State, fresh: set Address] {
  some fresh
  no fresh & idom[s]
  idom[sPost] = idom[s] + fresh
  all a: idom[s] | sPost.ispace[a] = s.ispace[a]
  all a: fresh | one sPost.ispace[a]
}

-- DELETE: I-space unchanged
pred Delete[s, sPost: State] {
  sPost.ispace = s.ispace
}

-- REARRANGE: I-space unchanged
pred Rearrange[s, sPost: State] {
  sPost.ispace = s.ispace
}

-- COPY: I-space unchanged
pred Copy[s, sPost: State] {
  sPost.ispace = s.ispace
}

-- CREATENEWVERSION: I-space unchanged
pred CreateNewVersion[s, sPost: State] {
  sPost.ispace = s.ispace
}

-- INSERT preserves all existing I-space entries
assert InsertPreservesOld {
  all s, sPost: State, fresh: set Address |
    Insert[s, sPost, fresh] implies s.ispace in sPost.ispace
}

-- INSERT strictly grows I-space
assert InsertStrictlyGrows {
  all s, sPost: State, fresh: set Address |
    Insert[s, sPost, fresh] implies not (s.ispace = sPost.ispace)
}

-- Non-INSERT operations preserve I-space exactly
assert NonInsertPreservesISpace {
  all s, sPost: State |
    (Delete[s, sPost] or Rearrange[s, sPost] or
     Copy[s, sPost] or CreateNewVersion[s, sPost])
      implies sPost.ispace = s.ispace
}

-- Non-vacuity: INSERT can fire from a non-empty state
run FindInsert {
  some s, sPost: State, fresh: set Address |
    Insert[s, sPost, fresh] and some idom[s]
} for 5 but exactly 2 State

check InsertPreservesOld for 5 but exactly 2 State
check InsertStrictlyGrows for 5 but exactly 2 State
check NonInsertPreservesISpace for 5 but exactly 2 State
