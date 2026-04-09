open util/ordering[Doc]

sig Account {}
sig Version {}
sig Link {}

sig Doc {
  acct: one Account
}

abstract sig Visibility {}
one sig Private, Public extends Visibility {}

sig State {
  D: set Doc,
  V: Doc -> set Version,
  vis: Doc -> lone Visibility,
  I: set Link,
  par: Doc -> lone Doc
} {
  V in D -> Version
  vis in D -> Visibility
  all d: D | one vis[d]
  par in D -> D
}

-- D0: EmptyCreation — create a fresh empty private document under account a
pred EmptyCreation[s, s2: State, a: Account] {
  some d: Doc {
    d not in s.D
    d.acct = a
    s2.D = s.D + d
    no s2.V[d]
    s2.vis[d] = Private
    no s2.par[d]
    all d2: s.D | d2.acct = a implies lt[d2, d]
    s2.I = s.I
    all d2: s.D {
      s2.V[d2] = s.V[d2]
      s2.vis[d2] = s.vis[d2]
      s2.par[d2] = s.par[d2]
    }
  }
}

assert AddsExactlyOne {
  all s, s2: State, a: Account |
    EmptyCreation[s, s2, a] implies one (s2.D - s.D)
}

assert SequentiallyOrdered {
  all s1, s2, s3: State, a: Account |
    (EmptyCreation[s1, s2, a] and EmptyCreation[s2, s3, a]) implies
      all d1: s2.D - s1.D, d2: s3.D - s2.D | lt[d1, d2]
}

run FindEmptyCreation {
  some s, s2: State, a: Account |
    EmptyCreation[s, s2, a]
} for 5 but exactly 2 State

check AddsExactlyOne for 5 but exactly 2 State
check SequentiallyOrdered for 6 but exactly 3 State
