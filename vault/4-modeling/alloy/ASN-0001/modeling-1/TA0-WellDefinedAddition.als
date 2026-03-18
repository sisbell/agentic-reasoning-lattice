-- TA0: WellDefinedAddition
-- Property (PRE): when w is positive and the action point of w falls within a,
-- TumblerAdd a⊕w produces a well-defined tumbler (all components non-negative).
--
-- Action point (0-indexed): first nonzero position in w.
-- Precondition: actionPt(w) < #a.comps  (action point within a's length).
-- Result length = #w.comps (prefix copy + single advance + tail replacement).

sig Tumbler {
  comps: seq Int
}

-- All components non-negative.
pred wf[t: Tumbler] {
  all i: t.comps.inds | t.comps[i] >= 0
}

-- At least one component is nonzero.
pred positive[t: Tumbler] {
  some i: t.comps.inds | not (t.comps[i] = 0)
}

-- k is the action point of w: 0-indexed position of the first nonzero component.
pred isActionPt[w: Tumbler, k: Int] {
  k in w.comps.inds
  not (w.comps[k] = 0)
  all j: w.comps.inds | j < k implies w.comps[j] = 0
}

-- r = a ⊕ w under action point k.
-- Encodes the three-case definition; k < #a.comps is the precondition.
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPt[w, k]
  k < #a.comps
  #r.comps = #w.comps
  all i: r.comps.inds |
    (i < k implies r.comps[i] = a.comps[i]) and
    (i = k implies r.comps[i] = plus[a.comps[k], w.comps[k]]) and
    (i > k implies r.comps[i] = w.comps[i])
}

-- TA0: well-formed inputs + precondition => well-formed result.
-- The overflow guard (plus[..] >= 0) excludes spurious counterexamples
-- that arise from bounded Int arithmetic; in the mathematical model
-- with natural-number components the sum is always non-negative.
assert TA0_WellDefinedAddition {
  all a, w, r: Tumbler, k: Int |
    (wf[a] and wf[w] and
     tumblerAdd[a, w, r, k] and
     plus[a.comps[k], w.comps[k]] >= 0)
    implies wf[r]
}

-- Non-vacuity: the precondition scenario must be satisfiable.
run nonVacuous {
  some a, w, r: Tumbler | some k: Int |
    wf[a] and wf[w] and positive[w] and
    tumblerAdd[a, w, r, k] and
    plus[a.comps[k], w.comps[k]] >= 0
} for 4 but 5 Int

check TA0_WellDefinedAddition for 4 but 5 Int
