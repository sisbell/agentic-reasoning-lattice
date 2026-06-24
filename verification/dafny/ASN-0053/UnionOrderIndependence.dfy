// ASN-0053: S10 — UnionOrderIndependence (theorem)
// Denote(spans) is invariant under permutation: equal multisets imply equal iset unions.
include "./SpanDefs.dfy"
include "./NormalizationExistence.dfy"

module UnionOrderIndependence {
  import opened SpanDefs
  import NE = NormalizationExistence

  lemma UnionOrderIndependence(spans1: seq<SpanEntry>, spans2: seq<SpanEntry>)
    requires NE.AllValid(spans1) && NE.AllValid(spans2)
    requires multiset(spans1) == multiset(spans2)
    ensures NE.Denote(spans1) == NE.Denote(spans2)
  {
    NE.DenoteSameMultiset(spans1, spans2);
  }
}
