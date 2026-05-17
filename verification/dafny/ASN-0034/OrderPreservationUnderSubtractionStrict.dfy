// ASN-0034: TA3-strict — OrderPreservationUnderSubtractionStrict
// (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./TumblerSub.dfy"
include "./WellDefinedSubtraction.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./Divergence.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatPartialSubtraction.dfy"
include "./NatZeroMinimum.dfy"

module OrderPreservationUnderSubtractionStrict {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerSub
  import opened WellDefinedSubtraction
  import opened ZeroPaddedDivergence
  import opened Divergence
  import opened NatStrictTotalOrder
  import opened NatPartialSubtraction
  import opened NatZeroMinimum
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened ActionPoint

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
                && ((kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)))
                    || (kw == Length(a) + 1 && kw <= Length(b)));
      if kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)) {
        Irreflexive(Component(a, kw));
      }
    }
  }

  // Helper: at equal lengths, T1 case (ii) is impossible. From a < b extract
  // a strict-component witness via Divergence.
  lemma EqualLengthDivergenceWitness(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) == Length(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures a != b
    ensures var j := Divergence.Divergence(a, b);
            1 <= j <= Length(a) &&
            (forall i :: 1 <= i < j ==> Component(a, i) == Component(b, i)) &&
            Less(Component(a, j), Component(b, j))
  {
    LexImpliesNotEqual(a, b);
    var m := Length(a);
    var j := Divergence.Divergence(a, b);
    assert j == Divergence.FirstMismatch(a, b, 1, m);
    if j > m {
      assert j == m + 1;
      assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);
      Extensionality(a, b);
      assert false;
    }
    assert 1 <= j <= m;
    assert Component(a, j) != Component(b, j);
    assert forall i :: 1 <= i < j ==> Component(a, i) == Component(b, i);
    var kw :| 1 <= kw
              && (forall i :: 1 <= i < kw ==>
                    i <= Length(a) && i <= Length(b) &&
                    Component(a, i) == Component(b, i))
              && ((kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)))
                  || (kw == Length(a) + 1 && kw <= Length(b)));
    if kw == Length(a) + 1 && kw <= Length(b) {
      assert kw == m + 1;
      assert kw <= m;
      assert false;
    }
    assert kw <= Length(a) && kw <= Length(b);
    assert Less(Component(a, kw), Component(b, kw));
    if kw < j {
      assert Component(a, kw) == Component(b, kw);
      Irreflexive(Component(a, kw));
    } else if kw > j {
      assert Component(a, j) == Component(b, j);
    }
    assert kw == j;
  }

  // Bridge: TumblerSub's componentwise formula via SubComponent.
  lemma TumblerSubComponents(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures
      var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
      var L := if Length(a) >= Length(w) then Length(a) else Length(w);
      var r := TumblerSub.TumblerSub(a, w);
      Length(r) == L &&
      forall i :: 1 <= i <= L ==>
        Component(r, i) == SubComponent(a, w, k, i)
  { }

  // Helper: when ZPD(x, w) != 0, the divergence index lies within x's native domain.
  // Suppose otherwise: zpd > Length(x). Then padded(x, zpd) = 0. But TumblerSub
  // gives padded(x, zpd) > padded(w, zpd) ≥ 0 (nat). Contradiction.
  lemma ZpdBoundedByOperand(x: Tumbler, w: Tumbler)
    requires InT(x) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, x) || w == x
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(x, w) != 0
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(x, w) <= Length(x)
  {
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(x, w);
    var L := if Length(x) >= Length(w) then Length(x) else Length(w);
    assert 1 <= k <= L;
    TumblerSub.TumblerSubPaddedDifference(x, w);
    assert PaddedComponent(x, k) > PaddedComponent(w, k);
    if k > Length(x) {
      assert PaddedComponent(x, k) == 0;
      assert false;
    }
  }

  // Helper: ZPD(x, w) == 0 implies all padded components agree on [1, L].
  lemma ZpdZeroPaddedEqual(x: Tumbler, w: Tumbler)
    requires InT(x) && InT(w)
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(x, w) == 0
    ensures var L := if Length(x) >= Length(w) then Length(x) else Length(w);
            forall i :: 1 <= i <= L ==> PaddedComponent(x, i) == PaddedComponent(w, i)
  {
    var L := if Length(x) >= Length(w) then Length(x) else Length(w);
    assert FirstPaddedMismatch(x, w, 1, L) == L + 1;
  }

  // Helper: identifying ZPD from pre-agreement and a disagreement point.
  // If padded(x, w) agree on [1, j-1] and disagree at j (1 ≤ j ≤ L),
  // then ZPD(x, w) = j.
  lemma ZpdIdentify(x: Tumbler, w: Tumbler, j: nat)
    requires InT(x) && InT(w)
    requires 1 <= j
    requires j <= (if Length(x) >= Length(w) then Length(x) else Length(w))
    requires forall i :: 1 <= i < j ==> PaddedComponent(x, i) == PaddedComponent(w, i)
    requires PaddedComponent(x, j) != PaddedComponent(w, j)
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(x, w) == j
  {
    var L := if Length(x) >= Length(w) then Length(x) else Length(w);
    var fpm := FirstPaddedMismatch(x, w, 1, L);
    if fpm > j {
      assert PaddedComponent(x, j) == PaddedComponent(w, j);
      assert false;
    } else if fpm < j {
      assert PaddedComponent(x, fpm) != PaddedComponent(w, fpm);
      assert PaddedComponent(x, fpm) == PaddedComponent(w, fpm);
      assert false;
    }
    assert fpm == j;
  }

  // Helper: from LexOrder(a, b), a divergence witness pointing the other way
  // (Less(b_k, a_k) with prefix agreement up to k-1) derives false. Internalises
  // the asymmetry of LexOrder at the Component (Carrier) level.
  lemma LexAsymmetricAtDivergence(a: Tumbler, b: Tumbler, k: nat)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires 1 <= k <= Length(a) && k <= Length(b)
    requires forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i)
    requires Less(Component(b, k), Component(a, k))
    ensures false
  {
    var kw :| 1 <= kw
              && (forall i :: 1 <= i < kw ==>
                    i <= Length(a) && i <= Length(b) &&
                    Component(a, i) == Component(b, i))
              && ((kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)))
                  || (kw == Length(a) + 1 && kw <= Length(b)));
    if kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)) {
      if kw < k {
        assert Component(a, kw) == Component(b, kw);
        Irreflexive(Component(a, kw));
      } else if kw == k {
        Asymmetric(Component(a, k), Component(b, k));
      } else {
        assert Component(a, k) == Component(b, k);
        Irreflexive(Component(a, k));
      }
    } else {
      assert kw > Length(a);
      assert k <= Length(a);
      assert k < kw;
      assert Component(a, k) == Component(b, k);
      Irreflexive(Component(a, k));
    }
  }

  lemma OrderPreservationUnderSubtractionStrict(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires LexicographicOrder.LexicographicOrder(w, b) || w == b
    requires Length(a) == Length(b)
    ensures LexicographicOrder.LexicographicOrder(
              TumblerSub.TumblerSub(a, w),
              TumblerSub.TumblerSub(b, w))
  {
    EqualLengthDivergenceWitness(a, b);
    var j := Divergence.Divergence(a, b);
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var ra := TumblerSub.TumblerSub(a, w);
    var rb := TumblerSub.TumblerSub(b, w);
    WellDefinedSubtraction.WellDefinedSubtraction(a, w);
    WellDefinedSubtraction.WellDefinedSubtraction(b, w);
    var da := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    var db := ZeroPaddedDivergence.ZeroPaddedDivergence(b, w);
    TumblerSubComponents(a, w);
    TumblerSubComponents(b, w);

    assert Length(ra) == L;
    assert Length(rb) == L;
    assert j <= Length(a) <= L;

    if da == 0 {
      // Case A: a is zero-padded-equal to w.
      ZpdZeroPaddedEqual(a, w);
      forall i | 1 <= i < j
        ensures PaddedComponent(b, i) == PaddedComponent(w, i)
      {
        assert i <= Length(a);
        assert Component(a, i) == Component(b, i);
        assert PaddedComponent(a, i) == Component(a, i);
        assert PaddedComponent(b, i) == Component(b, i);
        assert PaddedComponent(a, i) == PaddedComponent(w, i);
      }
      assert j <= Length(a) <= L;
      assert PaddedComponent(a, j) == Component(a, j);
      assert PaddedComponent(b, j) == Component(b, j);
      assert PaddedComponent(a, j) == PaddedComponent(w, j);
      assert Component(a, j) < Component(b, j);
      assert PaddedComponent(w, j) == Component(a, j);
      assert PaddedComponent(w, j) != Component(b, j);
      assert PaddedComponent(b, j) != PaddedComponent(w, j);
      ZpdIdentify(b, w, j);
      assert db == j;
      assert PaddedComponent(b, j) > PaddedComponent(w, j);
      assert SubComponent(a, w, da, j) == 0;
      assert SubComponent(b, w, db, j) == PaddedComponent(b, j) - PaddedComponent(w, j);
      assert Component(ra, j) == 0;
      assert Component(rb, j) == PaddedComponent(b, j) - PaddedComponent(w, j);
      assert Component(rb, j) > 0;
      forall i | 1 <= i < j
        ensures Component(ra, i) == Component(rb, i)
      {
        assert i <= L;
        assert Component(ra, i) == SubComponent(a, w, da, i);
        assert SubComponent(a, w, da, i) == 0;
        assert i < db;
        assert Component(rb, i) == SubComponent(b, w, db, i);
        assert SubComponent(b, w, db, i) == 0;
      }
      assert LexicographicOrder.LexicographicOrder(ra, rb) by {
        assert 1 <= j
            && (forall i :: 1 <= i < j ==>
                  i <= Length(ra) && i <= Length(rb) &&
                  Component(ra, i) == Component(rb, i))
            && (j <= Length(ra) && j <= Length(rb) &&
                Less(Component(ra, j), Component(rb, j)));
      }
    } else if db == 0 {
      // Contradiction: db == 0 ∧ da != 0.
      ZpdBoundedByOperand(a, w);
      assert 1 <= da <= Length(a);
      ZpdZeroPaddedEqual(b, w);
      var fpmA := FirstPaddedMismatch(a, w, 1, L);
      assert fpmA == da;
      forall i | 1 <= i < da
        ensures Component(a, i) == Component(b, i)
      {
        assert i <= L;
        assert i <= Length(a);
        assert i <= Length(b);
        assert PaddedComponent(a, i) == Component(a, i);
        assert PaddedComponent(b, i) == Component(b, i);
        assert PaddedComponent(b, i) == PaddedComponent(w, i);
        assert PaddedComponent(a, i) == PaddedComponent(w, i);
      }
      assert PaddedComponent(a, da) > PaddedComponent(w, da);
      assert da <= L;
      assert PaddedComponent(b, da) == PaddedComponent(w, da);
      assert PaddedComponent(a, da) > PaddedComponent(b, da);
      assert PaddedComponent(a, da) == Component(a, da);
      assert da <= Length(b);
      assert PaddedComponent(b, da) == Component(b, da);
      assert Component(a, da) > Component(b, da);
      assert Less(Component(b, da), Component(a, da));
      LexAsymmetricAtDivergence(a, b, da);
    } else if da == db {
      // Case 1
      var d := da;
      ZpdBoundedByOperand(a, w);
      ZpdBoundedByOperand(b, w);
      assert 1 <= d <= Length(a);
      assert 1 <= d <= Length(b);
      var fpmA := FirstPaddedMismatch(a, w, 1, L);
      var fpmB := FirstPaddedMismatch(b, w, 1, L);
      assert fpmA == d;
      assert fpmB == d;
      forall i | 1 <= i < d
        ensures Component(a, i) == Component(b, i)
      {
        assert i <= L;
        assert PaddedComponent(a, i) == PaddedComponent(w, i);
        assert PaddedComponent(b, i) == PaddedComponent(w, i);
        assert i <= Length(a) && i <= Length(b);
      }
      // T1 witness j: Less(a_j, b_j). Since a_i = b_i for i < d, j ≥ d.
      assert j >= d by {
        if j < d {
          assert Component(a, j) == Component(b, j);
          Irreflexive(Component(a, j));
        }
      }
      if j == d {
        // Subcase j == d.
        assert PaddedComponent(a, d) > PaddedComponent(w, d);
        assert PaddedComponent(b, d) > PaddedComponent(w, d);
        assert PaddedComponent(a, d) == Component(a, d);
        assert PaddedComponent(b, d) == Component(b, d);
        assert Component(a, d) < Component(b, d);
        assert Component(ra, d) == SubComponent(a, w, da, d);
        assert Component(rb, d) == SubComponent(b, w, db, d);
        assert SubComponent(a, w, da, d) == PaddedComponent(a, d) - PaddedComponent(w, d);
        assert SubComponent(b, w, db, d) == PaddedComponent(b, d) - PaddedComponent(w, d);
        assert Component(ra, d) == PaddedComponent(a, d) - PaddedComponent(w, d);
        assert Component(rb, d) == PaddedComponent(b, d) - PaddedComponent(w, d);
        assert Component(ra, d) < Component(rb, d);
        forall i | 1 <= i < d
          ensures Component(ra, i) == Component(rb, i)
        {
          assert i <= L;
          assert Component(ra, i) == 0;
          assert Component(rb, i) == 0;
        }
        assert LexicographicOrder.LexicographicOrder(ra, rb) by {
          assert 1 <= d
              && (forall i :: 1 <= i < d ==>
                    i <= Length(ra) && i <= Length(rb) &&
                    Component(ra, i) == Component(rb, i))
              && (d <= Length(ra) && d <= Length(rb) &&
                  Less(Component(ra, d), Component(rb, d)));
        }
      } else {
        // Subcase j > d.
        assert d < j;
        assert Component(a, d) == Component(b, d);
        assert PaddedComponent(a, d) == Component(a, d);
        assert PaddedComponent(b, d) == Component(b, d);
        assert PaddedComponent(a, d) == PaddedComponent(b, d);
        assert Component(ra, d) == PaddedComponent(a, d) - PaddedComponent(w, d);
        assert Component(rb, d) == PaddedComponent(b, d) - PaddedComponent(w, d);
        assert Component(ra, d) == Component(rb, d);
        forall i | 1 <= i < j
          ensures i <= Length(ra) && i <= Length(rb) &&
                  Component(ra, i) == Component(rb, i)
        {
          if i < d {
            assert Component(ra, i) == 0 == Component(rb, i);
          } else if i == d {
            // already shown
          } else {
            // d < i < j
            assert i <= Length(a) && i <= Length(b);
            assert Component(a, i) == Component(b, i);
            assert Component(ra, i) == SubComponent(a, w, da, i);
            assert Component(rb, i) == SubComponent(b, w, db, i);
            assert SubComponent(a, w, da, i) == PaddedComponent(a, i);
            assert SubComponent(b, w, db, i) == PaddedComponent(b, i);
            assert PaddedComponent(a, i) == Component(a, i);
            assert PaddedComponent(b, i) == Component(b, i);
          }
        }
        assert j <= L;
        assert j > d;
        assert Component(ra, j) == SubComponent(a, w, da, j);
        assert Component(rb, j) == SubComponent(b, w, db, j);
        assert SubComponent(a, w, da, j) == PaddedComponent(a, j);
        assert SubComponent(b, w, db, j) == PaddedComponent(b, j);
        assert PaddedComponent(a, j) == Component(a, j);
        assert PaddedComponent(b, j) == Component(b, j);
        assert Component(ra, j) < Component(rb, j);
        assert LexicographicOrder.LexicographicOrder(ra, rb) by {
          assert 1 <= j
              && (forall i :: 1 <= i < j ==>
                    i <= Length(ra) && i <= Length(rb) &&
                    Component(ra, i) == Component(rb, i))
              && (j <= Length(ra) && j <= Length(rb) &&
                  Less(Component(ra, j), Component(rb, j)));
        }
      }
    } else if da < db {
      // Case 2: contradiction.
      ZpdBoundedByOperand(a, w);
      ZpdBoundedByOperand(b, w);
      assert 1 <= da <= Length(a);
      assert 1 <= db <= Length(b);
      var fpmA := FirstPaddedMismatch(a, w, 1, L);
      assert fpmA == da;
      assert PaddedComponent(b, da) == PaddedComponent(w, da);
      assert PaddedComponent(a, da) > PaddedComponent(w, da);
      assert PaddedComponent(a, da) == Component(a, da);
      assert da <= Length(b);
      assert PaddedComponent(b, da) == Component(b, da);
      assert Component(a, da) > Component(b, da);
      assert Less(Component(b, da), Component(a, da));
      forall i | 1 <= i < da
        ensures Component(a, i) == Component(b, i)
      {
        assert i < db;
        assert PaddedComponent(a, i) == PaddedComponent(w, i);
        assert PaddedComponent(b, i) == PaddedComponent(w, i);
      }
      LexAsymmetricAtDivergence(a, b, da);
    } else {
      // Case 3: da > db.
      ZpdBoundedByOperand(a, w);
      ZpdBoundedByOperand(b, w);
      assert 1 <= da <= Length(a);
      assert 1 <= db <= Length(b);
      var fpmB := FirstPaddedMismatch(b, w, 1, L);
      assert fpmB == db;
      assert PaddedComponent(a, db) == PaddedComponent(w, db);
      assert PaddedComponent(b, db) > PaddedComponent(w, db);
      forall i | 1 <= i < db
        ensures Component(a, i) == Component(b, i)
      {
        assert i < da;
        assert PaddedComponent(a, i) == PaddedComponent(w, i);
        assert PaddedComponent(b, i) == PaddedComponent(w, i);
      }
      assert Component(ra, db) == SubComponent(a, w, da, db);
      assert db < da;
      assert SubComponent(a, w, da, db) == 0;
      assert Component(ra, db) == 0;
      assert Component(rb, db) == SubComponent(b, w, db, db);
      assert SubComponent(b, w, db, db) == PaddedComponent(b, db) - PaddedComponent(w, db);
      assert Component(rb, db) > 0;
      forall i | 1 <= i < db
        ensures Component(ra, i) == Component(rb, i)
      {
        assert i <= L;
        assert i < da;
        assert Component(ra, i) == SubComponent(a, w, da, i);
        assert SubComponent(a, w, da, i) == 0;
        assert Component(rb, i) == SubComponent(b, w, db, i);
        assert SubComponent(b, w, db, i) == 0;
      }
      assert db <= L;
      assert LexicographicOrder.LexicographicOrder(ra, rb) by {
        assert 1 <= db
            && (forall i :: 1 <= i < db ==>
                  i <= Length(ra) && i <= Length(rb) &&
                  Component(ra, i) == Component(rb, i))
            && (db <= Length(ra) && db <= Length(rb) &&
                Less(Component(ra, db), Component(rb, db)));
      }
    }
  }
}
