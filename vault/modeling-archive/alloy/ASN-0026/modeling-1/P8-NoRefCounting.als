-- P8-NoRefCounting.als
-- P8: dom(Sigma.I) never shrinks, regardless of |refs(a)|.
-- Content persists even when refs(a) = emptyset.
-- Derived from P1 (content immutability / append-only I-space).

sig Addr {}
sig Byte {}
sig DocId {}

sig State {
  ispace: Addr -> lone Byte,           -- Sigma.I: partial function Addr -> Byte
  docs: set DocId,                      -- Sigma.D: document set
  vspace: DocId -> Int -> lone Addr     -- Sigma.V: per-doc position -> Addr
}

-- Domain of I-space
fun dom[s: State]: set Addr {
  (s.ispace).Byte
}

-- refs(a): doc-position pairs referencing address a
fun refs[s: State, a: Addr]: DocId -> Int {
  { d: DocId, p: Int | d -> p -> a in s.vspace }
}

-- Well-formedness: vspace only for existing docs, positions positive,
-- vspace targets allocated in I-space
pred wellFormed[s: State] {
  all d: DocId, p: Int |
    some s.vspace[d][p] implies (d in s.docs and p > 0)
  all d: DocId, p: Int |
    some s.vspace[d][p] implies s.vspace[d][p] in dom[s]
}

-- Transition: any valid state change obeying P1 (append-only I-space)
pred transition[s, sPost: State] {
  wellFormed[s]
  wellFormed[sPost]
  -- P1: I-space domain only grows
  dom[s] in dom[sPost]
  -- P1: existing mappings are immutable
  all a: dom[s] | sPost.ispace[a] = s.ispace[a]
}

-- P8: addresses with zero refs in post-state still persist
assert NoRefCounting {
  all s, sPost: State, a: Addr |
    (transition[s, sPost] and a in dom[s] and no refs[sPost, a])
      implies a in dom[sPost]
}

-- Strengthened form: even if refs drop from positive to zero, address persists
assert DropToZeroRefsPersists {
  all s, sPost: State, a: Addr |
    (transition[s, sPost] and a in dom[s]
      and some refs[s, a] and no refs[sPost, a])
      implies a in dom[sPost]
}

-- Non-vacuity: find a transition where refs drop to zero yet address persists
run NonVacuity {
  some s, sPost: State, a: Addr |
    transition[s, sPost]
    and some refs[s, a]
    and no refs[sPost, a]
    and a in dom[sPost]
} for 4 but exactly 2 State, 4 Int

check NoRefCounting for 5 but exactly 2 State, 4 Int
check DropToZeroRefsPersists for 5 but exactly 2 State, 4 Int
