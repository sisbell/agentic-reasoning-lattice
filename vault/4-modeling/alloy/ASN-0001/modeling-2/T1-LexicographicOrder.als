-- T1-LexicographicOrder
-- Lexicographic ordering on tumblers is a strict total order

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1
    t.len =< 3
    all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
    all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

pred LT[a, b: Tumbler] {
  some k: Int |
    k >= 1 and
    (all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]) and
    ((k =< a.len and k =< b.len and a.comp[k] < b.comp[k])
     or
     (k = plus[a.len, 1] and k =< b.len))
}

pred EQ[a, b: Tumbler] {
  a.len = b.len
  all i: Int | a.comp[i] = b.comp[i]
}

assert Irreflexive {
  all a: Tumbler | not LT[a, a]
}

assert Asymmetric {
  all a, b: Tumbler | LT[a, b] implies not LT[b, a]
}

assert Transitive {
  all a, b, c: Tumbler |
    (LT[a, b] and LT[b, c]) implies LT[a, c]
}

assert Trichotomy {
  all a, b: Tumbler |
    LT[a, b] or EQ[a, b] or LT[b, a]
}

assert PrefixIsLess {
  all a, b: Tumbler |
    (a.len < b.len and
     (all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]))
    implies LT[a, b]
}

run FindLT {
  some a, b: Tumbler | LT[a, b]
} for 4 but exactly 2 Tumbler, 4 Int

check Irreflexive for 3 but 4 Int
check Asymmetric for 3 but 4 Int
check Transitive for 3 but 4 Int
check Trichotomy for 3 but 4 Int
check PrefixIsLess for 3 but 4 Int
