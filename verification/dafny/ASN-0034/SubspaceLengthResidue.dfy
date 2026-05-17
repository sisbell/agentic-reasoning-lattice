// ASN-0034: TA7a.1 — SubspaceLengthResidue
// When the subtrahend is longer than the minuend, subtraction escapes S:
//   (A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w > #o ⟹ o ⊖ w ∈ T \ S).
// Witness: r_{#w} = 0 (zero-padding o places a zero at the trailing index).
include "./SubspaceClosure.dfy"
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./CanonicalRepresentation.dfy"
include "./PositiveTumbler.dfy"
include "./WellDefinedSubtraction.dfy"
include "./TumblerSub.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatZeroMinimum.dfy"

module SubspaceLengthResidue {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened LexicographicOrder
  import opened CanonicalRepresentation
  import opened PositiveTumbler
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened NatStrictTotalOrder
  import opened SubspaceClosure

  // o a proper component-prefix of w ⇒ strict order o < w with ¬(w < o).
  // Forward: case (ii) witness k = #o + 1. Reverse: case analysis on any
  // candidate witness — case (i) collides with agreement, case (ii) needs
  // #w + 1 ≤ #o, contradicting #o < #w.
  lemma ProperPrefixForcesLess(o: Tumbler, w: Tumbler)
    requires InT(o) && InT(w)
    requires Length(o) < Length(w)
    requires forall i :: 1 <= i <= Length(o) ==> Component(o, i) == Component(w, i)
    ensures LexicographicOrder.LexicographicOrder(o, w)
    ensures !LexicographicOrder.LexicographicOrder(w, o)
  {
    var kw: nat := Length(o) + 1;
    ghost var trig := Component(w, kw);
    assert 1 <= kw && kw == Length(o) + 1 && kw <= Length(w);
    assert forall i :: 1 <= i < kw ==>
      i <= Length(o) && i <= Length(w) && Component(o, i) == Component(w, i);

    if LexicographicOrder.LexicographicOrder(w, o) {
      var k' :| 1 <= k'
            && (forall i :: 1 <= i < k' ==>
                  i <= Length(w) && i <= Length(o) &&
                  Component(w, i) == Component(o, i))
            && ((k' <= Length(w) && k' <= Length(o) &&
                 Less(Component(w, k'), Component(o, k')))
                || (k' == Length(w) + 1 && k' <= Length(o)));
      if k' <= Length(w) && k' <= Length(o) {
        assert Component(o, k') == Component(w, k');
        Irreflexive(Component(o, k'));
      }
      // Case (ii) impossible: would need Length(w) + 1 ≤ Length(o) < Length(w).
    }
  }

  // TA7a.1: #w > #o forces r := o ⊖ w to carry a zero at index #w,
  // which violates S's universal positivity clause; r ∈ T from TA2.
  lemma SubspaceLengthResidue(o: Tumbler, w: Tumbler)
    requires InT(o) && InT(w)
    requires InSubspaceS(o)
    requires PositiveTumbler.PositiveTumbler(w)
    requires LexicographicOrder.LexicographicOrder(w, o) || w == o
    requires Length(w) > Length(o)
    ensures InT(TumblerSub.TumblerSub(o, w))
    ensures !InSubspaceS(TumblerSub.TumblerSub(o, w))
  {
    var r := TumblerSub.TumblerSub(o, w);
    var L := Length(w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(o, w);

    // w == o impossible since #w > #o.
    if w == o {
      assert Length(w) == Length(o);
      assert false;
    }
    assert LexicographicOrder.LexicographicOrder(w, o);

    TumblerSubComponents(o, w);
    var fpm := FirstPaddedMismatch(o, w, 1, L);

    // Rule out k == 0 and k > Length(o) by deriving o < w (contradicting o ≥ w).
    // In both cases padded components agree on [1, Length(o)], so o is a
    // proper prefix of w, forcing LexicographicOrder(o, w).
    if k == 0 || k > Length(o) {
      forall i | 1 <= i <= Length(o)
        ensures Component(o, i) == Component(w, i)
      {
        if k == 0 {
          assert fpm == L + 1;
          assert 1 <= i < L + 1;
        } else {
          assert fpm == k;
          assert 1 <= i < k;
        }
        assert PaddedComponent(o, i) == PaddedComponent(w, i);
        assert PaddedComponent(o, i) == Component(o, i);
        assert PaddedComponent(w, i) == Component(w, i);
      }
      ProperPrefixForcesLess(o, w);
      assert false;
    }

    // 1 ≤ k ≤ #o < #w, so SubComponent at index #w takes the else branch
    // and returns PaddedComponent(o, #w) = 0 (since #w > #o).
    assert 1 <= k <= Length(o) < Length(w);
    assert Component(r, Length(w)) == SubComponent(o, w, k, Length(w));
    assert SubComponent(o, w, k, Length(w)) == PaddedComponent(o, Length(w));
    assert PaddedComponent(o, Length(w)) == 0;
    assert Length(r) == L == Length(w);
    assert 1 <= Length(w) <= Length(r) && Component(r, Length(w)) == 0;
  }
}
