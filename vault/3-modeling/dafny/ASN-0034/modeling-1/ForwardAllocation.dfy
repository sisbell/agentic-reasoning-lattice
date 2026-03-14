include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ForwardAllocation {

  import opened TumblerAlgebra

  // T9 — ForwardAllocation
  // Each allocator controls a single ownership prefix and allocates
  // sequentially within it. New addresses are strictly monotonically
  // increasing: (A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)
  //
  // Transition invariant: for any consecutive pair of allocations
  // (prev, next) from the same allocator, prev < next under T1.
  ghost predicate ForwardAllocation(prev: Tumbler, next: Tumbler) {
    LessThan(prev, next)
  }

  // Structural guarantee: shared prefix with strictly increasing
  // component at the first divergence point implies forward allocation.
  // This is the mechanism by which sequential allocation guarantees T9:
  // same allocator → shared prefix, sequential → increasing suffix.
  lemma SharedPrefixForward(prev: Tumbler, next: Tumbler, k: nat)
    requires k <= |prev.components| && k <= |next.components|
    requires forall i :: 0 <= i < k ==> prev.components[i] == next.components[i]
    requires k < |prev.components| && k < |next.components|
    requires prev.components[k] < next.components[k]
    ensures ForwardAllocation(prev, next)
  {
    LessThanIntro(prev, next, k);
  }
}
