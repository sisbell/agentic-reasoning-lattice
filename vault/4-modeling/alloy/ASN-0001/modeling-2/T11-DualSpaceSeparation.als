-- T11 — DualSpaceSeparation
--
-- Editing shifts (via ⊕/⊖ applied by INSERT/DELETE) target V-space
-- exclusively.  Permanence guarantees (T8/T9/T10) target I-space
-- exclusively.  No editing operation shifts an I-space address; no
-- operation claims permanence for a V-space position.

abstract sig Space {}
one sig ISpace, VSpace extends Space {}

sig Tumbler {
  space: one Space
}

sig State {
  live: set Tumbler
}

-- An editing operation (INSERT or DELETE) that shifts positions via add/sub
sig EditOp {
  pre, post: one State,
  shifted: set Tumbler
}

-- A permanence guarantee: tumbler identity preserved across a transition
sig PermanenceClaim {
  holder: one Tumbler,
  from, to: one State
}

-- == Well-formedness ==

-- Shifted tumblers must be live in the pre-state
fact ShiftedAreLive {
  all op: EditOp | op.shifted in op.pre.live
}

-- Permanence holder is live in both states of the claim
fact PermanenceHolderLive {
  all pc: PermanenceClaim |
    pc.holder in pc.from.live and pc.holder in pc.to.live
}

-- Editing preserves all unshifted live tumblers
fact EditPreservesUnshifted {
  all op: EditOp |
    (op.pre.live - op.shifted) in op.post.live
}

-- == T11: Dual Space Separation ==

-- (a) Editing shifts apply exclusively to V-space
fact EditShiftsVSpaceOnly {
  all op: EditOp | all t: op.shifted | t.space = VSpace
}

-- (b) Permanence claims apply exclusively to I-space
fact PermanenceISpaceOnly {
  all pc: PermanenceClaim | pc.holder.space = ISpace
}

-- == Derived Properties ==

-- I-space tumblers live before an edit remain live after.
-- Follows from T11a (I-space never shifted) + EditPreservesUnshifted.
assert ISpaceStableUnderEdit {
  all op: EditOp, t: op.pre.live |
    t.space = ISpace implies t in op.post.live
}

-- No tumbler is both subject to editing shifts and permanence claims.
-- Follows from T11a (shifted in VSpace) + T11b (holders in ISpace).
assert ShiftedAndPermanentDisjoint {
  no t: Tumbler |
    (some op: EditOp | t in op.shifted) and
    (some pc: PermanenceClaim | t = pc.holder)
}

-- == Non-vacuity ==
-- Both spaces populated, an edit that shifts something, a permanence claim.
run NonVacuity {
  some t: Tumbler | t.space = ISpace
  some t: Tumbler | t.space = VSpace
  some op: EditOp | some op.shifted
  some PermanenceClaim
} for 5 but exactly 2 State

check ISpaceStableUnderEdit for 5 but exactly 2 State
check ShiftedAndPermanentDisjoint for 5 but exactly 2 State
