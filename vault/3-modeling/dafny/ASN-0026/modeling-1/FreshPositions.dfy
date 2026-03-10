include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "InsertOps.dfy"

module FreshPositions {
  import opened Foundation
  import opened InsertOps

  // ASN-0026 P9 (new) — FreshPositions (POST, ensures)
  // After INSERT(d, p, k): positions [p, p+k) map to fresh addresses.
  // fresh = SetOf(newAddrs), with fresh ∩ dom(Σ.I) = ∅ established
  // upstream by ISpaceExtension and GlobalUniqueness (ASN-0001).

  lemma FreshPositions(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures var v' := InsertV(v, p, k, newAddrs);
            forall j {:trigger v'[j-1]} :: p <= j < p + k ==> v'[j-1] in SetOf(newAddrs)
  {
    var v' := InsertV(v, p, k, newAddrs);
    forall j {:trigger v'[j-1]} | p <= j < p + k
      ensures v'[j-1] in SetOf(newAddrs)
    {
      assert v'[j-1] == newAddrs[j-p];
    }
  }
}
