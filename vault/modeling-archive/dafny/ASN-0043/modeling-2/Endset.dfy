// Endset — Endset (DEF, type)
// ASN-0043: Endset = 𝒫_fin(Span) where Span satisfies T12 (SpanWellDefined)

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"

module Endset {
  import opened TumblerAlgebra
  import TumblerAddition

  // Span: a pair (start, length) — well-formed when T12 holds
  datatype Span = Span(start: Tumbler, length: Tumbler)

  ghost predicate WellFormedSpan(sp: Span) {
    TumblerAddition.SpanWellDefined(sp.start, sp.length)
  }

  // Endset: finite set of spans
  type Endset = set<Span>

  ghost predicate WellFormedEndset(e: Endset) {
    forall sp :: sp in e ==> WellFormedSpan(sp)
  }
}
