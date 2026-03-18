// L5 — EndsetSetSemantics
// An endset is an unordered set; only span membership matters.
// Encoded in Dafny's set<Span> type, which provides set equality semantics.

include "Endset.dfy"

module EndsetSetSemantics {
  import opened Endset

  // L5: Endset equality is characterized by membership alone.
  // Tautological for Dafny's set type — ordering carries no meaning.
  lemma EndsetSetSemantics(e1: Endset, e2: Endset)
    ensures (e1 == e2) <==> (forall sp :: sp in e1 <==> sp in e2)
  { }
}
