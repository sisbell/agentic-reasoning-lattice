-- T10a (AllocatorDiscipline): bounded check
-- Axiom: siblings by inc(·,0); child-spawn by inc(·,k') with k'>0.
-- Consequences: T10a.1 uniform length, T10a.2 non-nesting prefixes,
-- T10a.3 length separation (with additive nesting), T10a-N necessity.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
}

pred wellFormed[t: Tumbler] {
  all p: Int | (p >= 1 and p =< t.len) implies one t.comp[p]
  all p: Int | (p < 1 or p > t.len) implies no t.comp[p]
  all p: Int | some t.comp[p] implies t.comp[p] >= 1
}

fact AllWellFormed { all t: Tumbler | wellFormed[t] }

-- Proper prefix: a is strictly shorter with matching components
pred isProperPrefix[a, b: Tumbler] {
  a.len < b.len
  all p: Int | (p >= 1 and p =< a.len) implies a.comp[p] = b.comp[p]
}

-- Sibling allocation: inc(t, 0) — same length, same prefix, increment last
pred incSibling[t, r: Tumbler] {
  r.len = t.len
  all p: Int | (p >= 1 and p < t.len) implies r.comp[p] = t.comp[p]
  r.comp[t.len] = plus[t.comp[t.len], 1]
}

-- Child-spawning: inc(t, k) with k >= 1 — extends by k, preserves input prefix
pred incChild[t, r: Tumbler, k: Int] {
  k >= 1
  r.len = plus[t.len, k]
  all p: Int | (p >= 1 and p =< t.len) implies r.comp[p] = t.comp[p]
}

-- The allocator under test
one sig Alloc {
  base: one Tumbler,
  siblings: set Tumbler,
  childBase: lone Tumbler,
  spawnK: lone Int,
  spawner: lone Tumbler
}

-- Axiom: sibling outputs produced by iterated inc(·, 0) from base
fact SiblingsByShallowInc {
  all s: Alloc.siblings |
    incSibling[Alloc.base, s] or
    (some s2: Alloc.siblings - s | incSibling[s2, s])
}

-- Base is not a sibling output
fact BaseDistinct {
  Alloc.base not in Alloc.siblings
}

-- Axiom: child spawn by exactly one inc(·, k') with k' > 0
fact ChildSpawnAxiom {
  (some Alloc.childBase) iff (some Alloc.spawnK)
  (some Alloc.childBase) iff (some Alloc.spawner)
  some Alloc.childBase implies {
    Alloc.spawner in (Alloc.base + Alloc.siblings)
    incChild[Alloc.spawner, Alloc.childBase, Alloc.spawnK]
    Alloc.childBase not in Alloc.siblings
    Alloc.childBase != Alloc.base
  }
}

----------------------------------------------------------------------
-- T10a.1 (Uniform sibling length)
-- All sibling outputs have the same length as the base address.
----------------------------------------------------------------------
assert T10a_1_UniformLength {
  all t: Alloc.siblings | t.len = Alloc.base.len
}

----------------------------------------------------------------------
-- T10a.2 (Non-nesting sibling prefixes)
-- Distinct siblings are prefix-incomparable.
----------------------------------------------------------------------
assert T10a_2_NonNesting {
  all disj s1, s2: Alloc.siblings |
    not isProperPrefix[s1, s2] and not isProperPrefix[s2, s1]
}

----------------------------------------------------------------------
-- T10a.3 (Length separation — single level)
-- Child base length >= parent base length + spawn depth.
----------------------------------------------------------------------
assert T10a_3_LengthSep {
  some Alloc.childBase implies
    Alloc.childBase.len >= plus[Alloc.base.len, Alloc.spawnK]
}

----------------------------------------------------------------------
-- T10a.3 additive (Length separation — two nesting levels)
-- Deep increment chains produce additive length separation:
-- #c2 >= #b + k1 + k2.
----------------------------------------------------------------------
assert T10a_3_Additive {
  all b, c1, c2: Tumbler, k1, k2: Int |
    (incChild[b, c1, k1] and incChild[c1, c2, k2])
    implies c2.len >= plus[plus[b.len, k1], k2]
}

----------------------------------------------------------------------
-- T10a-N (Necessity)
-- Relaxing k=0 for siblings admits prefix nesting:
-- inc(·,0) then inc(·,1) produces a proper-prefix pair.
-- Expect COUNTEREXAMPLE: t1 IS a proper prefix of t2.
----------------------------------------------------------------------
assert T10a_N_Necessity {
  all t0, t1, t2: Tumbler |
    (incSibling[t0, t1] and incChild[t1, t2, 1])
    implies not isProperPrefix[t1, t2]
}

----------------------------------------------------------------------
-- Non-vacuity: allocator with siblings and a child spawn
----------------------------------------------------------------------
run NonVacuity {
  #Alloc.siblings >= 2
  some Alloc.childBase
} for 5 but 4 Int

check T10a_1_UniformLength for 5 but 4 Int
check T10a_2_NonNesting for 5 but 4 Int
check T10a_3_LengthSep for 5 but 4 Int
check T10a_3_Additive for 4 but 4 Int
check T10a_N_Necessity for 4 but exactly 3 Tumbler, 4 Int
