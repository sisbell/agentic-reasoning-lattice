open util/ordering[Step]

-- Tumblers: 3-component integer sequences (positions 1..3).
-- Components bounded to [0,5] to prevent Int overflow in the bounded check.

sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
}

pred wf[t: Tumbler] {
  t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
  t.c1 < 6 and t.c2 < 6 and t.c3 < 6
}

pred positive[w: Tumbler] {
  w.c1 > 0 or w.c2 > 0 or w.c3 > 0
}

-- Lexicographic order on 3-component tumblers.
pred lexLt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- TumblerAdd: r = a ⊕ w.
-- Action point k = first position where w is nonzero.
-- Prefix i < k: copied from a.  Position k: advanced (aₖ + wₖ).  Tail i > k: from w.
pred tAdd[a, w, r: Tumbler] {
  wf[a] and wf[w] and wf[r]
  positive[w]
  w.c1 > 0 => {
    r.c1 = plus[a.c1, w.c1]
    r.c2 = w.c2
    r.c3 = w.c3
  } else w.c2 > 0 => {
    r.c1 = a.c1
    r.c2 = plus[a.c2, w.c2]
    r.c3 = w.c3
  } else {
    r.c1 = a.c1
    r.c2 = a.c2
    r.c3 = plus[a.c3, w.c3]
  }
}

-- Sequential allocation chain: each Step holds an allocated address and the
-- positive displacement used to reach it. The ordering on Step models time.
sig Step {
  addr: Tumbler,
  disp: Tumbler
}

fact WFChain {
  all s: Step | wf[s.addr] and wf[s.disp] and positive[s.disp]
  -- Each step's successor address = this step's address advanced by the successor's displacement.
  all s: Step | some next[s] implies tAdd[s.addr, next[s].disp, next[s].addr]
}

-- T9/T10: TumblerAdd is strictly monotone under lexicographic order.
-- At the action point k, rₖ = aₖ + wₖ > aₖ (since wₖ > 0); prefix is equal.
assert TAddStrictlyAdvances {
  all a, w, r: Tumbler |
    tAdd[a, w, r] implies lexLt[a, r]
}

-- GlobalUniqueness (LEMMA): No two distinct allocations in the chain share an address.
-- Follows from strict monotonicity: the chain addr(first) <_lex addr(s1) <_lex ... are all distinct.
assert GlobalUniqueness {
  all s, s2: Step | s.addr = s2.addr implies s = s2
}

-- Non-vacuity: find a valid 3-step allocation chain.
run FindChain {} for 5 but exactly 3 Step, 8 Tumbler, 5 Int

-- Supporting lemma: TAdd always advances lexicographically (no overflow in bounded scope).
check TAddStrictlyAdvances for 5 but 4 Tumbler, 5 Int

-- Main property: all allocated addresses are distinct across the chain.
check GlobalUniqueness for 5 but exactly 3 Step, 8 Tumbler, 5 Int
