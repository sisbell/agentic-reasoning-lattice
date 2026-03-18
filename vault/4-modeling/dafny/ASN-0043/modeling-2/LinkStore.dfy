// Σ.L — LinkStore (DEF, State field)
// ASN-0043: T ⇀ Link — partial function mapping tumbler addresses to link values

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"

module LinkStore {
  import opened TumblerAlgebra
  import TumblerAddition

  // Span: a pair (start, length) satisfying T12 (SpanWellDefined)
  datatype Span = Span(start: Tumbler, length: Tumbler)

  ghost predicate WellFormedSpan(sp: Span) {
    TumblerAddition.SpanWellDefined(sp.start, sp.length)
  }

  // Endset: finite set of well-formed spans
  type Endset = set<Span>

  ghost predicate WellFormedEndset(e: Endset) {
    forall sp :: sp in e ==> WellFormedSpan(sp)
  }

  // Link: triple of endsets (from, to, type)
  datatype Link = Link(from: Endset, to: Endset, typ: Endset)

  ghost predicate WellFormedLink(link: Link) {
    WellFormedEndset(link.from) &&
    WellFormedEndset(link.to) &&
    WellFormedEndset(link.typ)
  }

  // LinkStore: partial function T ⇀ Link
  type Store = map<Tumbler, Link>

  ghost predicate WellFormedStore(store: Store) {
    forall a :: a in store ==> WellFormedLink(store[a])
  }
}
