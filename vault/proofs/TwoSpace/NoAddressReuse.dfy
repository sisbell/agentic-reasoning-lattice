
module NoAddressReuse {
  import opened Foundation
  import ISpaceImmutable

  // NO-REUSE — NoAddressReuse (LEMMA, lemma)
  // derived from P0 (ISpaceImmutable), P1 (ISpaceMonotone)
  // P1 is subsumed by P0 in the Dafny encoding: ISpaceImmutable
  // requires a in s'.iota (domain preservation) to make s'.iota[a]
  // well-formed, so P0 alone suffices as precondition.
  lemma NoAddressReuse(s: State, s': State, a: IAddr)
    requires ISpaceImmutable.ISpaceImmutable(s, s')
    requires a in Allocated(s)
    ensures a in Allocated(s')
    ensures s'.iota[a] == s.iota[a]
  { }
}
