// ASN-0034: TA7a.3 — SubspaceZeroResidue
// Self-subtraction collapses to the zero tumbler:
//   (A o ∈ S : o ⊖ o ∈ Z).
include "./SubspaceClosure.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./TumblerSub.dfy"
include "./ZeroPaddedDivergence.dfy"

module SubspaceZeroResidue {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened SubspaceClosure

  // FirstPaddedMismatch on identical inputs always exhausts to L + 1.
  lemma FirstPaddedMismatchSelf(a: Tumbler, start: nat, L: nat)
    requires InT(a)
    requires 1 <= start <= L + 1
    ensures FirstPaddedMismatch(a, a, start, L) == L + 1
    decreases L + 1 - start
  {
    if start <= L {
      FirstPaddedMismatchSelf(a, start + 1, L);
    }
  }

  lemma SubspaceZeroResidue(o: Tumbler)
    requires InT(o)
    requires InSubspaceS(o)
    ensures InT(TumblerSub.TumblerSub(o, o))
    ensures PositiveTumbler.ZeroTumbler(TumblerSub.TumblerSub(o, o))
  {
    var L := Length(o);
    FirstPaddedMismatchSelf(o, 1, L);
    assert ZeroPaddedDivergence(o, o) == 0;
  }
}
