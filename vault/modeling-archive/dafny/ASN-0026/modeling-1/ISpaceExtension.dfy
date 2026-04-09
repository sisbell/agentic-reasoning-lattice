include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "ISpaceImmutable.dfy"

module ISpaceExtension {
  import opened Foundation
  import ISpaceImmutable

  // ASN-0026 +_ext — ISpaceExtension (LEMMA)
  // derived from P0 (ISpaceImmutable), P1 (ISpaceMonotone)
  // P1 is subsumed by P0 in the Dafny encoding (see NoAddressReuse).

  // Extension: s.iota is a submap of s'.iota
  ghost predicate ISpaceExtends(s: State, s': State) {
    Allocated(s) <= Allocated(s') &&
    forall a :: a in Allocated(s) ==> s'.iota[a] == s.iota[a]
  }

  // Fresh addresses introduced by a transition
  ghost function Fresh(s: State, s': State): set<IAddr> {
    Allocated(s') - Allocated(s)
  }

  // +_ext: I-space transitions are pure extensions with fresh addresses
  // disjoint from the prior domain.
  lemma ISpaceExtensionLemma(s: State, s': State)
    requires ISpaceImmutable.ISpaceImmutable(s, s')
    ensures ISpaceExtends(s, s')
    ensures Fresh(s, s') !! Allocated(s)
  { }
}
