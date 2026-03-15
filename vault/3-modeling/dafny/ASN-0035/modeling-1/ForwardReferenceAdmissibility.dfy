// N7 — ForwardReferenceAdmissibility (LEMMA, lemma)
// ASN-0035: Node Ontology — derived from T12

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"

module ForwardReferenceAdmissibility {
  import opened TumblerAlgebra
  import TumblerAddition

  // N7 — ForwardReferenceAdmissibility
  // A reference may target any address in N, regardless of baptism status.
  // Well-definedness of a span (s, l) under T12 depends only on arithmetic
  // properties of s and l — no system state or node-existence check appears.
  //
  // DIVERGENCE: The ASN states N7 for three reference types: spans, link
  // endsets, and type addresses. Only span well-definedness is formalized
  // here, as links and type addresses are not yet modeled. The argument
  // for all three is identical: well-formedness predicates are arithmetic,
  // not state-dependent.
  lemma ForwardReferenceAdmissibility(s: Tumbler, l: Tumbler)
    requires PositiveTumbler(l)
    requires ActionPoint(l) < |s.components|
    ensures TumblerAddition.SpanWellDefined(s, l)
    ensures LessThan(s, TumblerAdd(s, l))
  {
    TumblerAddition.SpanNonEmpty(s, l);
  }
}
