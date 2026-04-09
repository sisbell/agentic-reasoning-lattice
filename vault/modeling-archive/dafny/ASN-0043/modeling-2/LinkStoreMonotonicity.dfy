include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// L12a — LinkStoreMonotonicity
module LinkStoreMonotonicity {
  import opened TumblerAlgebra

  // Span = (start, length) satisfying T12
  datatype Span = Span(start: Tumbler, length: Tumbler)

  // Endset = finite set of spans
  type Endset = set<Span>

  // Link = (from, to, type) triple of endsets
  datatype Link = Link(from: Endset, to: Endset, typeset: Endset)

  // LinkStore = partial function from addresses to links
  type LinkStore = map<Tumbler, Link>

  // L12 — LinkImmutability: every link present before a transition is
  // preserved with the same value after
  ghost predicate LinkImmutability(before: LinkStore, after: LinkStore) {
    forall a :: a in before ==> a in after && after[a] == before[a]
  }

  // L12a — LinkStoreMonotonicity: the domain of the link store only grows
  lemma LinkStoreMonotonicity(before: LinkStore, after: LinkStore)
    requires LinkImmutability(before, after)
    ensures before.Keys <= after.Keys
  { }
}
