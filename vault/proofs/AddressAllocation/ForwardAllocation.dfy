module ForwardAllocation {

  import opened TumblerAlgebra

  // T9 — ForwardAllocation (INV, predicate(State, State))
  // transition invariant

  // Allocator identifier
  datatype AllocatorId = AllocatorId(id: nat)

  // Allocation state: per-allocator ordered stream of allocated addresses
  datatype AllocState = AllocState(streams: map<AllocatorId, seq<Tumbler>>)

  // A sequence of tumblers is strictly monotonically ordered under LessThan
  ghost predicate StrictlyOrdered(stream: seq<Tumbler>) {
    forall i, j :: 0 <= i < j < |stream| ==> LessThan(stream[i], stream[j])
  }

  // T9: within each allocator's sequential stream, addresses are strictly
  // monotonically increasing. Across a state transition, streams grow
  // append-only and the ordering is maintained.
  ghost predicate ForwardAllocation(s: AllocState, s': AllocState) {
    // Every allocator's stream in s is preserved (append-only growth)
    (forall a :: a in s.streams ==>
      a in s'.streams &&
      |s'.streams[a]| >= |s.streams[a]| &&
      s'.streams[a][..|s.streams[a]|] == s.streams[a]) &&
    // Every allocator's stream in s' is strictly ordered
    (forall a :: a in s'.streams ==> StrictlyOrdered(s'.streams[a]))
  }
}
