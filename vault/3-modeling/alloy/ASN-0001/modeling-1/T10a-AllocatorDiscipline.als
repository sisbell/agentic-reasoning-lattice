-- T10a: AllocatorDiscipline
-- Each allocator produces siblings exclusively via inc(·,0) — shallow increment
-- at the last significant position.  To spawn a child, the parent performs
-- exactly one inc(·,k') with k'>0, then delegates to the child; afterwards
-- the parent resumes with inc(·,0) sibling steps.
--
-- Modeled as a state-machine over allocator operation sequences:
--   Sib   — a sibling step  (inc at depth 0)
--   Spawn — a child-spawn   (inc at depth k' > 0)
-- The two-state invariant: after any Spawn, the very next operation (if present)
-- must be Sib.  Equivalently, no two consecutive Spawn steps are permitted.

-- ── Operation alphabet ───────────────────────────────────────────────────────

abstract sig AllocOp {}

one sig Sib extends AllocOp {}     -- sibling step: inc(·, 0)

sig Spawn extends AllocOp {        -- child-spawn: inc(·, k') with k' > 0
  spawnDepth: Int
} {
  spawnDepth > 0
}

-- ── Allocator state chain ─────────────────────────────────────────────────────

sig AllocState {
  op:   one AllocOp,      -- operation that produced this state
  succ: lone AllocState   -- immediate successor in this allocator's sequence
}

-- The successor relation is acyclic (finite sequences only)
fact Acyclic {
  no s: AllocState | s in s.^succ
}

-- ── Core two-state predicate ──────────────────────────────────────────────────

-- AllocatorDiscipline[s, s2]: s2 is a valid next step after s.
-- If s was produced by a Spawn, s2 must be Sib.
pred AllocatorDiscipline[s, s2: AllocState] {
  s.succ = s2
  (s.op in Spawn) implies (s2.op in Sib)
}

-- A chain rooted at s is disciplined iff every consecutive pair satisfies
-- AllocatorDiscipline.
pred DisciplinedChain[s: AllocState] {
  all t: s.*succ |
    some t.succ implies AllocatorDiscipline[t, t.succ]
}

-- ── Assertions ────────────────────────────────────────────────────────────────

-- [1] NoConsecutiveSpawns
-- In any disciplined chain, a Spawn is never directly followed by another Spawn.
assert NoConsecutiveSpawns {
  all s: AllocState | DisciplinedChain[s] implies
    all t: s.*succ |
      (t.op in Spawn and some t.succ) implies not (t.succ.op in Spawn)
}

-- [2] AllSpawnChainViolates
-- A chain of length >= 2 where every operation is a Spawn cannot be disciplined.
-- (Consequence: the only all-Spawn chain that passes is the length-1 chain.)
assert AllSpawnChainViolates {
  no s: AllocState |
    DisciplinedChain[s] and
    some s.succ and
    (all t: s.*succ | t.op in Spawn)
}

-- [3] SibAfterSpawn
-- In a disciplined chain, every Spawn that has a successor is followed by Sib.
assert SibAfterSpawn {
  all s: AllocState | DisciplinedChain[s] implies
    all t: s.*succ |
      (t.op in Spawn and some t.succ) implies (t.succ.op = Sib)
}

-- ── Non-vacuity run ───────────────────────────────────────────────────────────

-- Confirm the model is satisfiable: find a disciplined chain that includes
-- at least one Spawn step followed by a Sib step.
run NonVacuous {
  some s: AllocState |
    DisciplinedChain[s] and
    some t: s.*succ |
      t.op in Spawn and
      some t.succ and
      t.succ.op = Sib
} for 5 but exactly 3 AllocState, 2 Spawn, 4 Int

-- ── Checks ────────────────────────────────────────────────────────────────────

check NoConsecutiveSpawns    for 5 but exactly 4 AllocState, 2 Spawn, 4 Int
check AllSpawnChainViolates  for 5 but exactly 4 AllocState, 2 Spawn, 4 Int
check SibAfterSpawn          for 5 but exactly 4 AllocState, 2 Spawn, 4 Int
