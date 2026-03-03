-- T11: DualSpaceSeparation
--
-- The two-space design (I-space / V-space) is strictly enforced:
-- editing operations (INSERT/DELETE) shift only V-space positions;
-- permanence (as in T8/T9/T10) applies only to I-space positions.
-- No editing operation shifts an I-space address.
-- No V-space position can be claimed as permanent.

sig Pos {}

-- Document state: I-space and V-space position sets
sig State {
  ipos: set Pos,
  vpos: set Pos
}

-- A state is valid iff its two spaces are disjoint
pred validState[s: State] {
  no (s.ipos & s.vpos)
}

-- Editing operation kinds
abstract sig EditKind {}
one sig INSERT, DELETE extends EditKind {}

-- An editing operation: maps pre-state to post-state; shifts a set of positions
sig EditOp {
  kind: one EditKind,
  pre:  one State,
  post: one State,
  shifted: set Pos
}

-- A permanence claim: asserts that a position is permanent in a given state
sig PermClaim {
  pos: one Pos,
  at:  one State
}

-- T11a: an editing op is admissible only if it shifts V-space positions
--       and leaves I-space unchanged
pred admissibleEdit[op: EditOp] {
  op.shifted in op.pre.vpos         -- shifts confined to V-space
  op.post.ipos = op.pre.ipos        -- I-space invariant across the edit
  no (op.post.ipos & op.post.vpos)  -- disjointness maintained in post-state
}

-- T11b: a permanence claim is admissible only for I-space positions
pred admissiblePerm[pc: PermClaim] {
  pc.pos in pc.at.ipos
}

-- C1: admissible edits never shift an I-space address
assert NoISpaceShift {
  all op: EditOp |
    (validState[op.pre] and admissibleEdit[op]) implies
    no (op.shifted & op.pre.ipos)
}

-- C2: admissible permanence claims never cover a V-space position
assert NoVSpacePermanence {
  all pc: PermClaim |
    (validState[pc.at] and admissiblePerm[pc]) implies
    pc.pos not in pc.at.vpos
}

-- C3: a position cannot simultaneously be shifted (V-space) and permanent (I-space)
assert ShiftAndPermMutuallyExclusive {
  all op: EditOp, pc: PermClaim |
    (validState[op.pre] and
     pc.at = op.pre and
     admissibleEdit[op] and
     admissiblePerm[pc]) implies
    pc.pos not in op.shifted
}

-- C4: I-space is stable across any sequence of two admissible edits
assert ISpaceStableUnderChain {
  all op1, op2: EditOp |
    (validState[op1.pre] and
     op2.pre = op1.post and
     admissibleEdit[op1] and admissibleEdit[op2]) implies
    op2.post.ipos = op1.pre.ipos
}

-- Non-vacuity: a valid system with both I-space and V-space, and actual shifting
run NonVacuous {
  some op: EditOp |
    validState[op.pre] and
    admissibleEdit[op] and
    some op.pre.ipos and
    some op.pre.vpos and
    some op.shifted
} for 5 but exactly 2 State

check NoISpaceShift              for 5 but exactly 2 State
check NoVSpacePermanence         for 5 but exactly 2 State
check ShiftAndPermMutuallyExclusive for 5 but exactly 2 State
check ISpaceStableUnderChain     for 5 but exactly 3 State
