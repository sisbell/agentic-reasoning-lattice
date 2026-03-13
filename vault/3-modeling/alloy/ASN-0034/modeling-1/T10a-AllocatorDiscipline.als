-- T10a: AllocatorDiscipline
-- Sibling increment preserves lastSig; spawn increment deepens it.

sig Tumbler {
  c1: one Int,
  c2: one Int,
  c3: one Int
}

fact nonNeg {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
}

pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Last significant position: index of last nonzero component.
-- Zero tumbler returns #t = 3 by convention.
fun lastSig[t: Tumbler]: Int {
  t.c3 > 0 => 3
    else (t.c2 > 0 => 2
    else (t.c1 > 0 => 1
    else 3))
}

-- Sibling increment: inc(t, 0) — advance at lastSig(t).
-- Tail positions come from the unit displacement (zeros).
pred incSibling[t, r: Tumbler] {
  positive[t]
  let k = lastSig[t] {
    k = 1 => (
      r.c1 = plus[t.c1, 1] and r.c2 = 0 and r.c3 = 0
    ) else k = 2 => (
      r.c1 = t.c1 and r.c2 = plus[t.c2, 1] and r.c3 = 0
    ) else (
      r.c1 = t.c1 and r.c2 = t.c2 and r.c3 = plus[t.c3, 1]
    )
  }
}

-- Spawn increment: inc(t, offset) with offset > 0.
-- Action point at lastSig(t) + offset establishes a child prefix.
pred incSpawn[t, r: Tumbler, offset: Int] {
  positive[t]
  offset > 0
  let ap = plus[lastSig[t], offset] {
    ap > 0   -- positions are 1-indexed; guards against Int overflow
    ap =< 3
    ap = 2 => (
      r.c1 = t.c1 and r.c2 = plus[t.c2, 1] and r.c3 = 0
    ) else (
      r.c1 = t.c1 and r.c2 = t.c2 and r.c3 = plus[t.c3, 1]
    )
  }
}

-- Core discipline: sibling increment preserves operating level
assert SiblingPreservesLevel {
  all t, r: Tumbler |
    incSibling[t, r] implies lastSig[r] = lastSig[t]
}

-- Spawn increment establishes a strictly deeper level
assert SpawnDeepensLevel {
  all t, r: Tumbler, offset: Int |
    incSpawn[t, r, offset] implies lastSig[r] = plus[lastSig[t], offset]
}

-- Composition: after spawn, child sibling stays at child level
assert SpawnThenChildSibling {
  all disj t1, t2, t3: Tumbler, offset: Int |
    (incSpawn[t1, t2, offset] and incSibling[t2, t3]) implies
      lastSig[t3] = plus[lastSig[t1], offset]
}

-- Sibling increment preserves positivity
assert SiblingResultPositive {
  all t, r: Tumbler |
    incSibling[t, r] implies positive[r]
}

-- Non-vacuity: spawn then child sibling is satisfiable
run NonVacuity {
  some disj t1, t2, t3: Tumbler, offset: Int |
    incSpawn[t1, t2, offset] and incSibling[t2, t3]
} for 5 but exactly 3 Tumbler, 5 Int

check SiblingPreservesLevel for 5 but exactly 2 Tumbler, 5 Int
check SpawnDeepensLevel for 5 but exactly 2 Tumbler, 5 Int
check SpawnThenChildSibling for 6 but exactly 3 Tumbler, 5 Int
check SiblingResultPositive for 5 but exactly 2 Tumbler, 5 Int
