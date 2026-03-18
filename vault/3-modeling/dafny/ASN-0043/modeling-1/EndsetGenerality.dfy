include "LinkStore.dfy"

// L4 — EndsetGenerality
module EndsetGenerality {
  import opened LinkStore

  // All spans from all three endset slots of a link
  function AllSpans(link: Link): set<Span> {
    link.from + link.to + link.typ
  }

  // L4 — EndsetGenerality
  // The only constraint on endset spans is T12 (SpanWellDefined).
  // No restriction confines spans to a single document, to content
  // addresses only, or to addresses at which content currently exists.
  // Sub-properties (a) cross-document, (b) intra-document, (c) cross-subspace
  // hold by absence of further constraints in this predicate.
  ghost predicate EndsetGenerality(store: Store) {
    forall a :: a in store ==>
      forall sp :: sp in AllSpans(store[a]) ==> WellFormedSpan(sp)
  }
}
