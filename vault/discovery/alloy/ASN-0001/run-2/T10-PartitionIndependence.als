-- T10 — PartitionIndependence
-- Two allocators with distinct, non-nesting prefixes produce
-- guaranteed-distinct addresses.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

-- A tumbler is well-formed: length >= 1, components defined exactly
-- at positions 1..len, all components non-negative.
pred wellFormed[t: Tumbler] {
  t.len >= 1
  all i: Int | (i >= 1 and i =< t.len) implies
    (one t.comp[i] and t.comp[i] >= 0)
  all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
}

-- p is a prefix of t: p's length <= t's length and they agree
-- on all positions 1..len(p).
pred isPrefix[p, t: Tumbler] {
  p.len =< t.len
  all i: Int | (i >= 1 and i =< p.len) implies
    p.comp[i] = t.comp[i]
}

-- Neither prefix nests within the other.
pred nonNesting[p1, p2: Tumbler] {
  not isPrefix[p1, p2]
  not isPrefix[p2, p1]
}

-- Content equality: same length and same component values.
pred sameAddress[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies
    a.comp[i] = b.comp[i]
}

-- Main property: non-nesting prefixes guarantee distinct addresses.
assert PartitionIndependence {
  all p1, p2, a, b: Tumbler |
    (wellFormed[p1] and wellFormed[p2]
     and wellFormed[a] and wellFormed[b]
     and nonNesting[p1, p2]
     and isPrefix[p1, a]
     and isPrefix[p2, b])
    implies not sameAddress[a, b]
}

-- Non-vacuity: there exist two non-nesting prefixes with
-- extensions that are indeed distinct.
run NonVacuity {
  some p1, p2, a, b: Tumbler |
    wellFormed[p1] and wellFormed[p2]
    and wellFormed[a] and wellFormed[b]
    and nonNesting[p1, p2]
    and isPrefix[p1, a]
    and isPrefix[p2, b]
    and not sameAddress[a, b]
} for 5 but 5 Int

check PartitionIndependence for 5 but 5 Int
