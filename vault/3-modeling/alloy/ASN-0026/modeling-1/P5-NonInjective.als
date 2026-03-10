-- P5-NonInjective.als
-- VSpaceMap is not required to be injective.
-- Self-transclusion (within a document) and cross-document transclusion
-- are both permitted.  Counterexamples on the checks below are the
-- expected outcome: each witnesses a non-injective configuration.

sig Addr {}
sig Doc {}
sig Pos {}

one sig S {
  docs : set Doc,
  vmap : Doc -> Pos -> lone Addr
} {
  -- vmap defined only for documents in docs
  all d : Doc, p : Pos | some vmap[d][p] implies d in docs
  -- every doc in docs has at least one mapped position
  all d : docs | some d.(vmap)
}

-- Self-transclusion: same doc, two distinct positions share an address
pred selfTransclusion {
  some d : S.docs, disj p1, p2 : Pos |
    some S.vmap[d][p1] and S.vmap[d][p1] = S.vmap[d][p2]
}

-- Cross-document transclusion: distinct docs share an address
pred crossTransclusion {
  some disj d1, d2 : S.docs, p1, p2 : Pos |
    some S.vmap[d1][p1] and S.vmap[d1][p1] = S.vmap[d2][p2]
}

-- Negated assertions — counterexample = existence witness
assert AlwaysInjectiveWithinDoc {
  not selfTransclusion
}

assert AlwaysInjectiveAcrossDocs {
  not crossTransclusion
}

-- Non-vacuity: a state with two docs each having a mapped position
run NonVacuity {
  #S.docs >= 2
  all d : S.docs | some p : Pos | some S.vmap[d][p]
} for 4

check AlwaysInjectiveWithinDoc for 5
check AlwaysInjectiveAcrossDocs for 5
