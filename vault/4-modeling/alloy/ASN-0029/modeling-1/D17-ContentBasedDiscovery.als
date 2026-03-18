open util/integer

-- ═══════════════════════════════════════════════════════════════
-- D17 — ContentBasedDiscovery (POST, ensures)
-- ASN-0029 · Document Ontology
--
-- FINDDOCSCONTAINING(S) returns documents whose version list
-- contains at least one address falling within a query span.
-- Pure query — frame: Σ' = Σ.
-- ═══════════════════════════════════════════════════════════════

sig Doc {}

-- Query span (s, l) with l > 0 per T12
sig Span {
  start: Int,
  len:   Int
}

sig State {
  D:   set Doc,
  -- V(d)(p): address value at position p of document d
  V:   Doc -> Int -> lone Int
} {
  -- well-formedness: V scoped to D, positions >= 1
  all d: Doc, p: Int |
    some V[d][p] implies (d in D and p >= 1)
}

----------------------------------------------------------------------
-- Helpers
----------------------------------------------------------------------

-- T12: span well-formedness
pred spanOK[sp: Span] {
  sp.len > 0
}

-- Address v falls in half-open interval [start, start+len)
pred inRange[v: Int, sp: Span] {
  v >= sp.start
  v < plus[sp.start, sp.len]
}

-- Document d (in state s) has a position matching span sp
pred hasMatch[s: State, d: Doc, sp: Span] {
  some p: Int |
    some s.V[d][p] and inRange[s.V[d][p], sp]
}

-- Spec: result set of FINDDOCSCONTAINING
fun specResult[s: State, spans: set Span]: set Doc {
  {d: s.D | some sp: spans | hasMatch[s, d, sp]}
}

----------------------------------------------------------------------
-- Operation
----------------------------------------------------------------------

pred FindDocsContaining[s, sPost: State, spans: set Span,
                        result: set Doc] {
  -- PRE: every span well-formed (T12)
  all sp: spans | spanOK[sp]

  -- POST: result per specification
  result = specResult[s, spans]

  -- FRAME: Σ' = Σ
  sPost.D = s.D
  sPost.V = s.V
}

----------------------------------------------------------------------
-- Assertions
----------------------------------------------------------------------

-- Result is always a subset of Σ.D
assert ResultInDocs {
  all s, sPost: State, spans: set Span, result: set Doc |
    FindDocsContaining[s, sPost, spans, result] implies
      result in s.D
}

-- Pure query: state unchanged
assert PureQuery {
  all s, sPost: State, spans: set Span, result: set Doc |
    FindDocsContaining[s, sPost, spans, result] implies
      (sPost.D = s.D and sPost.V = s.V)
}

-- Empty query yields empty result
assert EmptyQuery {
  all s: State, spans: set Span |
    no spans implies no specResult[s, spans]
}

-- Adding spans is monotonic: more spans => superset of results
assert SpanMonotonic {
  all s: State, sp: Span, spans: set Span |
    (spanOK[sp] and (all sp2: spans | spanOK[sp2])) implies
      specResult[s, spans] in specResult[s, spans + sp]
}

-- Boundary inclusion: value exactly at span.start is found
assert BoundaryInclusion {
  all s: State, d: Doc, sp: Span, p: Int |
    (d in s.D and spanOK[sp] and
     some s.V[d][p] and s.V[d][p] = sp.start) implies
      d in specResult[s, sp]
}

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

-- Find a valid query with non-empty results
run FindQuery {
  some s, sPost: State, spans: set Span, result: set Doc |
    FindDocsContaining[s, sPost, spans, result]
    and some result
} for 4 but exactly 2 State, 5 Int

----------------------------------------------------------------------
-- Checks
----------------------------------------------------------------------

check ResultInDocs for 5 but exactly 2 State, 5 Int
check PureQuery for 5 but exactly 2 State, 5 Int
check EmptyQuery for 5 but 5 Int
check SpanMonotonic for 5 but 5 Int
check BoundaryInclusion for 5 but 5 Int
