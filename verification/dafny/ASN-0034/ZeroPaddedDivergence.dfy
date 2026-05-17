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

  // On the shared-position range [start, m], padded components coincide with
  // native components, so the padded mismatch scan agrees with the native one.
  // When FirstMismatch returns a value <= m (Divergence case (i)),
  // FirstPaddedMismatch over [start, L] returns the same index.
  lemma FirstPaddedMismatchEqualsFirstMismatch(
      a: Tumbler, w: Tumbler, start: nat, m: nat, L: nat)
    requires InT(a) && InT(w)
    requires m <= Length(a) && m <= Length(w)
    requires L >= m
    requires 1 <= start <= m + 1
    requires Divergence.FirstMismatch(a, w, start, m) <= m
    ensures FirstPaddedMismatch(a, w, start, L) == Divergence.FirstMismatch(a, w, start, m)
    decreases m + 1 - start
  {
    if start > m {
      // FirstMismatch returns m+1 here, contradicting the precondition.
    } else if Component(a, start) != Component(w, start) {
      assert PaddedComponent(a, start) == Component(a, start);
      assert PaddedComponent(w, start) == Component(w, start);
    } else {
      FirstPaddedMismatchEqualsFirstMismatch(a, w, start + 1, m, L);
    }
  }

  // Relationship to Divergence — case (i): component divergence at shared
  // position k with k <= #a /\ k <= #w. The padded projections coincide with
  // the native projections through 1, ..., k, so zpd(a, w) = divergence(a, w).
  lemma ZeroPaddedDivergenceCaseI(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires a != w
    requires Divergence.Divergence(a, w) <= Length(a)
    requires Divergence.Divergence(a, w) <= Length(w)
    ensures ZeroPaddedDivergence(a, w) == Divergence.Divergence(a, w)
  {
    var m := if Length(a) <= Length(w) then Length(a) else Length(w);
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    assert Divergence.Divergence(a, w) == Divergence.FirstMismatch(a, w, 1, m);
    FirstPaddedMismatchEqualsFirstMismatch(a, w, 1, m, L);
  }

  // Advance the FirstPaddedMismatch scan past a prefix on which padded
  // components agree. Used to skip the shared-prefix range in Case (ii)
  // and to certify exhaustion when no trailing nonzero component exists.
  lemma FirstPaddedMismatchAdvance(
      a: Tumbler, w: Tumbler, start: nat, target: nat, L: nat)
    requires InT(a) && InT(w)
    requires 1 <= start <= target <= L + 1
    requires forall i :: start <= i < target ==> PaddedComponent(a, i) == PaddedComponent(w, i)
    ensures FirstPaddedMismatch(a, w, start, L) == FirstPaddedMismatch(a, w, target, L)
    decreases target - start
  {
    if start == target {
    } else {
      FirstPaddedMismatchAdvance(a, w, start + 1, target, L);
    }
  }

  // Relationship to Divergence — case (ii) sub-case (β): #a < #w with all
  // shared components agreeing. Divergence returns #a + 1. The padded scan
  // skips the agreeing prefix and inspects positions (#a, #w]: a's padded
  // entries are 0, w's are wᵢ. If some wᵢ != 0, zpd is defined and at least
  // #a + 1 = divergence; if all are 0, zpd is undefined (encoded 0).
  lemma ZeroPaddedDivergenceCaseIIBeta(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires a != w
    requires Length(a) < Length(w)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(w, i)
    ensures (exists i :: Length(a) < i <= Length(w) && Component(w, i) != 0)
              ==> (ZeroPaddedDivergence(a, w) != 0
                   && ZeroPaddedDivergence(a, w) >= Divergence.Divergence(a, w))
    ensures (forall i :: Length(a) < i <= Length(w) ==> Component(w, i) == 0)
              ==> ZeroPaddedDivergence(a, w) == 0
  {
    var L := Length(w);
    assert L == if Length(a) >= Length(w) then Length(a) else Length(w);

    assert forall i :: 1 <= i <= Length(a) ==>
      PaddedComponent(a, i) == PaddedComponent(w, i);
    FirstPaddedMismatchAdvance(a, w, 1, Length(a) + 1, L);

    if exists i :: Length(a) < i <= L && Component(w, i) != 0 {
      var wit :| Length(a) < wit <= L && Component(w, wit) != 0;
      assert PaddedComponent(a, wit) == 0;
      assert PaddedComponent(w, wit) == Component(w, wit);
      assert PaddedComponent(a, wit) != PaddedComponent(w, wit);
      var fpm := FirstPaddedMismatch(a, w, Length(a) + 1, L);
      // By FirstPaddedMismatch's postcondition, all positions in
      // [Length(a)+1, fpm) have matching padded components. The wit
      // disagrees and lies in [Length(a)+1, L], so fpm <= wit <= L.
      assert Length(a) + 1 <= wit;
      assert !(Length(a) + 1 <= wit < fpm);
      assert fpm <= wit;
    } else {
      assert forall i :: Length(a) < i <= L ==> Component(w, i) == 0;
      assert forall i :: Length(a) + 1 <= i <= L ==>
        PaddedComponent(a, i) == 0 && PaddedComponent(w, i) == 0;
      FirstPaddedMismatchAdvance(a, w, Length(a) + 1, L + 1, L);
    }
  }

  // Relationship to Divergence — case (ii) sub-case (γ): #w < #a, dual to (β).
  // Swap operands and reduce via ZeroPaddedDivergenceSymmetric and
  // Divergence.DivergenceSymmetric.
  lemma ZeroPaddedDivergenceCaseIIGamma(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires a != w
    requires Length(w) < Length(a)
    requires forall i :: 1 <= i <= Length(w) ==> Component(a, i) == Component(w, i)
    ensures (exists i :: Length(w) < i <= Length(a) && Component(a, i) != 0)
              ==> (ZeroPaddedDivergence(a, w) != 0
                   && ZeroPaddedDivergence(a, w) >= Divergence.Divergence(a, w))
    ensures (forall i :: Length(w) < i <= Length(a) ==> Component(a, i) == 0)
              ==> ZeroPaddedDivergence(a, w) == 0
  {
    ZeroPaddedDivergenceCaseIIBeta(w, a);
    ZeroPaddedDivergenceSymmetric(a, w);
    Divergence.DivergenceSymmetric(a, w);
  }
}
