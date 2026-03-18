open util/ordering[Pos]

sig Pos {}

sig Tumbler {
  comp: Pos -> lone Int
}

-- Defined positions (domain of comp)
fun defined[t: Tumbler]: set Pos {
  t.comp.Int
}

-- Well-formed: contiguous prefix from first, non-negative values
pred wf[t: Tumbler] {
  some defined[t]
  all p: defined[t] | {
    t.comp[p] >= 0
    prevs[p] in defined[t]
  }
}

-- Positive: at least one nonzero component
pred positive[t: Tumbler] {
  some p: defined[t] | t.comp[p] > 0
}

-- Action point: first position with nonzero component
fun actionPoint[t: Tumbler]: set Pos {
  {p: defined[t] | t.comp[p] > 0 and
    (no q: prevs[p] & defined[t] | t.comp[q] > 0)}
}

-- Divergence: first position where a and b differ
fun divergence[a, b: Tumbler]: set Pos {
  {p: defined[a] | not (a.comp[p] = b.comp[p]) and
    (no q: prevs[p] & defined[a] | not (a.comp[q] = b.comp[q]))}
}

-- Tumbler subtraction: result = a minus w (same-length operands)
pred tSub[a, w, result: Tumbler] {
  defined[a] = defined[w]
  defined[result] = defined[a]
  let d = divergence[a, w] | {
    (no d) implies
      (all p: defined[result] | result.comp[p] = 0)
    (some d) implies {
      all p: prevs[d] & defined[result] | result.comp[p] = 0
      result.comp[d] = minus[a.comp[d], w.comp[d]]
      all p: nexts[d] & defined[result] | result.comp[p] = a.comp[p]
    }
  }
}

-- Tumbler addition: result = s plus w with given action point
pred tAdd[s, w, result: Tumbler, ap: Pos] {
  ap in defined[s]
  ap in defined[w]
  let beforeAp = prevs[ap] & defined[s],
      apAndAfter = (ap + nexts[ap]) & defined[w] | {
    defined[result] = beforeAp + apAndAfter
    all p: beforeAp | result.comp[p] = s.comp[p]
    result.comp[ap] = plus[s.comp[ap], w.comp[ap]]
    all p: nexts[ap] & defined[w] | result.comp[p] = w.comp[p]
  }
}

-- ReverseInverse: (a minus w) plus w = a
-- under: w > 0, actionPoint(w) = k = #a = #w, a_i = 0 for i < k, a >= w
assert ReverseInverse {
  all disj a, w, sub, result: Tumbler, k: Pos |
    (wf[a] and wf[w]
     and positive[w]
     and k = actionPoint[w]
     and no (nexts[k] & defined[w])
     and defined[a] = defined[w]
     and (all p: prevs[k] & defined[a] | a.comp[p] = 0)
     and a.comp[k] >= w.comp[k]
     and tSub[a, w, sub]
     and tAdd[sub, w, result, k])
    implies
    (defined[result] = defined[a] and
     all p: defined[a] | result.comp[p] = a.comp[p])
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
  some disj a, w, sub, result: Tumbler, k: Pos |
    wf[a] and wf[w]
    and positive[w]
    and k = actionPoint[w]
    and no (nexts[k] & defined[w])
    and defined[a] = defined[w]
    and (all p: prevs[k] & defined[a] | a.comp[p] = 0)
    and a.comp[k] >= w.comp[k]
    and tSub[a, w, sub]
    and tAdd[sub, w, result, k]
} for 4 but exactly 4 Tumbler, 5 Int

check ReverseInverse for 4 but exactly 4 Tumbler, 5 Int
