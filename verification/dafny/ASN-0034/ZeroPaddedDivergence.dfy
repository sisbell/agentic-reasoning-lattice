// ASN-0034: ZPD — ZeroPaddedDivergence
// Pad to length L = max(#a, #w) with zeros. If padded sequences agree
// everywhere, zpd is undefined (encoded as 0). Otherwise, zpd(a, w) is
// the smallest k ∈ {1,...,L} with aₖ ≠ wₖ on the padded sequences.
include "./CarrierSetDefinition.dfy"
include "./Divergence.dfy"

module ZeroPaddedDivergence {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import Divergence

  function PaddedComponent(a: Tumbler, i: nat): Carrier
    requires InT(a)
    requires 1 <= i
  {
    if i <= Length(a) then Component(a, i) else 0
  }

  function FirstPaddedMismatch(a: Tumbler, w: Tumbler, start: nat, L: nat): nat
    requires InT(a) && InT(w)
    requires 1 <= start <= L + 1
    ensures start <= FirstPaddedMismatch(a, w, start, L) <= L + 1
    ensures FirstPaddedMismatch(a, w, start, L) <= L ==>
      PaddedComponent(a, FirstPaddedMismatch(a, w, start, L)) !=
      PaddedComponent(w, FirstPaddedMismatch(a, w, start, L))
    ensures forall i :: start <= i < FirstPaddedMismatch(a, w, start, L) ==>
      PaddedComponent(a, i) == PaddedComponent(w, i)
    decreases L + 1 - start
  {
    if start > L then L + 1
    else if PaddedComponent(a, start) != PaddedComponent(w, start) then start
    else FirstPaddedMismatch(a, w, start + 1, L)
  }

  lemma FirstPaddedMismatchSymmetric(a: Tumbler, w: Tumbler, start: nat, L: nat)
    requires InT(a) && InT(w)
    requires 1 <= start <= L + 1
    ensures FirstPaddedMismatch(a, w, start, L) == FirstPaddedMismatch(w, a, start, L)
    decreases L + 1 - start
  {
    if start > L {
    } else if PaddedComponent(a, start) != PaddedComponent(w, start) {
    } else {
      FirstPaddedMismatchSymmetric(a, w, start + 1, L);
    }
  }

  // zpd(a, w): partial function. Returns 0 when undefined (zero-padded-equal),
  // otherwise returns the first index 1..L where padded components disagree.
  function ZeroPaddedDivergence(a: Tumbler, w: Tumbler): nat
    requires InT(a) && InT(w)
    ensures var L := if Length(a) >= Length(w) then Length(a) else Length(w);
      ZeroPaddedDivergence(a, w) == 0 ||
      (1 <= ZeroPaddedDivergence(a, w) <= L)
  {
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var k := FirstPaddedMismatch(a, w, 1, L);
    if k == L + 1 then 0
    else k
  }

  // Symmetry: zpd(a, w) = zpd(w, a) for all a, w ∈ T.
  // Dafny disallows this as a self-referential ensures on ZeroPaddedDivergence
  // (the postcondition's swapped call has no strictly-decreasing measure),
  // so the contractual guarantee is encoded as this companion lemma.
  // Under the 0-encoding for undefined, joint-definedness equivalence collapses
  // to plain equality.
  lemma ZeroPaddedDivergenceSymmetric(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    ensures ZeroPaddedDivergence(a, w) == ZeroPaddedDivergence(w, a)
  {
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lswap := if Length(w) >= Length(a) then Length(w) else Length(a);
    assert L == Lswap;
    FirstPaddedMismatchSymmetric(a, w, 1, L);
  }
}
