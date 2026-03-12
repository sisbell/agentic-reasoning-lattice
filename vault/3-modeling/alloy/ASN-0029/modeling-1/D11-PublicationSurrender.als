-- D11 — PublicationSurrender (INV, predicate(State, DocId))
--
--   Σ.pub(d) = published ⟹
--     (a) any session may read d
--     (b) any session may create links into d (incoming links)
--     (c) any session may transclude from d (quotation)
--     (d) withdrawal requires extraordinary process
--
-- Access predicates are unconstrained; counterexamples demonstrate
-- each access right must be independently enforced for published docs.
-- D11(d) is checked via ordinary-step monotonicity (should hold).

sig Doc {}
sig Session {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D: set Doc,
  pub: Doc -> lone PubStatus,
  canRead: Session -> Doc,
  canLinkInto: Session -> Doc,
  canTransclude: Session -> Doc
} {
  pub in D -> PubStatus
  all d: D | one pub[d]
  canRead in Session -> D
  canLinkInto in Session -> D
  canTransclude in Session -> D
}

----------------------------------------------------------------------
-- D11(a): published ⟹ any session may read
----------------------------------------------------------------------

assert D11a_PublishedUniversalRead {
  all s: State, d: s.D, sess: Session |
    s.pub[d] = Published implies d in sess.(s.canRead)
}

----------------------------------------------------------------------
-- D11(b): published ⟹ any session may create incoming links
----------------------------------------------------------------------

assert D11b_PublishedUniversalLinkInto {
  all s: State, d: s.D, sess: Session |
    s.pub[d] = Published implies d in sess.(s.canLinkInto)
}

----------------------------------------------------------------------
-- D11(c): published ⟹ any session may transclude
----------------------------------------------------------------------

assert D11c_PublishedUniversalTransclude {
  all s: State, d: s.D, sess: Session |
    s.pub[d] = Published implies d in sess.(s.canTransclude)
}

----------------------------------------------------------------------
-- D11(d): withdrawal requires extraordinary process
----------------------------------------------------------------------

-- Ordinary operations (from D10): create, set-pub, skip

pred CreateDoc[s, s2: State, d: Doc] {
  d not in s.D
  s2.D = s.D + d
  s2.pub[d] = Private
  all d2: s.D | s2.pub[d2] = s.pub[d2]
}

pred SetPub[s, s2: State, d: Doc, target: PubStatus] {
  d in s.D
  s.pub[d] = Private
  target in Published + Privashed
  s2.D = s.D
  s2.pub[d] = target
  all d2: s.D - d | s2.pub[d2] = s.pub[d2]
}

pred Skip[s, s2: State] {
  s2.D = s.D
  s2.pub = s.pub
}

pred OrdinaryStep[s, s2: State] {
  (some d: Doc | CreateDoc[s, s2, d])
  or (some d: Doc, t: PubStatus | SetPub[s, s2, d, t])
  or Skip[s, s2]
}

-- Ordinary steps cannot withdraw publication (Published → non-Published)
assert D11d_OrdinaryCannotWithdraw {
  all s, s2: State, d: Doc |
    (OrdinaryStep[s, s2] and d in s.D and s.pub[d] = Published)
      implies s2.pub[d] = Published
}

----------------------------------------------------------------------
-- Checks (counterexamples expected for a, b, c; d should hold)
----------------------------------------------------------------------

check D11a_PublishedUniversalRead for 5 but exactly 1 State
check D11b_PublishedUniversalLinkInto for 5 but exactly 1 State
check D11c_PublishedUniversalTransclude for 5 but exactly 1 State
check D11d_OrdinaryCannotWithdraw for 5 but exactly 2 State

----------------------------------------------------------------------
-- Non-vacuity: published doc with universal access and sessions
----------------------------------------------------------------------

run NonVacuity {
  some s: State, d: s.D |
    s.pub[d] = Published and
    #Session > 1 and
    (all sess: Session | d in sess.(s.canRead)) and
    (all sess: Session | d in sess.(s.canLinkInto)) and
    (all sess: Session | d in sess.(s.canTransclude))
} for 4 but exactly 1 State
