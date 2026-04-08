sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact WellFormed {
  all t: Tumbler {
    t.len >= 1
    t.len =< 6
    all pos: Int {
      (pos >= 1 and pos =< t.len) implies one t.comp[pos]
      (pos < 1 or pos > t.len) implies no t.comp[pos]
    }
    all pos: Int | some t.comp[pos] implies t.comp[pos] >= 0
  }
}

-- No T3 canonical representation: allow content-equal atoms
-- so IntrinsicComparison is non-trivially checkable

-- Minimum of two integers
fun min2[a, b: Int]: Int {
  a =< b implies a else b
}

-- Divergence position: first i in 1..min(#a,#b) where components differ
-- Returns 0 if all shared positions agree
fun divPos[a, b: Tumbler]: Int {
  let bound = min2[a.len, b.len] |
    let diffs = { i: Int | i >= 1 and i =< bound and
                  not (a.comp[i] = b.comp[i]) } |
      (some diffs implies min[diffs] else 0)
}

-- T1 ordering: a < b (lexicographic with prefix rule)
pred ltT[a, b: Tumbler] {
  let d = divPos[a, b] {
    (d >= 1 and a.comp[d] < b.comp[d])
    or
    (d = 0 and a.len < b.len)
  }
}

-- Content equality: same length and same components at every position
pred contentEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | i >= 1 and i =< a.len implies a.comp[i] = b.comp[i]
}

-- Number of component pairs examined by the comparison scan
fun pairsExamined[a, b: Tumbler]: Int {
  let d = divPos[a, b] |
    d >= 1 implies d else min2[a.len, b.len]
}

-- Postcondition (a): ordering is determined — trichotomy over content
assert OrderingDetermined {
  all a, b: Tumbler |
    (ltT[a, b] and not ltT[b, a] and not contentEq[a, b])
    or (ltT[b, a] and not ltT[a, b] and not contentEq[a, b])
    or (contentEq[a, b] and not ltT[a, b] and not ltT[b, a])
}

-- Postcondition (b): at most min(#a, #b) component pairs examined
assert BoundedExamination {
  all a, b: Tumbler |
    pairsExamined[a, b] =< min2[a.len, b.len]
}

-- Postcondition (c): comparison is intrinsic — pure function of content
-- Content-equal tumblers yield identical comparison results
assert IntrinsicComparison {
  all a1, a2, b1, b2: Tumbler |
    (contentEq[a1, a2] and contentEq[b1, b2]) implies
      (ltT[a1, b1] iff ltT[a2, b2])
}

-- Non-vacuity: find two tumblers where one is strictly less
run NonVacuity {
  some a, b: Tumbler | ltT[a, b]
} for 3 but exactly 2 Tumbler, 4 Int

check OrderingDetermined for 4 but 4 Int
check BoundedExamination for 4 but 4 Int
check IntrinsicComparison for 4 but 4 Int
