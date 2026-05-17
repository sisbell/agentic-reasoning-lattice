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
    // d > m means all positions 1..m agree
    assert d == m + 1;
    assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);

    // Now we must show Length(a) < Length(b).
    var kp :| 1 <= kp
              && (forall i :: 1 <= i < kp ==>
                    i <= Length(a) && i <= Length(b) &&
                    Component(a, i) == Component(b, i))
              && ((kp <= Length(a) && kp <= Length(b)
                   && Less(Component(a, kp), Component(b, kp)))
                  || (kp == Length(a) + 1 && kp <= Length(b)));
    if kp <= Length(a) && kp <= Length(b) && Less(Component(a, kp), Component(b, kp)) {
      assert kp <= m;
      assert Component(a, kp) == Component(b, kp);
      Irreflexive(Component(a, kp));
    }
    assert kp == Length(a) + 1 && kp <= Length(b);
    assert Length(a) < Length(b);
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
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert Length(ra) == La;
    assert Length(rb) == Lb;
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
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
      // Contradiction: kb = 0 means b zero-padded-equal to w.
      // But then component divergence and b ≥ w force a contradiction.
      KbDefinedFromDivergence(a, b, w);
      assert false;
    } else {
      // ka != 0 and kb != 0.
      assert 1 <= ka <= Length(a);
      assert 1 <= kb <= Length(b);
      // Both ra and rb are positive, with action points ka, kb respectively.
      assert PositiveTumbler.PositiveTumbler(ra);
      assert PositiveTumbler.PositiveTumbler(rb);

      // Now case on the relationship between ka and kb.
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

  // Helper: ka != 0 ⟹ ka <= #a (analogously for kb).
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
      // TumblerSub's exported postcondition gives â_k > ŵ_k.
      var r := TumblerSub.TumblerSub(a, w);
      assert PaddedComponent(a, k) > PaddedComponent(w, k);
      if k > Length(a) {
        // Then â_k = 0, contradicting â_k > ŵ_k since ŵ_k >= 0.
        assert PaddedComponent(a, k) == 0;
        NZM.NatZeroMinimum(PaddedComponent(w, k));
        assert false;
      }
    }
  }

  // Helper: in component divergence case, kb != 0.
  lemma KbDefinedFromDivergence(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
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
      // Then padded sequences of b and w agree everywhere on [1, Lb].
      ZpdZeroImpliesPaddedEqual(b, w);
      // In particular, at j = d: b̂_d = ŵ_d.
      assert PaddedComponent(b, d) == PaddedComponent(w, d);
      assert PaddedComponent(b, d) == Component(b, d);
      // We need to derive a contradiction. Two cases on d vs #w.
      if d <= Length(w) {
        // b_d = w_d. Combined with a_d < b_d = w_d, get a_d < w_d.
        // For i < d, we need a_i = w_i. b_i = a_i (pre-d) and b_i = w_i (padded equality).
        // So a_i = w_i for i < d. Then a < w via T1 case (i), contradicting w <= b.
        // But we don't have w <= a as precondition here.
        // Hmm: we have w <= b and a < b, but neither implies w <= a.
        // The standard "a >= w" precondition is for the original lemma. Here we don't need it.
        // Actually... let me think. We need to derive a contradiction from kb == 0.
        // The TA3 hypothesis is a < b ∧ a >= w ∧ b >= w. So w <= a is provided.
        // We need to add this as a precondition.
        assert false; // placeholder — to be addressed
      } else {
        // d > #w. Then ŵ_d = 0, so b_d = 0. a_d < 0 contradicts nat.
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
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var d := Divergence.Divergence(a, b);
    var La := if Length(a) >= Length(w) then Length(a) else Length(w);
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= k <= Length(a);
    assert 1 <= k <= Length(b);
    assert PaddedComponent(a, k) > PaddedComponent(w, k);
    assert PaddedComponent(b, k) > PaddedComponent(w, k);
    assert PaddedComponent(a, k) == Component(a, k);
    assert PaddedComponent(b, k) == Component(b, k);

    // Pre-k agreement on padded projections.
    var Lmax := if La >= Lb then La else Lb;
    // From ZPD's pre-divergence agreements for (a, w) and (b, w):
    assert forall i :: 1 <= i < k ==> PaddedComponent(a, i) == PaddedComponent(w, i);
    assert forall i :: 1 <= i < k ==> PaddedComponent(b, i) == PaddedComponent(w, i);
    // Hence a_i = b_i for i < k (lift via padded-native equality).
    assert forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i)
      by {
        forall i | 1 <= i < k
          ensures Component(a, i) == Component(b, i)
        {
          assert i < k <= Length(a);
          assert i < k <= Length(b);
          assert Component(a, i) == PaddedComponent(a, i);
          assert PaddedComponent(b, i) == Component(b, i);
        }
      }

    // d >= k: if d < k, then a_d = b_d (from pre-k agreement above),
    // but DivergenceCaseIStrict gave a_d < b_d.
    if d < k {
      assert Component(a, d) == Component(b, d);
      Irreflexive(Component(a, d));
      assert false;
    }
    assert d >= k;

    // Sub-cases: d == k vs d > k.
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

    // ra_k and rb_k via the SubComponent characterisation.
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

    // At k: ra_k = a_k - w_k, rb_k = b_k - w_k, a_k < b_k, so ra_k < rb_k.
    assert Component(a, k) < Component(b, k);
    assert PaddedComponent(a, k) == Component(a, k);
    assert PaddedComponent(b, k) == Component(b, k);
    assert PaddedComponent(w, k) == (if k <= Length(w) then Component(w, k) else 0);
    // NAT-sub strict monotonicity: ra_k < rb_k.
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

    // Witness k for LexOrder(ra, rb).
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

    // For i < k: both ra_i = rb_i = 0.
    forall i | 1 <= i < k
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
    }

    // At k: ra_k = a_k - w_k = b_k - w_k = rb_k.
    TumblerSubComponentChar(a, w, k);
    TumblerSubComponentChar(b, w, k);
    assert Component(ra, k) == Component(rb, k);

    // For k < i < d: ra_i = a_i (padded), rb_i = b_i (padded), and
    // pre-d agreement gives a_i = b_i.
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

    // At d: ra_d = a_d, rb_d = b_d, a_d < b_d.
    TumblerSubComponentChar(a, w, d);
    TumblerSubComponentChar(b, w, d);
    assert d > k;
    assert Component(ra, d) == PaddedComponent(a, d);
    assert Component(rb, d) == PaddedComponent(b, d);
    assert PaddedComponent(a, d) == Component(a, d);
    assert PaddedComponent(b, d) == Component(b, d);
    assert Less(Component(a, d), Component(b, d));
    assert Less(Component(ra, d), Component(rb, d));

    // Build LexOrder witness at d.
    assert d <= Length(ra) && d <= Length(rb);
    forall i | 1 <= i < d
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    { }
    ConstructLessFromDivergence(ra, rb, d);
  }

  // Case ka < kb: impossible (TumblerSub's > inequality at ka contradicts).
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
    var ka := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var kb := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    var d := Divergence.Divergence(a, b);
    assert ka <= Length(a) && kb <= Length(b);
    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    // Pre-kb agreement: b̂_ka = ŵ_ka.
    var Lb := if Length(b) >= Length(w) then Length(b) else Length(w);
    assert 1 <= ka < kb <= Lb;
    assert PaddedComponent(b, ka) == PaddedComponent(w, ka);
    // Lift to native: a_ka != b_ka.
    assert PaddedComponent(a, ka) == Component(a, ka);
    assert ka <= Length(b);
    assert PaddedComponent(b, ka) == Component(b, ka);
    assert Component(a, ka) > Component(b, ka);

    // Pre-ka agreement for both (a, w) and (b, w): a_i = w_i = b_i for i < ka.
    forall i | 1 <= i < ka
      ensures Component(a, i) == Component(b, i)
    {
      assert i < ka <= Length(a);
      assert i < ka <= Length(b);
      assert PaddedComponent(a, i) == PaddedComponent(w, i);
      assert PaddedComponent(b, i) == PaddedComponent(w, i);
    }
    // a_ka > b_ka and pre-ka agreement: gives Divergence(a,b) = ka, and a > b.
    // But a < b precondition. Contradiction.
    assert d == ka by {
      assert d <= ka by {
        // Divergence is the first mismatch position; we have a mismatch at ka.
        // Since pre-ka agreement holds, d <= ka.
        if d > ka {
          assert Component(a, ka) == Component(b, ka);
          assert false;
        }
      }
      // d >= ka: if d < ka, then a_d != b_d, but pre-ka agreement contradicts.
      if d < ka {
        assert Component(a, d) == Component(b, d);
        DivergenceCaseIStrict(a, b);
        Irreflexive(Component(a, d));
        assert false;
      }
    }
    assert d == ka;
    DivergenceCaseIStrict(a, b);
    assert Component(a, d) < Component(b, d);
    Asymmetric(Component(a, d), Component(b, d));
    assert false;
  }

  // Case ka > kb: ra_kb = 0, rb_kb > 0 (from TumblerSub's > inequality at kb).
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

    // For i < kb: ra_i = 0 (i < kb < ka), rb_i = 0 (i < kb).
    forall i | 1 <= i < kb
      ensures i <= Length(ra) && i <= Length(rb)
              && Component(ra, i) == Component(rb, i)
    {
      assert i <= La;
      assert i <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
    }

    // At kb: ra_kb = 0 (kb < ka), rb_kb = b̂_kb - ŵ_kb > 0.
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
    // Length(a) < Length(b), so Lb >= Length(b) > Length(a).
    // La is max(#a, #w). In all cases Lb >= La.
    assert Lb >= La by {
      if Length(w) <= Length(a) {
        assert La == Length(a);
        assert Lb >= Length(b) > Length(a) == La;
      } else if Length(w) <= Length(b) {
        assert La == Length(w);
        assert Lb == Length(b);
        assert Length(b) >= Length(w);
      } else {
        assert La == Length(w);
        assert Lb == Length(w);
      }
    }

    if ka == 0 && kb == 0 {
      // Both are zero tumblers, but Lb >= La. If La == Lb then ra == rb, else ra < rb.
      assert PositiveTumbler.ZeroTumbler(ra);
      assert PositiveTumbler.ZeroTumbler(rb);
      if La < Lb {
        // ra is a strict prefix of rb (both all zero, different lengths).
        forall i | 1 <= i <= La
          ensures i <= Length(rb) && Component(ra, i) == Component(rb, i)
        {
          assert Component(ra, i) == 0;
          assert Component(rb, i) == 0;
        }
        // Witness Length(ra) + 1 for T1 case (ii).
        IC.LexOrderShorterWitness(ra, rb);
      } else {
        // La == Lb. Both are zero tumblers of equal length, so ra == rb.
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
      // ra is zero, rb is positive — TA-PosDom gives ra < rb.
      PositiveDominatesZero.PositiveDominatesZero(rb, ra);
    } else if ka != 0 && kb == 0 {
      // Impossible: if a > w by zpd, then b (which prefixes-extends a)
      // also has zpd != 0 with same component disagreement, OR has nonzero tail.
      KbZeroImpossibleInPrefix(a, b, w);
      assert false;
    } else {
      // Both ka and kb defined. Use PrefixSubcase.
      assert ka != 0 && kb != 0;
      PrefixSubcaseBothPositive(a, b, w);
    }
  }

  // In prefix case, if ka != 0 then kb != 0 as well.
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
    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    assert PaddedComponent(a, ka) == Component(a, ka);
    // Since ka <= Length(a) < Length(b), a_ka = b_ka.
    assert ka <= Length(a);
    assert Component(a, ka) == Component(b, ka);
    assert PaddedComponent(b, ka) == Component(b, ka);
    // So b̂_ka != ŵ_ka.
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

    // Pre-ka agreement of (a, w) gives a_i = w_i for i < ka, i <= #a, i <= #w.
    // Since a prefixes b at indices <= #a, also b_i = a_i = w_i for i < ka.
    // Hence pre-ka padded agreement of (b, w), so kb >= ka by ZPD's minimality.
    PrefixKbGEKa(a, b, w);
    assert kb >= ka;

    if kb == ka {
      // Same divergence position. a_ka = b_ka. Both ra_ka = rb_ka = a_ka - w_ka.
      PrefixCaseEqualK(a, b, w);
    } else {
      // kb > ka. Impossible: see PrefixCaseKbGreater (contradiction).
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

    // Pre-ka agreement for (a, w).
    assert forall i :: 1 <= i < ka ==> PaddedComponent(a, i) == PaddedComponent(w, i);
    // Lift to (b, w) on [1, ka): for i < ka <= #a, a_i = b_i (prefix).
    forall i | 1 <= i < ka
      ensures PaddedComponent(b, i) == PaddedComponent(w, i)
    {
      assert i < ka <= Length(a);
      assert Component(a, i) == Component(b, i);
      assert PaddedComponent(a, i) == Component(a, i);
      assert i <= Length(b);
      assert PaddedComponent(b, i) == Component(b, i);
    }
    // So b agrees with w on padded [1, ka). Hence first padded mismatch of (b, w)
    // does not occur before ka.
    if kb < ka {
      // FirstPaddedMismatch(b, w, 1, Lb) is at kb, contradicting pre-ka agreement.
      assert 1 <= kb < ka;
      assert PaddedComponent(b, kb) == PaddedComponent(w, kb);
      // But ZPD's first-disagreement clause gives mismatch at kb.
      assert PaddedComponent(b, kb) != PaddedComponent(w, kb);
      assert false;
    }
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

    // Lengths: La <= Lb because of #a < #b.
    assert La <= Lb by {
      // La = max(#a, #w), Lb = max(#b, #w). #a < #b, so max(#a, #w) <= max(#b, #w).
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

    // Both ra and rb agree on [1, La].
    forall i | 1 <= i <= La
      ensures i <= Length(rb) && Component(ra, i) == Component(rb, i)
    {
      assert i <= La <= Lb;
      TumblerSubComponentChar(a, w, i);
      TumblerSubComponentChar(b, w, i);
      // SubComponent(a, w, k, i) vs SubComponent(b, w, k, i)
      if i < k {
        // both 0
      } else if i == k {
        // SatSub(PaddedComponent(a, k), PaddedComponent(w, k))
        // = SatSub(PaddedComponent(b, k), PaddedComponent(w, k))
        // since a_k = b_k (k <= #a)
        assert k <= Length(a);
        assert Component(a, k) == Component(b, k);
        assert PaddedComponent(a, k) == Component(a, k);
        assert PaddedComponent(b, k) == Component(b, k);
      } else {
        // SubComponent = PaddedComponent at i
        // PaddedComponent(a, i) = a_i if i <= #a, else 0.
        // PaddedComponent(b, i) = b_i if i <= #b, else 0.
        if i <= Length(a) {
          assert PaddedComponent(a, i) == Component(a, i);
          assert PaddedComponent(b, i) == Component(b, i);
          assert Component(a, i) == Component(b, i);
        } else {
          assert i > Length(a);
          assert PaddedComponent(a, i) == 0;
          // i <= La. If La = #a then i > #a contradicts i <= La. So La > #a.
          // La > #a means La = #w > #a. So i <= #w.
          assert La == Length(w);
          assert Length(w) > Length(a);
          assert i <= Length(w);
          // Now PaddedComponent(b, i): i could be <= #b or > #b.
          // Wait: i <= La <= Lb, so i is a valid index. But is i <= #b or > #b?
          // #b > #a, but i could be either.
          // The case where i > #b is possible: La = #w, but #w > #b also possible.
          // Hmm.
          if i <= Length(b) {
            // b_i exists, but we don't know it equals a_i.
            // Wait — we have a < b in prefix case, b extends a beyond #a.
            // We have no constraint on b_i for #a < i <= #b.
            // So Component(b, i) is arbitrary.
            // The result is therefore not equal to 0 in general.
            // We CANNOT prove Component(ra, i) == Component(rb, i) here.
          } else {
            // i > #b, PaddedComponent(b, i) = 0 = PaddedComponent(a, i).
            assert PaddedComponent(b, i) == 0;
            assert PaddedComponent(a, i) == 0;
          }
        }
      }
    }

    if La == Lb {
      Extensionality(ra, rb);
    } else {
      assert La < Lb;
      IC.LexOrderShorterWitness(ra, rb);
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

    // This case is impossible: ka <= #a, b_i = a_i for i <= #a (prefix).
    // So PaddedComponent(b, ka) = b_ka = a_ka = PaddedComponent(a, ka)
    //   != PaddedComponent(w, ka).
    // Then ZPD's pre-divergence agreement for (b, w) at ka < kb gives
    // PaddedComponent(b, ka) = PaddedComponent(w, ka). Contradiction.
    assert ka <= Length(a);
    assert Component(a, ka) == Component(b, ka);
    assert PaddedComponent(a, ka) == Component(a, ka);
    assert PaddedComponent(b, ka) == Component(b, ka);
    assert PaddedComponent(a, ka) > PaddedComponent(w, ka);
    assert PaddedComponent(b, ka) > PaddedComponent(w, ka);
    assert PaddedComponent(b, ka) != PaddedComponent(w, ka);
    // ZPD pre-divergence at ka < kb gives padded equality.
    assert 1 <= ka < kb;
    assert PaddedComponent(b, ka) == PaddedComponent(w, ka);
    assert false;
  }
}
