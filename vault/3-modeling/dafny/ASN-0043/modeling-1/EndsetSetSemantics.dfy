include "Endset.dfy"

// L5 — EndsetSetSemantics
// An endset is an unordered set; only membership matters.
// Encoded in the set type: Dafny's set has extensional equality.
module EndsetSetSemantics {
  import opened Endset

  // Set extensionality: two endsets are equal iff they have the same spans
  lemma SetSemantics(e1: Endset, e2: Endset)
    ensures (e1 == e2) <==> (forall sp :: sp in e1 <==> sp in e2)
  { }
}
