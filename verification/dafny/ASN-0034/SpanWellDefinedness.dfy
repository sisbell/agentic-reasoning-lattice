// ASN-0034: T12 — SpanWellDefinedness
// For any (s, ℓ) satisfying the preconditions of Span:
//   (a) s ⊕ ℓ ∈ T
//   (b) s ∈ span(s, ℓ)
//   (c) span(s, ℓ) is order-convex under T1
include "./Span.dfy"
include "./WellDefinedAddition.dfy"
include "./StrictIncrease.dfy"

module SpanWellDefinedness {
  import opened CarrierSetDefinition
  import PT = PositiveTumbler
  import AP = ActionPoint
  import TA = TumblerAdd
  import LO = LexicographicOrder
  import WDA = WellDefinedAddition
  import SI = StrictIncrease
  import SP = Span
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  // Helper: transitivity of LexicographicOrder on Tumblers.
  // Needed for order convexity: chains like s ≤ a ≤ b and b ≤ c < s ⊕ ℓ
  // reduce to < chains via the < ∨ = decomposition.
  lemma LexicographicTransitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LO.LexicographicOrder(a, b)
    requires LO.LexicographicOrder(b, c)
    ensures LO.LexicographicOrder(a, c)
  {
    var j :| 1 <= j
          && (forall i :: 1 <= i < j ==>
                i <= Length(a) && i <= Length(b) &&
                Component(a, i) == Component(b, i))
          && ((j <= Length(a) && j <= Length(b) && Less(Component(a, j), Component(b, j)))
              || (j == Length(a) + 1 && j <= Length(b)));
    var k :| 1 <= k
          && (forall i :: 1 <= i < k ==>
                i <= Length(b) && i <= Length(c) &&
                Component(b, i) == Component(c, i))
          && ((k <= Length(b) && k <= Length(c) && Less(Component(b, k), Component(c, k)))
              || (k == Length(b) + 1 && k <= Length(c)));

    // Witness for LexicographicOrder(a, c) is min(j, k).
    var m := if j <= k then j else k;
    assert 1 <= m;

    // Agreement of a and c at positions 1..m-1.
    assert forall i :: 1 <= i < m ==>
              i < j && i < k &&
              i <= Length(a) && i <= Length(b) && i <= Length(c) &&
              Component(a, i) == Component(b, i) == Component(c, i);

    if j < k {
      // m == j. Either a_j < b_j or j == #a+1 ≤ #b.
      // For both cases, j < k means j ≤ #b and Component(b, j) == Component(c, j).
      assert j <= Length(b);
      assert j <= Length(c);
      assert Component(b, j) == Component(c, j);
      if j <= Length(a) && j <= Length(b) && Less(Component(a, j), Component(b, j)) {
        assert Less(Component(a, m), Component(c, m));
      } else {
        assert j == Length(a) + 1;
        assert m == Length(a) + 1 && m <= Length(c);
      }
    } else if k < j {
      // m == k.
      assert k < j;
      assert k <= Length(a);
      assert Component(a, k) == Component(b, k);
      assert k <= Length(b) && k <= Length(c) && Less(Component(b, k), Component(c, k));
      assert Less(Component(a, m), Component(c, m));
    } else {
      // j == k == m.
      if j <= Length(a) && j <= Length(b) && Less(Component(a, j), Component(b, j)) {
        if k <= Length(b) && k <= Length(c) && Less(Component(b, k), Component(c, k)) {
          Transitive(Component(a, m), Component(b, m), Component(c, m));
          assert Less(Component(a, m), Component(c, m));
        } else {
          // k == #b + 1 ≤ #c. But j ≤ #b and j == k, contradiction.
          assert false;
        }
      } else {
        // j == #a + 1 ≤ #b.
        assert j == Length(a) + 1;
        if k <= Length(b) && k <= Length(c) && Less(Component(b, k), Component(c, k)) {
          // k ≤ #b but j == k == #a + 1 ≤ #b. So m == #a + 1 ≤ #c.
          assert m == Length(a) + 1 && m <= Length(c);
        } else {
          // k == #b + 1 ≤ #c. But j == k and j ≤ #b. Contradiction with k == #b + 1.
          assert false;
        }
      }
    }
  }

  // T12 — SpanWellDefinedness
  lemma SpanWellDefinedness(s: Tumbler, l: Tumbler)
    requires InT(s) && InT(l)
    requires PT.PositiveTumbler(l)
    requires AP.ActionPoint(l) <= Length(s)
    // (a) Endpoint exists in T
    ensures InT(TA.TumblerAdd(s, l))
    // (b) s ∈ span(s, ℓ)
    ensures s in SP.Span(s, l)
    // (c) Order convexity: a ≤ b ≤ c with a, c ∈ span implies b ∈ span
    ensures forall a, b, c ::
              InT(a) && InT(b) && InT(c) &&
              a in SP.Span(s, l) && c in SP.Span(s, l) &&
              (a == b || LO.LexicographicOrder(a, b)) &&
              (b == c || LO.LexicographicOrder(b, c))
              ==> b in SP.Span(s, l)
  {
    // (a) follows from WellDefinedAddition
    WDA.WellDefinedAddition(s, l);
    // (b) follows from StrictIncrease — s < s ⊕ l, and s == s
    SI.StrictIncrease(s, l);
    // (c) Order convexity: bridge via transitivity for each (a, b, c) triple
    forall a, b, c |
              InT(a) && InT(b) && InT(c) &&
              a in SP.Span(s, l) && c in SP.Span(s, l) &&
              (a == b || LO.LexicographicOrder(a, b)) &&
              (b == c || LO.LexicographicOrder(b, c))
      ensures b in SP.Span(s, l)
    {
      // We need: (b == s || s < b) and b < s ⊕ l.
      // First clause: s ≤ a (from a ∈ Span) and a ≤ b.
      if a == s {
        // s == a, so a ≤ b gives s == b or s < b directly.
      } else {
        // s < a from membership of a in Span.
        assert LO.LexicographicOrder(s, a);
        if a == b {
          // s < a == b.
        } else {
          assert LO.LexicographicOrder(a, b);
          LexicographicTransitive(s, a, b);
        }
      }
      // Second clause: b ≤ c and c < s ⊕ l.
      if b == c {
        // b == c < s ⊕ l.
      } else {
        assert LO.LexicographicOrder(b, c);
        assert LO.LexicographicOrder(c, TA.TumblerAdd(s, l));
        LexicographicTransitive(b, c, TA.TumblerAdd(s, l));
      }
    }
  }
}
