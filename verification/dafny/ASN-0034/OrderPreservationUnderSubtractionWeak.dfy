// ASN-0034: TA3 — OrderPreservationUnderSubtractionWeak
// (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./CanonicalRepresentation.dfy"
include "./PositiveTumbler.dfy"
include "./PositiveDominatesZero.dfy"
include "./TumblerSub.dfy"
include "./WellDefinedSubtraction.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./Divergence.dfy"
include "./IntrinsicComparison.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatZeroMinimum.dfy"
include "./NatDiscreteness.dfy"
include "./NatPartialSubtraction.dfy"
include "./NatArithmeticClosureAndIdentity.dfy"

module OrderPreservationUnderSubtractionWeak {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened CanonicalRepresentation
  import opened PositiveTumbler
  import opened PositiveDominatesZero
  import opened TumblerSub
  import opened WellDefinedSubtraction
  import opened ZeroPaddedDivergence
  import Divergence
  import IC = IntrinsicComparison
  import opened NatStrictTotalOrder
  import NZM = NatZeroMinimum
  import opened NatDiscreteness
  import opened NatPartialSubtraction
  import opened NatArithmeticClosureAndIdentity
  import opened NatCarrierSet

  // Helper: LexicographicOrder(a, b) implies a != b.
  lemma LexImpliesNotEqual(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures a != b
  {
    if a == b {
      var kw :| 1 <= kw
                && (forall i :: 1 <= i < kw ==>
                      i <= Length(a) && i <= Length(b) &&
                      Component(a, i) == Component(b, i))
                && ((kw <= Length(a) && kw <= Length(b)
                     && Less(Component(a, kw), Component(b, kw)))
                    || (kw == Length(a) + 1 && kw <= Length(b)));
      if kw <= Length(a) && kw <= Length(b)
         && Less(Component(a, kw), Component(b, kw)) {
        Irreflexive(Component(a, kw));
      }
    }
  }

  // Helper: in T1 case (i), the lex witness is Divergence(a, b).
  lemma DivergenceCaseIStrict(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    ensures var k := Divergence.Divergence(a, b);
            1 <= k &&
            (forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i)) &&
            Less(Component(a, k), Component(b, k))
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    var k := Divergence.Divergence(a, b);
    assert k == Divergence.FirstMismatch(a, b, 1, m);
    assert k <= m;
    assert Component(a, k) != Component(b, k);
    var kp :| 1 <= kp
              && (forall i :: 1 <= i < kp ==>
                    i <= Length(a) && i <= Length(b) &&
                    Component(a, i) == Component(b, i))
              && ((kp <= Length(a) && kp <= Length(b)
                   && Less(Component(a, kp), Component(b, kp)))
                  || (kp == Length(a) + 1 && kp <= Length(b)));
    if kp < k {
      assert Component(a, kp) == Component(b, kp);
      if kp <= Length(a) && kp <= Length(b)
         && Less(Component(a, kp), Component(b, kp)) {
        Irreflexive(Component(a, kp));
      }
    } else if kp > k {
      assert 1 <= k < kp;
      assert Component(a, k) == Component(b, k);
    }
    assert kp == k;
    if kp == Length(a) + 1 && kp <= Length(b) {
      assert k > Length(a);
      assert k <= Length(a);
      assert false;
    }
  }

  // Helper: in T1 case (ii), #a < #b and a prefixes b.
  // Avoids :| extraction; uses ShorterPrefix to rule out #b < #a and Extensionality
  // to rule out #a == #b.
  lemma PrefixCaseExtraction(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires a != b
    requires Divergence.Divergence(a, b) > Length(a) ||
             Divergence.Divergence(a, b) > Length(b)
    ensures Length(a) < Length(b)
    ensures forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    var d := Divergence.Divergence(a, b);
    assert d == Divergence.FirstMismatch(a, b, 1, m);
    // FirstMismatch <= m + 1, and precondition forces d > m.
    assert d > m by {
      if Divergence.Divergence(a, b) > Length(a) {
        assert d > Length(a) >= m;
      } else {
        assert d > Length(b) >= m;
      }
    }
    assert d <= m + 1;
    assert d == m + 1;
    // Pre-d agreement gives agreement on [1, m].
    assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);

