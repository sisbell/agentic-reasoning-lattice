-- D7-OriginTraceability.als
-- Property D7: home(Σ.V(d)(p)) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ Σ.V(d)(p)}
-- Every I-address in document content has a well-defined home document.
-- Depends on T4 (HierarchicalParsing): fields() uniquely decomposes any
-- I-address, so the set of document-level prefixes forms a chain with a
-- unique maximum.

----------------------------------------------------------------------
-- Address hierarchy
----------------------------------------------------------------------

sig Addr {
  below: set Addr    -- {b : b ≼ this} — all prefixes of this address
}

-- Document-level addresses (zeros = 2)
sig DocAddr in Addr {}

----------------------------------------------------------------------
-- Prefix relation axioms
----------------------------------------------------------------------

fact PrefixPartialOrder {
  -- reflexive
  all a: Addr | a in a.below
  -- antisymmetric
  all a, b: Addr | (a in b.below and b in a.below) implies a = b
  -- transitive
  all a, b, c: Addr | (c in b.below and b in a.below) implies c in a.below
}

-- T4 (HierarchicalParsing): document-level prefixes of any address
-- form a chain (linearly ordered under ≼)
fact T4_HierarchicalParsing {
  all a: Addr, d1, d2: a.below & DocAddr |
    d1 in d2.below or d2 in d1.below
}

-- Every address extends from at least one document
fact HasDocPrefix {
  all a: Addr | some (a.below & DocAddr)
}

----------------------------------------------------------------------
-- Document content (versioned state)
----------------------------------------------------------------------

sig Pos {}

one sig State {
  content: DocAddr -> Pos -> lone Addr    -- Σ.V(d)(p)
}

-- Content addresses extend their containing document
fact ContentExtendsDoc {
  all d: DocAddr, p: Pos, v: Addr |
    v in State.content[d][p] implies d in v.below
}

----------------------------------------------------------------------
-- home function
----------------------------------------------------------------------

-- home(a) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}
-- The unique maximal document-level prefix of a.
fun home[a: Addr]: set DocAddr {
  {d: a.below & DocAddr | (a.below & DocAddr) in d.below}
}

----------------------------------------------------------------------
-- D7 assertions
----------------------------------------------------------------------

-- D7: home is well-defined (exactly one) for every content address
assert D7_OriginTraceability {
  all d: DocAddr, p: Pos |
    (some State.content[d][p]) implies one home[State.content[d][p]]
}

-- Stronger: home is well-defined for ALL addresses
assert D7_Universal {
  all a: Addr | one home[a]
}

----------------------------------------------------------------------
-- Scope
----------------------------------------------------------------------

-- Non-vacuity: content exists and home is computable
run NonVacuity {
  some d: DocAddr, p: Pos |
    some State.content[d][p]
} for 4

-- Transclusion: content whose home differs from its container
run Transclusion {
  some d: DocAddr, p: Pos, v: Addr |
    v in State.content[d][p] and not (home[v] = d)
} for 5

check D7_OriginTraceability for 5
check D7_Universal for 5
