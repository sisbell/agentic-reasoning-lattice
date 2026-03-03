-- T10 — PartitionIndependence
-- If p1 and p2 are prefix-incomparable (neither is a prefix of the other),
-- then any tumbler with prefix p1 is distinct from any tumbler with prefix p2.
--
-- Proof sketch: suppose a = b. Then a has both p1 and p2 as prefixes.
-- WLOG #p1 <= #p2; then for all i in p1.inds, p1[i] = a[i] = p2[i],
-- so p1 is a prefix of p2 — contradicting the incomparability assumption.

sig Tumbler {
  comps: seq Int
}

-- p is a prefix of t: p is no longer than t, and they agree on every position of p.
pred isPrefix[p, t: Tumbler] {
  #p.comps =< #t.comps
  all i: p.comps.inds | p.comps[i] = t.comps[i]
}

assert PartitionIndependence {
  all p1, p2, a, b: Tumbler |
    (not isPrefix[p1, p2] and
     not isPrefix[p2, p1] and
     isPrefix[p1, a] and
     isPrefix[p2, b])
    implies not (a = b)
}

-- Non-vacuity: two incomparable prefixes, each extended to a longer tumbler.
run NonVacuous {
  some p1, p2, a, b: Tumbler |
    not isPrefix[p1, p2] and
    not isPrefix[p2, p1] and
    isPrefix[p1, a] and
    isPrefix[p2, b]
} for 4 but 4 Tumbler, 5 Int

check PartitionIndependence for 5 but 5 Int
