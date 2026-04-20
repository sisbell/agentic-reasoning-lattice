open util/integer

-- Tumblers: finite sequences of positive integers, length 1..4
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1
    t.len =< 4
    all i: Int {
      (i >= 1 and i =< t.len) implies (one t.comp[i] and t.comp[i] >= 1)
      (i < 1 or i > t.len) implies no t.comp[i]
    }
  }
}

-- No two distinct atoms encode the same tumbler value
fact DistinctTumblers {
  all disj a, b: Tumbler |
    a.len != b.len or
    (some i: Int | i >= 1 and i =< a.len and a.comp[i] != b.comp[i])
}

-- Prefix relation: p ≼ t
pred isPrefix[p, t: Tumbler] {
  p.len =< t.len
  all i: Int | (i >= 1 and i =< p.len) implies t.comp[i] = p.comp[i]
}

-- Strict lexicographic order (T1): a < b
-- Case (i): first divergence within common length, a smaller
-- Case (ii): a is a proper prefix of b
pred ltT1[a, b: Tumbler] {
  (some k: Int {
    k >= 1
    k =< a.len
    k =< b.len
    all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
    a.comp[k] < b.comp[k]
  })
  or
  (a.len < b.len and
   (all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]))
}

-- Lexicographic less-than-or-equal: a ≤ b
pred leqT1[a, b: Tumbler] {
  a = b or ltT1[a, b]
}

-- T5 (ContiguousSubtrees): prefixed subtrees are contiguous under T1
-- Preconditions: a,b,c ∈ T; p prefix with #p ≥ 1; p ≼ a; p ≼ c; a ≤ b ≤ c
-- Postcondition: p ≼ b
assert ContiguousSubtrees {
  all p, a, b, c: Tumbler |
    (p.len >= 1 and isPrefix[p, a] and isPrefix[p, c] and
     leqT1[a, b] and leqT1[b, c])
    implies isPrefix[p, b]
}

-- Non-vacuity: preconditions satisfiable with strictly ordered a < b < c
run NonVacuity {
  some disj a, b, c: Tumbler |
    some p: Tumbler |
      p.len >= 1 and
      isPrefix[p, a] and isPrefix[p, c] and
      ltT1[a, b] and ltT1[b, c]
} for 5 but 5 Int

check ContiguousSubtrees for 5 but 5 Int
