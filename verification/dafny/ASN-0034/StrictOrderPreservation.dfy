// ASN-0034: TA1-strict — StrictOrderPreservation
// Corollary of TA1: when actionPoint(w) ≥ divergence(a, b),
// addition preserves strict order:
//   a < b ∧ Pos(w) ∧ actionPoint(w) ≤ min(#a, #b) ∧
//   actionPoint(w) ≥ divergence(a, b) ⇒ a ⊕ w < b ⊕ w.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./LexicographicOrder.dfy"
include "./Divergence.dfy"
include "./NatStrictTotalOrder.dfy"

module StrictOrderPreservation {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened Divergence
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  // Helper: LexicographicOrder(a, b) implies a != b. (T1 witness rules out equality.)
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

  // Helper: when divergence falls strictly within both lengths, the
  // T1 witness coincides with Divergence and case (i) holds.
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
              && ((kp <= Length(a) && kp <= Length(b) && Less(Component(a, kp), Component(b, kp)))
                  || (kp == Length(a) + 1 && kp <= Length(b)));
    if kp < k {
      assert Component(a, kp) == Component(b, kp);
      if kp <= Length(a) && kp <= Length(b) && Less(Component(a, kp), Component(b, kp)) {
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

  lemma StrictOrderPreservation(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires ActionPoint.ActionPoint(w) <= Length(b)
    requires ActionPoint.ActionPoint(w) >= Divergence.Divergence(a, b)
    ensures LexicographicOrder.LexicographicOrder(
              TumblerAdd.TumblerAdd(a, w),
              TumblerAdd.TumblerAdd(b, w))
  {
    // From `a < b` and T1 irreflexivity, derive `a != b` to discharge
    // Divergence's precondition.
    LexImpliesNotEqual(a, b);

    var ap := ActionPoint.ActionPoint(w);
    var d := Divergence.Divergence(a, b);
    var ra := TumblerAdd.TumblerAdd(a, w);
    var rb := TumblerAdd.TumblerAdd(b, w);

    assert d <= Length(a) && d <= Length(b);
    DivergenceCaseIStrict(a, b);
    // From DivergenceCaseIStrict:
    //   1 ≤ d, ∀ i < d : a_i = b_i, a_d < b_d.

    assert Length(ra) == Length(w);
    assert Length(rb) == Length(w);
    assert d <= Length(ra) && d <= Length(rb);

    // For i < d ≤ ap, both r_a[i] = a[i] and r_b[i] = b[i] (prefix region).
    forall i | 1 <= i < d
      ensures Component(ra, i) == Component(rb, i)
    {
      assert i < ap;
      assert Component(ra, i) == Component(a, i);
      assert Component(rb, i) == Component(b, i);
    }

    // Less(r_a[d], r_b[d]): cases d < ap (prefix) vs d == ap (sum).
    if d < ap {
      assert Component(ra, d) == Component(a, d);
      assert Component(rb, d) == Component(b, d);
    } else {
      assert d == ap;
      assert Component(ra, d) == Component(a, d) + Component(w, d);
      assert Component(rb, d) == Component(b, d) + Component(w, d);
    }
    assert Less(Component(ra, d), Component(rb, d));

    // Witness k = d for LexicographicOrder(ra, rb).
    assert LexicographicOrder.LexicographicOrder(ra, rb) by {
      assert 1 <= d
          && (forall i :: 1 <= i < d ==>
                i <= Length(ra) && i <= Length(rb) &&
                Component(ra, i) == Component(rb, i))
          && (d <= Length(ra) && d <= Length(rb) &&
              Less(Component(ra, d), Component(rb, d)));
    }
  }
}
