// ASN-0034: TA1 — OrderPreservationUnderAddition
// (A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b :
//   a ⊕ w ≤ b ⊕ w).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatStrictTotalOrder.dfy"
include "./Divergence.dfy"
include "./IntrinsicComparison.dfy"

module OrderPreservationUnderAddition {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened CanonicalRepresentation
  import opened NatStrictTotalOrder
  import opened NatCarrierSet
  import opened Divergence
  import IC = IntrinsicComparison

  // Helper: LexicographicOrder(a, b) ⇒ a != b. The :| succeeds because the
  // `if a == b` block drives the solver to unfold the predicate.
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

  // Helper: in case (i) (divergence within both lengths), the LexicographicOrder
  // witness coincides with Divergence and the strict inequality holds at it.
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

  lemma OrderPreservationUnderAddition(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires ActionPoint.ActionPoint(w) <= Length(b)
    ensures
      var r1 := TumblerAdd.TumblerAdd(a, w);
      var r2 := TumblerAdd.TumblerAdd(b, w);
      LexicographicOrder.LexicographicOrder(r1, r2) || r1 == r2
  {
    LexImpliesNotEqual(a, b);

    var ap := ActionPoint.ActionPoint(w);
    var d := Divergence.Divergence(a, b);
    var r1 := TumblerAdd.TumblerAdd(a, w);
    var r2 := TumblerAdd.TumblerAdd(b, w);
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);

    // ap <= min(|a|, |b|) = m.
    assert ap <= m;

    if d <= m {
      // Case (i): components first diverge at d ≤ m, with Less(a_d, b_d).
      DivergenceCaseIStrict(a, b);

      if d < ap {
        // Witness d for LexicographicOrder(r1, r2). Prefix region for both.
        forall i | 1 <= i < d
          ensures i <= Length(r1) && i <= Length(r2)
                  && Component(r1, i) == Component(r2, i)
        {
          assert i < d < ap;
          assert Component(r1, i) == Component(a, i);
          assert Component(r2, i) == Component(b, i);
        }
        assert d <= Length(r1) && d <= Length(r2);
        assert Component(r1, d) == Component(a, d);
        assert Component(r2, d) == Component(b, d);
        assert Less(Component(r1, d), Component(r2, d));
        assert LexicographicOrder.LexicographicOrder(r1, r2) by {
          assert 1 <= d
              && (forall i :: 1 <= i < d ==>
                    i <= Length(r1) && i <= Length(r2)
                    && Component(r1, i) == Component(r2, i))
              && (d <= Length(r1) && d <= Length(r2)
                  && Less(Component(r1, d), Component(r2, d)));
        }
      } else if d == ap {
        // Witness d = ap. Less(a_d + w_d, b_d + w_d) from Less(a_d, b_d) on nat.
        forall i | 1 <= i < d
          ensures i <= Length(r1) && i <= Length(r2)
                  && Component(r1, i) == Component(r2, i)
        {
        }
        assert Component(r1, d) == Component(a, d) + Component(w, d);
        assert Component(r2, d) == Component(b, d) + Component(w, d);
        assert Less(Component(r1, d), Component(r2, d));
        assert LexicographicOrder.LexicographicOrder(r1, r2) by {
          assert 1 <= d
              && (forall i :: 1 <= i < d ==>
                    i <= Length(r1) && i <= Length(r2)
                    && Component(r1, i) == Component(r2, i))
              && (d <= Length(r1) && d <= Length(r2)
                  && Less(Component(r1, d), Component(r2, d)));
        }
      } else {
        // d > ap: r1 and r2 coincide on [1, #w] (componentwise equality).
        forall i | 1 <= i <= Length(w)
          ensures Component(r1, i) == Component(r2, i)
        {
          if i < ap {
            assert i < ap < d;
          } else if i == ap {
            assert ap < d;
          }
        }
        CanonicalRepresentation.CanonicalRepresentation(r1, r2);
      }
    } else {
      // Case (ii): d > m. a and b agree on [1, m]; from a != b, |a| ≠ |b|.
      // LexicographicOrder(a, b) forces |a| < |b| (else b would be ≤ a).
      assert d > m;
      assert forall i :: 1 <= i <= m ==> Component(a, i) == Component(b, i);

      if Length(b) <= Length(a) {
        if Length(b) < Length(a) {
          // b is a strict prefix of a. By IntrinsicComparison, LexOrder(b, a)
          // and !LexOrder(a, b). Contradicts the precondition.
          assert m == Length(b);
          assert forall j :: 1 <= j <= Length(b) ==> Component(b, j) == Component(a, j);
          IC.ShorterPrefix(b, a);
          assert false;
        } else {
          // |a| == |b|. Pointwise agreement gives a == b, contradicting a != b.
          assert m == Length(a) == Length(b);
          Extensionality(a, b);
          assert false;
        }
      }
      assert Length(a) < Length(b);
      // ap ≤ |a| < d, so the equality argument goes through.
      forall i | 1 <= i <= Length(w)
        ensures Component(r1, i) == Component(r2, i)
      {
        if i < ap {
          assert i < ap <= Length(a) < d;
        } else if i == ap {
          assert ap <= Length(a) < d;
        }
      }
      CanonicalRepresentation.CanonicalRepresentation(r1, r2);
    }
  }
}
