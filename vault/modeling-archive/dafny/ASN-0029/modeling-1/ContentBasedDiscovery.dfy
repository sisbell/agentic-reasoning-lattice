include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ContentBasedDiscovery {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0029 D17 — ContentBasedDiscovery (POST, ensures)
  // pure query; frame: Σ' = Σ

  // Query span: start address and positive displacement
  datatype Span = Span(start: Tumbler, disp: Tumbler)

  // Span well-formedness: displacement is positive (T12) and
  // action point within start's length (TumblerAdd precondition)
  ghost predicate ValidSpan(sp: Span) {
    PositiveTumbler(sp.disp) &&
    ActionPoint(sp.disp) < |sp.start.components|
  }

  // Tumbler less-than-or-equal
  ghost predicate LessEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  // Address falls in half-open interval [start, start ⊕ disp)
  ghost predicate InRange(addr: Tumbler, sp: Span) {
    ValidSpan(sp) &&
    LessEqual(sp.start, addr) &&
    LessThan(addr, TumblerAdd(sp.start, sp.disp))
  }

  // Document d has a position whose address falls in some span
  ghost predicate HasMatch(s: State, d: DocId, spans: set<Span>)
    requires d in s.vmap
  {
    exists q :: q in s.vmap[d] &&
      exists sp :: sp in spans && InRange(s.vmap[d][q], sp)
  }

  // Spec result: {d ∈ Σ.D : ∃ q, (s,l) ∈ S : s ≤ Σ.V(d)(q) < s ⊕ l}
  ghost function FindDocsContaining(s: State, spans: set<Span>): set<DocId>
    requires WellFormed(s)
    requires forall sp :: sp in spans ==> ValidSpan(sp)
    ensures FindDocsContaining(s, spans) <= s.docs
  {
    set d | d in s.docs && d in s.vmap && HasMatch(s, d, spans)
  }

  // D17: FINDDOCSCONTAINING postcondition and frame
  ghost predicate ContentBasedDiscovery(
    s: State, s': State, spans: set<Span>, result: set<DocId>
  )
    requires WellFormed(s)
    requires forall sp :: sp in spans ==> ValidSpan(sp)
  {
    result == FindDocsContaining(s, spans) &&
    s' == s
  }
}
