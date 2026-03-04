open util/ordering[Step]

-- Allocation time steps
sig Step {}

-- Tumbler: fixed-length sequence of 3 natural-number components
sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
}

-- Model natural numbers: all components non-negative
fact NonNegative {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Action point: index of first positive component in displacement
fun actionPoint[w: Tumbler]: Int {
  (w.c1 > 0) => 1 else ((w.c2 > 0) => 2 else 3)
}

-- Last significant position: deepest positive component (minimum 1)
fun lastSig[t: Tumbler]: Int {
  (t.c3 > 0) => 3 else ((t.c2 > 0) => 2 else 1)
}

-- TumblerAdd: result = a ⊕ w
-- At action point k: copy a before k, add at k, copy w after k
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  let k = actionPoint[w] {
    k = 1 implies (
      result.c1 = plus[a.c1, w.c1] and
      result.c2 = w.c2 and
      result.c3 = w.c3)
    k = 2 implies (
      result.c1 = a.c1 and
      result.c2 = plus[a.c2, w.c2] and
      result.c3 = w.c3)
    k = 3 implies (
      result.c1 = a.c1 and
      result.c2 = a.c2 and
      result.c3 = plus[a.c3, w.c3])
  }
}

-- Lexicographic strict less-than on tumblers
pred tlt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- Unit displacement: exactly one component is 1, rest are 0
-- Models "inc" — a single-unit increment at one position
pred unitDisp[w: Tumbler] {
  (w.c1 = 1 and w.c2 = 0 and w.c3 = 0) or
  (w.c1 = 0 and w.c2 = 1 and w.c3 = 0) or
  (w.c1 = 0 and w.c2 = 0 and w.c3 = 1)
}

-- Allocator: advances position via TumblerAdd at each step
sig Allocator {
  pos: Step -> one Tumbler,
  disp: Step -> lone Tumbler
}

-- Allocator advances via unit-displacement TumblerAdd
fact AllocatorAdvances {
  all al: Allocator {
    no al.disp[last]
    all s: Step - last | {
      unitDisp[al.disp[s]]
      tumblerAdd[al.pos[s], al.disp[s], al.pos[s.next]]
    }
  }
}

-- Sibling step: action point = lastSig (increment at current depth)
pred siblingStep[al: Allocator, s: Step] {
  some al.disp[s]
  actionPoint[al.disp[s]] = lastSig[al.pos[s]]
}

-- Spawn step: action point > lastSig (increment deeper than current depth)
pred spawnStep[al: Allocator, s: Step] {
  some al.disp[s]
  actionPoint[al.disp[s]] > lastSig[al.pos[s]]
}

-- T10a: Allocator discipline — every step is sibling or spawn,
-- never an increment shallower than the current depth
fact AllocatorDiscipline {
  all al: Allocator, s: Step - last |
    siblingStep[al, s] or spawnStep[al, s]
}

-----------------------------------------------------------
-- Assertions
-----------------------------------------------------------

-- Sibling steps preserve the last significant position
assert SiblingPreservesDepth {
  all al: Allocator, s: Step - last |
    siblingStep[al, s] implies
      lastSig[al.pos[s.next]] = lastSig[al.pos[s]]
}

-- Spawn steps strictly increase the last significant position
assert SpawnIncreasesDepth {
  all al: Allocator, s: Step - last |
    spawnStep[al, s] implies
      lastSig[al.pos[s.next]] > lastSig[al.pos[s]]
}

-- Every disciplined step advances the address lexicographically
assert DisciplineImpliesForward {
  all al: Allocator, s: Step - last |
    tlt[al.pos[s], al.pos[s.next]]
}

-- Sibling and spawn are mutually exclusive
assert StepsExclusive {
  all al: Allocator, s: Step |
    not (siblingStep[al, s] and spawnStep[al, s])
}

-----------------------------------------------------------
-- Checks
-----------------------------------------------------------

check SiblingPreservesDepth for 6 but exactly 3 Step, exactly 1 Allocator, 5 Int
check SpawnIncreasesDepth for 6 but exactly 3 Step, exactly 1 Allocator, 5 Int
check DisciplineImpliesForward for 6 but exactly 3 Step, exactly 1 Allocator, 5 Int
check StepsExclusive for 6 but exactly 3 Step, exactly 1 Allocator, 5 Int

-----------------------------------------------------------
-- Non-vacuity: find a trace with both sibling and spawn steps
-----------------------------------------------------------

run FindMixedTrace {
  some al: Allocator, disj s1, s2: Step - last |
    siblingStep[al, s1] and spawnStep[al, s2]
} for 6 but exactly 3 Step, exactly 1 Allocator, 5 Int
