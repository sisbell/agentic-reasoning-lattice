-- TA5 — HierarchicalIncrement
-- Checks that inc(t, k) produces t' strictly greater than t under T1 ordering.
-- Sibling case (k=0): increment at lastSig(t), preserve length.
-- Child case (k>0): extend by k positions with k-1 zero separators and a final 1.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  all i: Int | (1 =< i and i =< len) implies one comp[i]
  all i: Int | (i < 1 or i > len) implies no comp[i]
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Last significant position (1-based):
-- max nonzero position, or len if all components are zero
fun lastSig[t: Tumbler]: Int {
  let nz = {i: Int | 1 =< i and i =< t.len and not (t.comp[i] = 0)} |
    (some nz) => max[nz] else t.len
}

-- T1 strict ordering on tumblers (lexicographic + prefix)
pred tLess[a: Tumbler, b: Tumbler] {
  -- Case (i): component divergence at first differing position
  (some k: Int |
    1 =< k and k =< a.len and k =< b.len and
    (all i: Int | (1 =< i and i < k) implies a.comp[i] = b.comp[i]) and
    a.comp[k] < b.comp[k])
  or
  -- Case (ii): a is a proper prefix of b
  (a.len < b.len and
    (all i: Int | (1 =< i and i =< a.len) implies a.comp[i] = b.comp[i]))
}

-- Sibling increment (k = 0): increment at lastSig(t), preserve length
pred incSibling[t: Tumbler, tPost: Tumbler] {
  let s = lastSig[t] {
    tPost.len = t.len
    all i: Int | (1 =< i and i < s) implies tPost.comp[i] = t.comp[i]
    tPost.comp[s] = plus[t.comp[s], 1]
    all i: Int | (s < i and i =< t.len) implies tPost.comp[i] = t.comp[i]
  }
}

-- Child increment (k > 0): extend by k, with k-1 zero separators and final 1
pred incChild[t: Tumbler, k: Int, tPost: Tumbler] {
  k >= 1
  tPost.len = plus[t.len, k]
  all i: Int | (1 =< i and i =< t.len) implies tPost.comp[i] = t.comp[i]
  all i: Int | (plus[t.len, 1] =< i and i < plus[t.len, k]) implies tPost.comp[i] = 0
  tPost.comp[plus[t.len, k]] = 1
}

-- TA5(a): sibling increment yields t' > t
assert TA5_SiblingStrict {
  all t, tPost: Tumbler |
    incSibling[t, tPost] implies tLess[t, tPost]
}

-- TA5(a): child increment yields t' > t
assert TA5_ChildStrict {
  all t, tPost: Tumbler, k: Int |
    (k >= 1 and incChild[t, k, tPost]) implies tLess[t, tPost]
}

-- Non-vacuity: find a valid sibling increment
run FindSibling {
  some disj t, tPost: Tumbler |
    incSibling[t, tPost]
} for 5 but exactly 2 Tumbler, 5 Int

-- Non-vacuity: find a valid child increment
run FindChild {
  some disj t, tPost: Tumbler, k: Int |
    k >= 1 and incChild[t, k, tPost]
} for 5 but exactly 2 Tumbler, 5 Int

check TA5_SiblingStrict for 5 but exactly 2 Tumbler, 5 Int
check TA5_ChildStrict for 5 but exactly 2 Tumbler, 5 Int
