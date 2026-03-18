include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SpanWellDefined {
  import opened TumblerAlgebra

  // T12 — SpanWellDefined
  // A span (s, len) with len > 0 denotes {t : s ≤ t < s ⊕ len}.
  // Well-defined when len is positive and its action point falls within s.
  ghost predicate SpanWellDefined(s: Tumbler, len: Tumbler) {
    PositiveTumbler(len) &&
    ActionPoint(len) < |s.components|
  }

  // Non-emptiness from TA-strict: s ⊕ len > s when the span is well-defined.
  // The interval [s, s ⊕ len) therefore contains at least s itself.
  lemma SpanNonEmpty(s: Tumbler, len: Tumbler)
    requires SpanWellDefined(s, len)
    ensures LessThan(s, TumblerAdd(s, len))
  { }
}
