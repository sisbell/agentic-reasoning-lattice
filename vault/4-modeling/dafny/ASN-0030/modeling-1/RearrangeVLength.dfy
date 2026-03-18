include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangeVLength {
  import opened Foundation

  // ASN-0030 A4a(b) — RearrangeVLength (FRAME, ensures)
  // |Σ'.V(d)| = |Σ.V(d)|

  // Bijection on [0..n): a permutation of indices
  ghost predicate IsBijection(pi: seq<nat>, n: nat) {
    |pi| == n &&
    (forall i :: 0 <= i < n ==> pi[i] < n) &&
    (forall i, j :: 0 <= i < j < n ==> pi[i] != pi[j])
  }

  // REARRANGE on seq-based V-space: apply permutation pi to reorder positions
  function RearrangeV(v: seq<IAddr>, pi: seq<nat>): (v': seq<IAddr>)
    requires IsBijection(pi, |v|)
    ensures |v'| == |v|
  {
    seq(|v|, i requires 0 <= i < |v| => v[pi[i]])
  }
}
