-- T5-ContiguousSubtrees.als
-- For any tumbler prefix p, the set {t : p prefix-of t} forms
-- a contiguous interval under lexicographic order.

open util/integer

sig Tumbler {
  len: Int,
  v0: Int,
  v1: Int,
  v2: Int,
  v3: Int
}

fact wellFormed {
  all t: Tumbler {
    t.len >= 1
    t.len =< 4
    t.v0 >= 0
    t.v1 >= 0
    t.v2 >= 0
    t.v3 >= 0
    t.len < 2 implies t.v1 = 0
    t.len < 3 implies t.v2 = 0
    t.len < 4 implies t.v3 = 0
  }
}

-- p is a prefix of t: first #p components of t match p
pred isPrefix[p: Tumbler, t: Tumbler] {
  p.len =< t.len
  p.v0 = t.v0
  p.len >= 2 implies p.v1 = t.v1
  p.len >= 3 implies p.v2 = t.v2
  p.len >= 4 implies p.v3 = t.v3
}

-- Lexicographic less-than-or-equal with implicit zero-padding
pred lexLTE[a: Tumbler, b: Tumbler] {
  a.v0 < b.v0
  or (a.v0 = b.v0 and a.v1 < b.v1)
  or (a.v0 = b.v0 and a.v1 = b.v1 and a.v2 < b.v2)
  or (a.v0 = b.v0 and a.v1 = b.v1 and a.v2 = b.v2 and a.v3 =< b.v3)
}

-- T5: Contiguous Subtrees
-- p prefix-of a, p prefix-of c, a <= b <= c  =>  p prefix-of b
assert ContiguousSubtrees {
  all p, a, b, c: Tumbler |
    (isPrefix[p, a] and isPrefix[p, c] and lexLTE[a, b] and lexLTE[b, c])
    implies isPrefix[p, b]
}

-- Non-vacuity: find a strict a < b < c all extending prefix p
run NonVacuity {
  some disj p, a, b, c: Tumbler |
    isPrefix[p, a] and isPrefix[p, c] and
    lexLTE[a, b] and not lexLTE[b, a] and
    lexLTE[b, c] and not lexLTE[c, b]
} for 5 but 5 Int

check ContiguousSubtrees for 5 but 5 Int
