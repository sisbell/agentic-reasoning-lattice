include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SpanWellDefined {
  import opened TumblerAlgebra

  // T12: A span (s, l) is well-formed when l > 0 and the action point
  // of l falls within s's length.
  ghost predicate SpanWellDefined(s: Tumbler, l: Tumbler) {
    PositiveTumbler(l) &&
    ActionPoint(l) < |s.components|
  }

  // Non-emptiness: a well-formed span satisfies s < s ⊕ l,
  // so the interval [s, s ⊕ l) contains at least s itself.
  lemma SpanNonEmpty(s: Tumbler, l: Tumbler)
    requires SpanWellDefined(s, l)
    ensures LessThan(s, TumblerAdd(s, l))
  {
    var k := ActionPoint(l);
    var r := TumblerAdd(s, l);
    LessThanIntro(s, r, k);
  }
}
