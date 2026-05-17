// ASN-0034: T12 — SpanWellDefinedness
// For any (s, ℓ) satisfying the preconditions of Span:
//   (a) s ⊕ ℓ ∈ T
//   (b) s ∈ span(s, ℓ)
//   (c) span(s, ℓ) is order-convex under T1
include "./Span.dfy"
include "./WellDefinedAddition.dfy"
include "./StrictIncrease.dfy"
include "./IntrinsicComparison.dfy"

module SpanWellDefinedness {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened WellDefinedAddition
  import opened StrictIncrease
  import opened Span
  import opened NatStrictTotalOrder
  import opened NatCarrierSet
  import IC = IntrinsicComparison

  // Inductive transitivity of CompareFrom on the LT result.
  // Reasoning is structural on the CompareFrom definition: the cases for
  // i == Length(a)/b/c either return a non-LT value (contradicting the
  // preconditions), or reduce to nat order transitivity at position i+1.
  lemma CompareFromTransitiveLT(a: Tumbler, b: Tumbler, c: Tumbler, i: nat)
    requires InT(a) && InT(b) && InT(c)
    requires 0 <= i <= Length(a) && 0 <= i <= Length(b) && 0 <= i <= Length(c)
    requires IC.CompareFrom(a, b, i) == IC.LT
    requires IC.CompareFrom(b, c, i) == IC.LT
    ensures IC.CompareFrom(a, c, i) == IC.LT
    decreases Length(b) - i
  {
    if i == Length(b) {
      // CompareFrom(a, b, i) at i == Length(b) returns EQ (if i == Length(a))
      // or GT (if i < Length(a)) — never LT.
      assert false;
    } else if i == Length(c) {
      // CompareFrom(b, c, i) at i == Length(c) and i < Length(b) returns GT.
      assert false;
    } else if i == Length(a) {
      // i < Length(b) and i < Length(c), so CompareFrom(a, c, i) returns LT.
    } else {
      var ai := Component(a, i + 1);
      var bi := Component(b, i + 1);
      var ci := Component(c, i + 1);

      if Less(ai, bi) {
        if Less(bi, ci) {
          Transitive(ai, bi, ci);
        } else if Less(ci, bi) {
          // CompareFrom(b, c, i) would return GT.
          assert false;
        } else {
          // bi == ci, so Less(ai, ci) from Less(ai, bi).
        }
      } else if Less(bi, ai) {
        // CompareFrom(a, b, i) would return GT.
        assert false;
      } else {
        // ai == bi.
        if Less(bi, ci) {
          // ai == bi < ci, so Less(ai, ci).
        } else if Less(ci, bi) {
          // CompareFrom(b, c, i) would return GT.
          assert false;
        } else {
          // ai == bi == ci. Recurse with i + 1.
          CompareFromTransitiveLT(a, b, c, i + 1);
        }
      }
    }
  }

  // Transitivity of LexicographicOrder. Bridges via IntrinsicComparison: convert
  // LexOrder to Compare == LT, prove transitivity for Compare, convert back.
  lemma LexicographicTransitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires LexicographicOrder.LexicographicOrder(b, c)
    ensures LexicographicOrder.LexicographicOrder(a, c)
  {
    IC.IntrinsicComparison(a, b);
    IC.IntrinsicComparison(b, c);
    assert IC.Compare(a, b) == IC.LT;
    assert IC.Compare(b, c) == IC.LT;
    CompareFromTransitiveLT(a, b, c, 0);
    assert IC.Compare(a, c) == IC.LT;
    IC.IntrinsicComparison(a, c);
  }

  // T12 — SpanWellDefinedness
  lemma SpanWellDefinedness(s: Tumbler, l: Tumbler)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    // (a) Endpoint exists in T
    ensures InT(TumblerAdd.TumblerAdd(s, l))
    // (b) s ∈ span(s, ℓ)
    ensures s in Span.Span(s, l)
    // (c) Order convexity: a ≤ b ≤ c with a, c ∈ span implies b ∈ span
    ensures forall a, b, c ::
              InT(a) && InT(b) && InT(c) &&
              a in Span.Span(s, l) && c in Span.Span(s, l) &&
              (a == b || LexicographicOrder.LexicographicOrder(a, b)) &&
              (b == c || LexicographicOrder.LexicographicOrder(b, c))
              ==> b in Span.Span(s, l)
  {
    // (a) follows from WellDefinedAddition
    WellDefinedAddition.WellDefinedAddition(s, l);
    // (b) follows from StrictIncrease — s < s ⊕ l, and s == s
    StrictIncrease.StrictIncrease(s, l);
    // (c) Order convexity: bridge via transitivity of LexicographicOrder
    forall a, b, c |
              InT(a) && InT(b) && InT(c) &&
              a in Span.Span(s, l) && c in Span.Span(s, l) &&
              (a == b || LexicographicOrder.LexicographicOrder(a, b)) &&
              (b == c || LexicographicOrder.LexicographicOrder(b, c))
      ensures b in Span.Span(s, l)
    {
      // First clause: (b == s || s < b)
      // From a ∈ Span: s ≤ a. From hypothesis: a ≤ b.
      if a == s {
        // s == a, then s == b or s < b via a ≤ b.
      } else {
        assert LexicographicOrder.LexicographicOrder(s, a);
        if a == b {
          // s < a == b.
        } else {
          assert LexicographicOrder.LexicographicOrder(a, b);
          LexicographicTransitive(s, a, b);
        }
      }
      // Second clause: b < s ⊕ l
      // From c ∈ Span: c < s ⊕ l. From hypothesis: b ≤ c.
      if b == c {
        // b == c < s ⊕ l.
      } else {
        assert LexicographicOrder.LexicographicOrder(b, c);
        assert LexicographicOrder.LexicographicOrder(c, TumblerAdd.TumblerAdd(s, l));
        LexicographicTransitive(b, c, TumblerAdd.TumblerAdd(s, l));
      }
    }
  }
}
