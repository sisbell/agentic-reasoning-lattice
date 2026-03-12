-- D7b — HomeDocumentMembership (LEMMA)
-- Derived from D7a, P2, D2.
--
-- Property: (A d in Sigma.D, p : 1 <= p <= n_d : home(Sigma.V(d)(p)) in Sigma.D)
--
-- Every I-address appearing in any document's version list has its home
-- document in D. Follows from:
--   P2:  V(d)(p) in dom(Sigma.I)        (referential completeness)
--   D7a: allocated addresses are scoped under their creating document
--   D2:  documents are permanent

----------------------------------------------------------------------
-- Address hierarchy (consistent with D7-OriginTraceability)
----------------------------------------------------------------------

sig Addr {
  below: set Addr    -- {b : b =< this} — prefixes of this address
}

sig DocAddr in Addr {}

fact PrefixPartialOrder {
  -- reflexive
  all a: Addr | a in a.below
  -- antisymmetric
  all a, b: Addr | (a in b.below and b in a.below) implies a = b
  -- transitive
  all a, b, c: Addr | (c in b.below and b in a.below) implies c in a.below
}

-- T4 (HierarchicalParsing): doc-level prefixes of any address form a chain
fact T4_DocPrefixChain {
  all a: Addr, d1, d2: a.below & DocAddr |
    d1 in d2.below or d2 in d1.below
}

-- Every address extends from at least one document
fact HasDocPrefix {
  all a: Addr | some (a.below & DocAddr)
}

----------------------------------------------------------------------
-- home function
----------------------------------------------------------------------

-- home(a) = max=< {d' : d' in DocAddr /\ d' =< a}
fun home[a: Addr]: set DocAddr {
  {d: a.below & DocAddr | (a.below & DocAddr) in d.below}
}

----------------------------------------------------------------------
-- System state
----------------------------------------------------------------------

sig Pos {}

one sig Sigma {
  D: set DocAddr,
  I: set Addr,                         -- dom(Sigma.I): allocated I-addresses
  V: DocAddr -> Pos -> lone Addr       -- version function: V(d)(p)
}

----------------------------------------------------------------------
-- Supporting properties (premises of the lemma)
----------------------------------------------------------------------

-- P2 (ReferentialCompleteness): every V-position maps to an allocated I-address
fact P2 {
  all d: Sigma.D, p: Pos |
    let a = Sigma.V[d][p] |
      some a implies a in Sigma.I
}

-- D7a + D2 combined invariant: every allocated I-address has its home
-- document in D.
-- D7a: addresses are allocated under existing documents (scoped INSERT).
-- D2: documents, once in D, remain permanently.
-- Together: the home doc of any allocated address was in D at allocation
-- time, and by permanence is still in D.
fact AllocatedHomeInD {
  all a: Sigma.I | home[a] in Sigma.D
}

----------------------------------------------------------------------
-- D7b assertion
----------------------------------------------------------------------

assert HomeDocumentMembership {
  all d: Sigma.D, p: Pos |
    let a = Sigma.V[d][p] |
      some a implies home[a] in Sigma.D
}

----------------------------------------------------------------------
-- Non-vacuity: content whose home differs from its container (transclusion)
----------------------------------------------------------------------

run NonVacuity {
  some d: Sigma.D, p: Pos, a: Addr |
    a in Sigma.V[d][p] and not (home[a] = d)
} for 5

check HomeDocumentMembership for 5
