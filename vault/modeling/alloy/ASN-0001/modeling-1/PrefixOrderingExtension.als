sig Tumbler {
  comps: seq Int
} {
  all i: comps.inds | comps[i] >= 0
}

pred prefixOf[p, t: Tumbler] {
  #p.comps =< #t.comps
  all i: p.comps.inds | p.comps[i] = t.comps[i]
}

pred lex_lt[a, b: Tumbler] {
  (some k: a.comps.inds & b.comps.inds | {
    a.comps[k] < b.comps[k]
    all j: a.comps.inds & b.comps.inds | j < k implies a.comps[j] = b.comps[j]
  }) or
  (prefixOf[a, b] and #a.comps < #b.comps)
}

assert PrefixOrderingExtension {
  all p1, p2, a, b: Tumbler |
    (lex_lt[p1, p2] and
     not prefixOf[p1, p2] and
     not prefixOf[p2, p1] and
     prefixOf[p1, a] and
     prefixOf[p2, b])
    implies lex_lt[a, b]
}

run NonVacuous {
  some p1, p2, a, b: Tumbler |
    lex_lt[p1, p2] and
    not prefixOf[p1, p2] and
    not prefixOf[p2, p1] and
    prefixOf[p1, a] and
    prefixOf[p2, b]
} for 5 but 3 seq, 5 Int

check PrefixOrderingExtension for 5 but 3 seq, 5 Int
