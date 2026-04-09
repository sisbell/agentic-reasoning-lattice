include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"

// Endset — ASN-0043
module Endset {
  import opened TumblerAlgebra
  import TumblerAddition

  // Span: a (start, length) pair
  datatype Span = Span(start: Tumbler, length: Tumbler)

  // Well-formedness: delegates to T12 (SpanWellDefined)
  ghost predicate WellFormedSpan(sp: Span) {
    TumblerAddition.SpanWellDefined(sp.start, sp.length)
  }

  // Endset: a finite set of well-formed spans
  type Endset = set<Span>

  // All spans in the endset satisfy T12
  ghost predicate WellFormedEndset(e: Endset) {
    forall sp :: sp in e ==> WellFormedSpan(sp)
  }
}
