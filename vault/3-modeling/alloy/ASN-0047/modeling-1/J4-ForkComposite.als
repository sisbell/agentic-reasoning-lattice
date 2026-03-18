-- J4-ForkComposite.als
-- Fork of d_src to d_new decomposes into K.delta ; K.mu+ ; K.rho.
-- Postconditions: (1) dom(C') = dom(C),  (2) all addresses in
-- ran(M'(d_new)) have provenance recorded as (a, d_new) in R'.

sig Addr {}
sig Doc {}
sig VPos {}

sig State {
  content: set Addr,
  entities: set Doc,
  arr: Doc -> VPos -> lone Addr,
  prov: Addr -> set Doc
}

pred WF[s: State] {
  all d: Doc | some s.arr[d] implies d in s.entities
}

fun ranM[s: State, d: Doc]: set Addr { VPos.(s.arr[d]) }

----------------------------------------------------------------------
-- Elementary transitions
----------------------------------------------------------------------

-- K.delta: create new document entity (empty arrangement)
pred KDelta[s, sPost: State, d: Doc] {
  d not in s.entities
  sPost.entities = s.entities + d
  no sPost.arr[d]
  all d2: Doc - d | sPost.arr[d2] = s.arr[d2]
  sPost.content = s.content
  sPost.prov = s.prov
}

-- K.mu+ (fork variant): populate d_new's arrangement from d_src
pred KMuPlusFork[s, sPost: State, dnew: Doc, dsrc: Doc] {
  dnew in s.entities
  -- ran(M'(d_new)) subset of ran(M(d_src))
  ranM[sPost, dnew] in ranM[s, dsrc]
  some ranM[sPost, dnew]
  -- frame
  all d2: Doc - dnew | sPost.arr[d2] = s.arr[d2]
  sPost.entities = s.entities
  sPost.content = s.content
  sPost.prov = s.prov
}

-- K.rho (bulk): record provenance for every address in d's arrangement
pred KRhoBulk[s, sPost: State, d: Doc] {
  d in s.entities
  all a: ranM[s, d] | (a -> d) in sPost.prov
  s.prov in sPost.prov
  -- tight frame: only (a, d) entries added
  all a2: Addr, d2: Doc |
    (a2 -> d2) in sPost.prov implies
      ((a2 -> d2) in s.prov or (a2 in ranM[s, d] and d2 = d))
  -- frame: everything else unchanged
  sPost.entities = s.entities
  all d2: Doc | sPost.arr[d2] = s.arr[d2]
  sPost.content = s.content
}

----------------------------------------------------------------------
-- Fork composite: K.delta ; K.mu+ ; K.rho  and no other steps
----------------------------------------------------------------------

pred Fork[s0, s3: State, dsrc: Doc, dnew: Doc] {
  -- Precondition: d_src exists with nonempty arrangement
  dsrc in s0.entities
  some ranM[s0, dsrc]
  dnew not in s0.entities
  dsrc != dnew

  -- Three-step composition through intermediate states
  some disj s1, s2: State - s0 - s3 {
    KDelta[s0, s1, dnew]
    KMuPlusFork[s1, s2, dnew, dsrc]
    KRhoBulk[s2, s3, dnew]
  }
}

----------------------------------------------------------------------
-- J4 assertions
----------------------------------------------------------------------

-- dom(C') = dom(C): none of K.delta, K.mu+, K.rho modify content
assert ForkPreservesContent {
  all s0, s3: State, dsrc, dnew: Doc |
    Fork[s0, s3, dsrc, dnew] implies s3.content = s0.content
}

-- Every address in ran(M'(d_new)) has provenance (a, d_new) in R'
assert ForkRecordsProvenance {
  all s0, s3: State, dsrc, dnew: Doc |
    Fork[s0, s3, dsrc, dnew] implies
      (all a: ranM[s3, dnew] | (a -> dnew) in s3.prov)
}

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

run ForkExists {
  some s0, s3: State, dsrc, dnew: Doc |
    WF[s0] and Fork[s0, s3, dsrc, dnew]
} for 5 but exactly 4 State

check ForkPreservesContent for 5 but exactly 4 State
check ForkRecordsProvenance for 5 but exactly 4 State
