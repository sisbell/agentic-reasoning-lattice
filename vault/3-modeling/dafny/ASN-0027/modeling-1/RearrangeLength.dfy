include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangeLength {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0027 A3.length — RearrangeLength (POST, ensures)
  // |Σ'.V(d)| = n_d

  // Rearrange on seq-based V-space (1-indexed positions, 0-indexed seq).
  // Constructs v' using σ⁻¹: v'[i] = v[σ⁻¹(i+1) - 1].
  function RearrangeV(v: seq<IAddr>, sigmaInv: nat -> nat): (v': seq<IAddr>)
    requires forall i :: 1 <= i <= |v| ==> 1 <= sigmaInv(i) <= |v|
    ensures |v'| == |v|
  {
    seq(|v|, i requires 0 <= i < |v| => v[sigmaInv(i + 1) - 1])
  }
}