    if Length(a) == Length(b) {
      assert m == Length(a) == Length(b);
      Extensionality(a, b);
      assert false;
    } else if Length(b) < Length(a) {
      assert m == Length(b);
      IC.ShorterPrefix(b, a);
      assert false;
    }
    assert Length(a) < Length(b);
    assert m == Length(a);
  }

  // Helper: TumblerSub yields a tumbler with the SubComponent characterisation
  // for every result position. This bridges the function body's internal
  // assertions to lemmas reasoning about result components.
  lemma TumblerSubComponentChar(a: Tumbler, w: Tumbler, i: nat)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires 1 <= i <= Length(TumblerSub.TumblerSub(a, w))
    ensures Component(TumblerSub.TumblerSub(a, w), i)
            == TumblerSub.SubComponent(
                 a, w, ZeroPaddedDivergence.ZeroPaddedDivergence(a, w), i)
  { }

  // Body of the weak order preservation proof.
  lemma OrderPreservationUnderSubtractionWeak(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    LexImpliesNotEqual(a, b);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var d := Divergence.Divergence(a, b);

    if d <= Length(a) && d <= Length(b) {
      // === Component divergence: a_d < b_d, agreement before d.
      DivergenceCaseIStrict(a, b);
      ComponentDivergenceCase(a, b, w);
    } else {
      // === Prefix case: a is a proper prefix of b.
      PrefixCaseExtraction(a, b);
      PrefixCase(a, b, w);
    }
  }

  // Case B (component divergence): a < b via T1 case (i).
  lemma ComponentDivergenceCase(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    var d := Divergence.Divergence(a, b);

    // From DivergenceCaseIStrict: d <= #a, d <= #b, a_d < b_d.
    assert forall i :: 1 <= i < d ==> Component(a, i) == Component(b, i);
    assert Less(Component(a, d), Component(b, d));

    // Derive bounds on ka and kb.
    assert ka == 0 || 1 <= ka <= La;
    assert kb == 0 || 1 <= kb <= Lb;

    // If ka != 0, ka <= #a; if kb != 0, kb <= #b.
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);

    // Case B1: ka = 0 (a is zero-padded-equal to w).
    if ka == 0 {
      // a ⊖ w is the zero tumbler of length La.
      assert PositiveTumbler.ZeroTumbler(ra);
      // We need kb != 0 to use TA-PosDom.
      KbDefinedFromDivergence(a, b, w);
      assert kb != 0;
      assert PositiveTumbler.PositiveTumbler(rb);
      PositiveDominatesZero.PositiveDominatesZero(rb, ra);
    } else if kb == 0 {
      // Contradiction: kb = 0 means b zero-padded-equal to w,
      // but component divergence and b ≥ w forces kb != 0.
      KbDefinedFromDivergence(a, b, w);
      assert false;
    } else {
      // ka != 0 and kb != 0.
      assert 1 <= ka <= Length(a);
      assert 1 <= kb <= Length(b);
      // Both ra and rb are positive.
      assert PositiveTumbler.PositiveTumbler(ra);
      assert PositiveTumbler.PositiveTumbler(rb);

      Trichotomy(ka, kb);
      if ka == kb {
        EqualZpdCase(a, b, w);
      } else if ka < kb {
        SmallerKaCase(a, b, w);
      } else {
        LargerKaCase(a, b, w);
      }
    }
  }

  // Helper: ka != 0 ⟹ ka <= #a.
  lemma KaBoundedByLength(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
            k == 0 || k <= Length(a)
  {
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    if k == 0 {
    } else {
      assert 1 <= k <= L;
      // Touch TumblerSub to expose its postcondition.
      var r := TumblerSub.TumblerSub(a, w);
      assert PaddedComponent(a, k) > PaddedComponent(w, k);
      if k > Length(a) {
        assert PaddedComponent(a, k) == 0;
        NZM.NatZeroMinimum(PaddedComponent(w, k));
        assert false;
      }
    }
  }

  // Helper: in component divergence case under w ≤ b, kb != 0.
  // Needs w ≤ a precondition to discharge the contradiction.
  lemma KbDefinedFromDivergence(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
  {
    DivergenceCaseIStrict(a, b);
    var d := Divergence.Divergence(a, b);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert d <= Length(b);
    assert d <= Lb;

    if ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) == 0 {
      ZpdZeroImpliesPaddedEqual(b, w);
      assert PaddedComponent(b, d) == PaddedComponent(w, d);
      assert PaddedComponent(b, d) == Component(b, d);
      if d <= Length(w) {
        // b_d = w_d. Combined with a_d < b_d, get a_d < w_d.
        // Also a_i = b_i = w_i for i < d. So a < w via T1 case (i),
        // contradicting w <= a.
        assert PaddedComponent(w, d) == Component(w, d);
        assert Component(b, d) == Component(w, d);
        // For i < d: agreement.
        forall i | 1 <= i < d
          ensures Component(a, i) == Component(w, i)
        {
          assert Component(a, i) == Component(b, i);
          assert i <= Lb;
          assert i <= Length(b);
          assert PaddedComponent(b, i) == Component(b, i);
          assert PaddedComponent(b, i) == PaddedComponent(w, i);
          assert i <= Length(w);
          assert PaddedComponent(w, i) == Component(w, i);
        }
        // Build LexOrder(a, w) witness at d.
        ConstructLessFromDivergence(a, w, d);
        // Contradict w <= a.
        LexImpliesNotEqual(w, a);
        LexAsymmetric(a, w);
      } else {
        // d > #w. ŵ_d = 0. b_d = 0. a_d < 0 contradicts nat.
        assert Length(w) < d;
        assert PaddedComponent(w, d) == 0;
        assert Component(b, d) == 0;
        NZM.NatZeroMinimum(Component(a, d));
        assert Component(a, d) < Component(b, d);
        assert Component(a, d) < 0;
        assert false;
      }
    }
  }

  // Helper: LexOrder is asymmetric.
  lemma LexAsymmetric(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(b, a) || b == a
    ensures false
  {
    if b == a {
      LexImpliesNotEqual(a, b);
    } else {
      // Use IntrinsicComparison's structure: Compare(a, b) = LT and GT — impossible.
      IC.IntrinsicComparison(a, b);
    }
  }

  // Helper: zpd = 0 implies padded equality everywhere on [1, L].
  lemma ZpdZeroImpliesPaddedEqual(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) == 0
    ensures var L := if Length(a) >= Length(w) then Length(a) else Length(w);
            forall i :: 1 <= i <= L ==> PaddedComponent(a, i) == PaddedComponent(w, i)
  {
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var fpm := FirstPaddedMismatch(a, w, 1, L);
    assert fpm == L + 1;
  }

  // Helper: construct LexOrder witness via T1 case (i).
  lemma ConstructLessFromDivergence(a: Tumbler, b: Tumbler, k: nat)
    requires InT(a) && InT(b)
    requires 1 <= k <= Length(a) && k <= Length(b)
    requires forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i)
    requires Less(Component(a, k), Component(b, k))
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    ghost var w: nat := k;
    assert 1 <= w
        && (forall i :: 1 <= i < w ==>
              i <= Length(a) && i <= Length(b) &&
              Component(a, i) == Component(b, i))
        && (w <= Length(a) && w <= Length(b)
            && Less(Component(a, w), Component(b, w)));
  }

  // Case B2: ka = kb = k. Both subtractions diverge at same position.
  lemma EqualZpdCase(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    // Touch TumblerSub to expose its postconditions.
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var d := Divergence.Divergence(a, b);
    assert 1 <= k <= Length(a);
    assert 1 <= k <= Length(b);
    assert PaddedComponent(a, k) > PaddedComponent(w, k);
    assert PaddedComponent(b, k) > PaddedComponent(w, k);
    assert PaddedComponent(a, k) == Component(a, k);
    assert PaddedComponent(b, k) == Component(b, k);

    // Lift ZPD's pre-divergence agreements to native: a_i = b_i for i < k.
    forall i | 1 <= i < k
      ensures Component(a, i) == Component(b, i)
    {
      assert i < k <= Length(a);
      assert i < k <= Length(b);
      assert Component(a, i) == PaddedComponent(a, i);
      assert PaddedComponent(b, i) == Component(b, i);
    }

    // d >= k: if d < k, then a_d = b_d (from pre-k agreement), but a_d < b_d.
    if d < k {
      assert Component(a, d) == Component(b, d);
      Irreflexive(Component(a, d));
      assert false;
    }
    assert d >= k;

    if d == k {
      EqualZpdSubcaseDEqualsK(a, b, w);
    } else {
      assert d > k;
      EqualZpdSubcaseDGreaterThanK(a, b, w);
    }
  }

  // Sub-case d == k: ra_k < rb_k via NAT-sub monotonicity.
  lemma EqualZpdSubcaseDEqualsK(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    requires Divergence.Divergence(a, b)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    assert k <= Length(a) && k <= Length(b);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);

    assert PaddedComponent(a, k) > PaddedComponent(w, k);
    assert PaddedComponent(b, k) > PaddedComponent(w, k);
    assert k <= La && k <= Lb;
    TumblerSubComponentChar(a, w, k);
    TumblerSubComponentChar(b, w, k);

    // For i < k, result components are 0.
    forall i | 1 <= i < k
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      assert i <= La;
      assert i <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
    }

    // At k: ra_k = a_k - w_k, rb_k = b_k - w_k, a_k < b_k.
    assert Component(a, k) < Component(b, k);
    var av := PaddedComponent(a, k);
    var bv := PaddedComponent(b, k);
    var wv := PaddedComponent(w, k);
    assert av < bv;
    assert av >= wv;
    assert bv >= wv;
    assert TumblerSub.SatSub(av, wv) == av - wv;
    assert TumblerSub.SatSub(bv, wv) == bv - wv;
    assert av - wv < bv - wv;
    assert Component(ra, k) == av - wv;
    assert Component(rb, k) == bv - wv;
    assert Less(Component(ra, k), Component(rb, k));

    ConstructLessFromDivergence(ra, rb, k);
  }

  // Sub-case d > k: results agree at k (both = a_k - w_k = b_k - w_k since
  // a_k = b_k from pre-d agreement), then disagree at d.
  lemma EqualZpdSubcaseDGreaterThanK(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    requires Divergence.Divergence(a, b)
             > ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var d := Divergence.Divergence(a, b);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert k <= Length(a) && k <= Length(b);
    assert d <= Length(a) && d <= Length(b);
    assert k < d;

    // Pre-d agreement gives a_k = b_k.
    assert Component(a, k) == Component(b, k);

    forall i | 1 <= i < k
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
    }

    TumblerSubComponentChar(a, w, k);
    TumblerSubComponentChar(b, w, k);
    assert Component(ra, k) == Component(rb, k);

    forall i | k < i < d
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      assert i < d <= Length(a);
      assert i < d <= Length(b);
      assert i <= La && i <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
      assert PaddedComponent(a, i) == Component(a, i);
      assert PaddedComponent(b, i) == Component(b, i);
    }

    TumblerSubComponentChar(a, w, d);
    TumblerSubComponentChar(b, w, d);
    assert d > k;
    assert Component(ra, d) == PaddedComponent(a, d);
    assert Component(rb, d) == PaddedComponent(b, d);
    assert PaddedComponent(a, d) == Component(a, d);
    assert PaddedComponent(b, d) == Component(b, d);
    assert Less(Component(a, d), Component(b, d));
    assert Less(Component(ra, d), Component(rb, d));

    assert d <= Length(ra) && d <= Length(rb);
    forall i | 1 <= i < d
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    { }
    ConstructLessFromDivergence(ra, rb, d);
  }

  // Case ka < kb: impossible.
  lemma SmallerKaCase(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             < ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    // Touch TumblerSub to expose its postconditions.
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var d := Divergence.Divergence(a, b);
    assert ka <= Length(a) && kb <= Length(b);
    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka < kb <= Lb;
    assert PaddedComponent(b, ka) == PaddedComponent(w, ka);
    assert PaddedComponent(a, ka) == Component(a, ka);
    assert ka <= Length(b);
    assert PaddedComponent(b, ka) == Component(b, ka);
    assert Component(a, ka) > Component(b, ka);

    forall i | 1 <= i < ka
      ensures Component(a, i) == Component(b, i)
    {
      assert i < ka <= Length(a);
      assert i < ka <= Length(b);
      assert PaddedComponent(a, i) == PaddedComponent(w, i);
      assert PaddedComponent(b, i) == PaddedComponent(w, i);
    }
    // a_ka > b_ka and pre-ka agreement: Divergence(a, b) = ka, b < a, contradicting a < b.
    assert d == ka by {
      assert d <= ka by {
        if d > ka {
          assert Component(a, ka) == Component(b, ka);
          assert false;
        }
      }
      if d < ka {
        assert Component(a, d) == Component(b, d);
        DivergenceCaseIStrict(a, b);
        Irreflexive(Component(a, d));
        assert false;
      }
    }
    DivergenceCaseIStrict(a, b);
    assert Component(a, d) < Component(b, d);
    Asymmetric(Component(a, d), Component(b, d));
    assert false;
  }

  // Case ka > kb: ra_kb = 0, rb_kb > 0.
  lemma LargerKaCase(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Divergence.Divergence(a, b) <= Length(b)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             > ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    DivergenceCaseIStrict(a, b);
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert kb < ka <= Length(a);
    assert kb <= Length(b);

    forall i | 1 <= i < kb
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      assert i <= La;
      assert i <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
    }

    assert PaddedComponent(b, kb) > PaddedComponent(w, kb);
    TumblerSubComponentChar(a, w, kb);
    TumblerSubComponentChar(b, w, kb);
    assert kb < ka;
    assert Component(ra, kb) == 0;
    var bv := PaddedComponent(b, kb);
    var wv := PaddedComponent(w, kb);
    assert bv > wv;
    assert TumblerSub.SatSub(bv, wv) == bv - wv;
    assert Component(rb, kb) == bv - wv;
    assert bv - wv > 0;
    assert Less(Component(ra, kb), Component(rb, kb));
    assert kb <= Length(ra) && kb <= Length(rb);

    ConstructLessFromDivergence(ra, rb, kb);
  }

  // Case A (prefix): #a < #b, a_i = b_i for 1 <= i <= #a.
  lemma PrefixCase(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert Lb >= La by {
      if Length(w) <= Length(a) {
        assert La == Length(a);
        assert Lb >= Length(b) > Length(a) == La;
      } else if Length(w) <= Length(b) {
        assert La == Length(w);
        assert Lb == Length(b);
      } else {
        assert La == Length(w);
        assert Lb == Length(w);
      }
    }

    if ka == 0 && kb == 0 {
      assert PositiveTumbler.ZeroTumbler(ra);
      assert PositiveTumbler.ZeroTumbler(rb);
      if La < Lb {
        forall i | 1 <= i <= La
          ensures i <= Length(rb) && Component(ra, i) == Component(rb, i)
        {
          assert Component(ra, i) == 0;
          assert Component(rb, i) == 0;
        }
        IC.LexOrderShorterWitness(ra, rb);
      } else {
        assert La == Lb;
        forall i | 1 <= i <= La
          ensures Component(ra, i) == Component(rb, i)
        {
          assert Component(ra, i) == 0;
          assert Component(rb, i) == 0;
        }
        Extensionality(ra, rb);
      }
    } else if ka == 0 && kb != 0 {
      PositiveDominatesZero.PositiveDominatesZero(rb, ra);
    } else if ka != 0 && kb == 0 {
      KbZeroImpossibleInPrefix(a, b, w);
      assert false;
    } else {
      assert ka != 0 && kb != 0;
      PrefixSubcaseBothPositive(a, b, w);
    }
  }

  // In prefix case, if ka != 0 then kb != 0.
  lemma KbZeroImpossibleInPrefix(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
  {
    KaBoundedByLength(a, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka <= Length(a);
    var ra := TumblerSub.TumblerSub(a, w);
    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    assert PaddedComponent(a, ka) == Component(a, ka);
    assert ka <= Length(a);
    assert Component(a, ka) == Component(b, ka);
    assert PaddedComponent(b, ka) == Component(b, ka);
    assert PaddedComponent(b, ka) != PaddedComponent(w, ka);
    assert 1 <= ka <= Lb by {
      assert Lb >= Length(b) >= Length(a) >= ka;
    }
    if ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) == 0 {
      ZpdZeroImpliesPaddedEqual(b, w);
      assert PaddedComponent(b, ka) == PaddedComponent(w, ka);
      assert false;
    }
  }

  // In prefix case, both ka != 0 and kb != 0.
  lemma PrefixSubcaseBothPositive(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka <= Length(a);
    assert 1 <= kb <= Length(b);

    PrefixKbGEKa(a, b, w);
    assert kb >= ka;

    if kb == ka {
      PrefixCaseEqualK(a, b, w);
    } else {
      PrefixCaseKbGreater(a, b, w);
      assert false;
    }
  }

  // In prefix case with ka != 0, kb >= ka.
  lemma PrefixKbGEKa(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
            >= ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka <= Length(a);
    assert 1 <= kb <= Length(b);

    forall i | 1 <= i < ka
      ensures PaddedComponent(b, i) == PaddedComponent(w, i)
    {
      assert i < ka <= Length(a);
      assert Component(a, i) == Component(b, i);
      assert PaddedComponent(a, i) == Component(a, i);
      assert i <= Length(b);
      assert PaddedComponent(b, i) == Component(b, i);
      assert PaddedComponent(a, i) == PaddedComponent(w, i);
    }
    if kb < ka {
      assert 1 <= kb < ka;
      assert PaddedComponent(b, kb) == PaddedComponent(w, kb);
      assert PaddedComponent(b, kb) != PaddedComponent(w, kb);
      assert false;
    }
  }

  // Helper: find first disagreement position in [start, L].
  function FirstResultDisagreement(
      ra: Tumbler, rb: Tumbler, start: nat, L: nat): nat
    requires InT(ra) && InT(rb)
    requires L <= Length(ra) && L <= Length(rb)
    requires 1 <= start <= L + 1
    ensures start <= FirstResultDisagreement(ra, rb, start, L) <= L + 1
    ensures FirstResultDisagreement(ra, rb, start, L) <= L ==>
            Component(ra, FirstResultDisagreement(ra, rb, start, L))
              != Component(rb, FirstResultDisagreement(ra, rb, start, L))
    ensures forall i :: start <= i < FirstResultDisagreement(ra, rb, start, L) ==>
            Component(ra, i) == Component(rb, i)
    decreases L + 1 - start
  {
    if start > L then L + 1
    else if Component(ra, start) != Component(rb, start) then start
    else FirstResultDisagreement(ra, rb, start + 1, L)
  }

  // Prefix case with kb == ka == k.
  lemma PrefixCaseEqualK(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= k <= Length(a);
    assert k <= Length(b);

    assert La <= Lb by {
      if Length(w) <= Length(a) {
        assert La == Length(a) < Length(b) <= Lb;
      } else if Length(w) <= Length(b) {
        assert La == Length(w);
        assert Lb == Length(b);
        assert La <= Length(b) == Lb;
      } else {
        assert La == Length(w) == Lb;
      }
    }
    assert Length(ra) == La && Length(rb) == Lb;
    assert La <= Length(ra) && La <= Length(rb);

    // ra and rb agree on positions [1, #a].
    forall i | 1 <= i <= Length(a)
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      assert i <= La;  // since Length(a) <= La (La = max(#a, #w))
      assert i <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
      if i < k {
        // both 0
      } else if i == k {
        assert k <= Length(a);
        assert Component(a, k) == Component(b, k);
        assert PaddedComponent(a, k) == Component(a, k);
        assert PaddedComponent(b, k) == Component(b, k);
      } else {
        // i > k. SubComponent = PaddedComponent at i.
        assert PaddedComponent(a, i) == Component(a, i);
        assert i <= Length(b);
        assert PaddedComponent(b, i) == Component(b, i);
        assert Component(a, i) == Component(b, i);
      }
    }

    // Scan from #a + 1 to La for the first disagreement.
    if Length(a) < La {
      // La > #a, so La = #w. For #a < i <= La, ra_i = â_i = 0.
      // rb_i = b̂_i which depends on whether i <= #b.
      forall i | Length(a) < i <= La
        ensures Component(ra, i) == 0
      {
        assert La == Length(w);
        TumblerSubComponentChar(a, w, i);
        assert i > k;
        assert PaddedComponent(a, i) == 0;
      }
      PrefixCaseEqualKScan(a, b, w);
    } else {
      // La == #a. Then ra and rb agree on [1, La].
      assert La == Length(a);
      assert La <= Lb;
      if La == Lb {
        Extensionality(ra, rb);
      } else {
        assert La < Lb;
        IC.LexOrderShorterWitness(ra, rb);
      }
    }
  }

  // Sub-lemma: when La > #a in prefix case, scan for first disagreement.
  lemma PrefixCaseEqualKScan(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
             == ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
    requires Length(a) < (if Length(a) >= Length(w) then Length(a) else Length(w))
    ensures
      var ra := TumblerSub.TumblerSub(a, w);
      var rb := TumblerSub.TumblerSub(b, w);
      LexicographicOrder.LexicographicOrder(ra, rb) || ra == rb
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert La == Length(w);
    assert Length(a) < Length(w);
    assert La <= Lb by {
      if Length(w) <= Length(b) {
        assert Lb == Length(b);
        assert La == Length(w) <= Length(b);
      } else {
        assert Lb == Length(w) == La;
      }
    }
    assert La <= Length(ra) && La <= Length(rb);

    // For #a < i <= La, ra_i = 0.
    // We need to find the first p in [#a+1, La] with ra_p != rb_p (i.e., rb_p != 0).
    var p := FirstResultDisagreement(ra, rb, Length(a) + 1, La);
    if p <= La {
      // Found a disagreement at p ∈ [#a + 1, La].
      // ra_p = 0, rb_p != 0.
      TumblerSubComponentChar(a, w, p);
      assert p > Length(a);
      assert p > k by { assert k <= Length(a); }
      assert PaddedComponent(a, p) == 0;
      assert Component(ra, p) == 0;
      assert Component(ra, p) != Component(rb, p);
      assert Component(rb, p) != 0;
      // Also TumblerSubComponentChar gives rb_p = either SatSub(b̂_p, ŵ_p)
      // (if p == k, but p > k here) or b̂_p (if p > k). So rb_p = b̂_p.
      TumblerSubComponentChar(b, w, p);
      assert Component(rb, p) == PaddedComponent(b, p);
      NZM.NatZeroMinimum(Component(ra, p));
      // Component(ra, p) = 0 < Component(rb, p), since rb_p != 0 and rb_p >= 0.
      assert Component(rb, p) > 0;
      assert Less(Component(ra, p), Component(rb, p));

      // Agreement on [1, #a]: established by PrefixCaseEqualK; replay here.
      forall i | 1 <= i <= Length(a)
        ensures Component(ra, i) == Component(rb, i)
      {
        assert i <= La;
        assert i <= Lb;
        TumblerSubComponentChar(a, w, i);
        TumblerSubComponentChar(b, w, i);
        if i < k {
        } else if i == k {
          assert Component(a, k) == Component(b, k);
          assert PaddedComponent(a, k) == Component(a, k);
          assert PaddedComponent(b, k) == Component(b, k);
        } else {
          assert PaddedComponent(a, i) == Component(a, i);
          assert i <= Length(b);
          assert PaddedComponent(b, i) == Component(b, i);
          assert Component(a, i) == Component(b, i);
        }
      }
      // Agreement on [#a + 1, p - 1] from FirstResultDisagreement.
      assert forall i :: Length(a) + 1 <= i < p ==>
        Component(ra, i) == Component(rb, i);
      assert forall i :: 1 <= i < p ==>
        i <= Length(ra) && i <= Length(rb) &&
        Component(ra, i) == Component(rb, i);
      ConstructLessFromDivergence(ra, rb, p);
    } else {
      // No disagreement in [#a + 1, La]. ra and rb agree on [1, La].
      assert p == La + 1;
      // Agreement on [1, #a] (replayed).
      forall i | 1 <= i <= Length(a)
        ensures Component(ra, i) == Component(rb, i)
      {
        assert i <= La;
        assert i <= Lb;
        TumblerSubComponentChar(a, w, i);
        TumblerSubComponentChar(b, w, i);
        if i < k {
        } else if i == k {
          assert Component(a, k) == Component(b, k);
        } else {
          assert PaddedComponent(a, i) == Component(a, i);
          assert i <= Length(b);
          assert PaddedComponent(b, i) == Component(b, i);
          assert Component(a, i) == Component(b, i);
        }
      }
      // Agreement on [#a + 1, La] from FirstResultDisagreement.
      assert forall i :: Length(a) + 1 <= i <= La ==>
        Component(ra, i) == Component(rb, i);
      // Combined: agreement on [1, La].
      if La == Lb {
        forall i | 1 <= i <= La
          ensures Component(ra, i) == Component(rb, i)
        { }
        Extensionality(ra, rb);
      } else {
        assert La < Lb;
        forall i | 1 <= i <= La
          ensures Component(ra, i) == Component(rb, i)
        { }
        IC.LexOrderShorterWitness(ra, rb);
      }
    }
  }

  // Prefix case with kb > ka. Impossible.
  lemma PrefixCaseKbGreater(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires a != b
    requires Length(a) < Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w) != 0
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(b, w)
             > ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)
    ensures false
  {
    KaBoundedByLength(a, w);
    KaBoundedByLength(b, w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka <= Length(a);
    assert ka < kb <= Length(b);

    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    assert ka <= Length(a);
    assert Component(a, ka) == Component(b, ka);
    assert PaddedComponent(a, ka) == Component(a, ka);
    assert PaddedComponent(b, ka) == Component(b, ka);
    assert PaddedComponent(b, ka) > PaddedComponent(w, ka);
    assert PaddedComponent(b, ka) != PaddedComponent(w, ka);
    assert 1 <= ka < kb;
    assert PaddedComponent(b, ka) == PaddedComponent(w, ka);
    assert false;
  }
}
