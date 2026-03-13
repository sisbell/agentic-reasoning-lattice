-- AdditionAssociative: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)
-- Bounded check for tumbler addition associativity.

abstract sig Tumbler {
  len: one Int,
  comp: Int -> lone Int
}

one sig TA, TB, TC, TAB, TBC, TLHS, TRHS extends Tumbler {}

-- Well-formedness: natural-number sequence of length 1..4
pred wf[t: Tumbler] {
  t.len >= 1
  t.len =< 4
  all i: Int {
    (1 =< i and i =< t.len) implies (one t.comp[i] and t.comp[i] >= 0)
    (i < 1 or i > t.len) implies no t.comp[i]
  }
}

fact { all t: Tumbler | wf[t] }

-- Bound input values so triple sums stay within 5-bit Int range (5+5+5=15)
fact { all t: TA + TB + TC, i: Int | some t.comp[i] implies t.comp[i] =< 5 }

-- k is the action point of t (first nonzero position)
pred isAP[t: Tumbler, k: Int] {
  1 =< k and k =< t.len
  t.comp[k] != 0
  all j: Int | (1 =< j and j < k) implies t.comp[j] = 0
}

-- result = a ⊕ w where w has action point k
-- Result length = #w; prefix from a, advance at k, tail from w
pred tAdd[a, w, result: Tumbler, k: Int] {
  isAP[w, k]
  k =< a.len
  result.len = w.len
  all i: Int | (1 =< i and i =< result.len) implies {
    i < k implies result.comp[i] = a.comp[i]
    i = k implies result.comp[i] = plus[a.comp[k], w.comp[k]]
    i > k implies result.comp[i] = w.comp[i]
  }
}

-- Component-wise tumbler equality
pred tEq[s, t: Tumbler] {
  s.len = t.len
  all i: Int | (1 =< i and i =< s.len) implies s.comp[i] = t.comp[i]
}

-- Both compositions are well-defined
pred bothDefined {
  some kb, kc, kbc: Int {
    isAP[TB, kb]
    isAP[TC, kc]
    tAdd[TA, TB, TAB, kb]
    tAdd[TAB, TC, TLHS, kc]
    tAdd[TB, TC, TBC, kc]
    isAP[TBC, kbc]
    tAdd[TA, TBC, TRHS, kbc]
  }
}

assert AddAssoc {
  bothDefined implies tEq[TLHS, TRHS]
}

-- Non-vacuity: the premise is satisfiable
run NonVacuity {
  bothDefined
} for 4 but 5 Int

check AddAssoc for 4 but 5 Int
