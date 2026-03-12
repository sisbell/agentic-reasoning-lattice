-- D10a — PublishOperation (POST, ensures)
--
--   pre:  d in Sigma.D, account(d) = actor(op),
--         Sigma.pub(d) = private, status in {published, privashed}
--   post: Sigma'.pub(d) = status
--   frame: Sigma'.D = Sigma.D, Sigma'.I = Sigma.I, Sigma'.V(d) = Sigma.V(d),
--          (A d' : d' in Sigma.D, d' != d :
--              Sigma'.V(d') = Sigma.V(d') and Sigma'.pub(d') = Sigma.pub(d'))

sig AccountAddr {}

sig Doc {
  account: one AccountAddr
}

sig Element {}
sig Value {}
sig Link {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D: set Doc,
  I: set Link,
  V: Doc -> Element -> lone Value,
  pub: Doc -> lone PubStatus
} {
  -- pub defined exactly on D
  pub in D -> PubStatus
  all d: D | one pub[d]
  -- V scoped to D
  (V.Value).Element in D
}

----------------------------------------------------------------------
-- PublishOperation
----------------------------------------------------------------------

pred PublishOp[s, sPost: State, d: Doc, act: AccountAddr, status: PubStatus] {
  -- precondition
  d in s.D
  d.account = act
  s.pub[d] = Private
  status in Published + Privashed

  -- postcondition + frame
  sPost.D = s.D
  sPost.I = s.I
  sPost.V = s.V
  sPost.pub = s.pub ++ (d -> status)
}

----------------------------------------------------------------------
-- Assertions
----------------------------------------------------------------------

-- PublishOp preserves well-formedness (sig facts hold in post-state)
assert PublishPreservesWF {
  all s, sPost: State, d: Doc, act: AccountAddr, st: PubStatus |
    PublishOp[s, sPost, d, act, st] implies {
      sPost.pub in sPost.D -> PubStatus
      all d2: sPost.D | one sPost.pub[d2]
      (sPost.V.Value).Element in sPost.D
    }
}

-- Post: the target document gets the requested status
assert PublishSetsStatus {
  all s, sPost: State, d: Doc, act: AccountAddr, st: PubStatus |
    PublishOp[s, sPost, d, act, st] implies sPost.pub[d] = st
}

-- Frame: version maps are entirely unchanged
assert PublishPreservesVersions {
  all s, sPost: State, d: Doc, act: AccountAddr, st: PubStatus |
    PublishOp[s, sPost, d, act, st] implies
      (all d2: s.D | sPost.V[d2] = s.V[d2])
}

-- Frame: other documents' pub status is unchanged
assert PublishFrameOtherPub {
  all s, sPost: State, d: Doc, act: AccountAddr, st: PubStatus |
    PublishOp[s, sPost, d, act, st] implies
      (all d2: s.D - d | sPost.pub[d2] = s.pub[d2])
}

----------------------------------------------------------------------
-- Checks and non-vacuity
----------------------------------------------------------------------

check PublishPreservesWF for 5 but exactly 2 State
check PublishSetsStatus for 5 but exactly 2 State
check PublishPreservesVersions for 5 but exactly 2 State
check PublishFrameOtherPub for 5 but exactly 2 State

run FindPublishOp {
  some s, sPost: State, d: Doc, act: AccountAddr, st: PubStatus |
    PublishOp[s, sPost, d, act, st] and some s.D
} for 4 but exactly 2 State
