include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module FreshPositions {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0026 P9 (new) — FreshPositions (POST, ensures)
  // After INSERT(d, p, k): positions [p, p+k) map to fresh addresses.
  // fresh = SetOf(newAddrs), with fresh ∩ dom(Σ.I) = ∅ established
  // upstream by ISpaceExtension and GlobalUniqueness (ASN-0001).

  // Elements of a sequence as a set
  function SetOf(s: seq<IAddr>): set<IAddr> {
    set i | 0 <= i < |s| :: s[i]
  }

  // V-space as seq<IAddr>, isomorphic to Foundation's vmap under J1.
  // Position j (1-indexed) corresponds to index j-1.
  function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): (v': seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures |v'| == |v| + k
    ensures forall j {:trigger v'[j-1]} :: p <= j < p + k ==> v'[j-1] in SetOf(newAddrs)
  {
    v[..p-1] + newAddrs + v[p-1..]
  }
}
