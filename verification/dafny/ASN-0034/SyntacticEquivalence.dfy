// ASN-0034: T4a — SyntacticEquivalence
// The three positional conditions (no two adjacent zeros, t₁ ≠ 0,
// t_{#t} ≠ 0) are logically equivalent to the condition that every
// field segment of t — a maximal contiguous sub-sequence of non-zero
// positions delimited by the zeros of t — is non-empty.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"

module SyntacticEquivalence {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing

  // Split a sequence at zero separators into field segments.
  // Number of returned segments is always (zeros in s) + 1.
  function FieldSegments(s: seq<Carrier>): seq<seq<Carrier>>
    decreases |s|
    ensures |FieldSegments(s)| >= 1
  {
    if |s| == 0 then [[]]
    else if s[0] == 0 then [[]] + FieldSegments(s[1..])
    else
      var rest := FieldSegments(s[1..]);
      [[s[0]] + rest[0]] + rest[1..]
  }

  predicate AllFieldSegmentsNonEmpty(s: seq<Carrier>)
  {
    forall k :: 0 <= k < |FieldSegments(s)| ==> |FieldSegments(s)[k]| > 0
  }

  // The three positional conditions of T4's field-segment constraint:
  // (i) no two zeros adjacent, (ii) t₁ ≠ 0, (iii) t_{#t} ≠ 0.
  predicate FieldSegmentConstraint(t: Tumbler)
    requires InT(t)
  {
    (forall i :: 1 <= i < Length(t) ==>
       !(Component(t, i) == 0 && Component(t, i + 1) == 0)) &&
    Component(t, 1) != 0 &&
    Component(t, Length(t)) != 0
  }

  // Sequence-level form of the field-segment constraint.
  predicate PositionalConstraint(s: seq<Carrier>)
  {
    |s| >= 1 &&
    s[0] != 0 &&
    s[|s| - 1] != 0 &&
    (forall i :: 0 <= i < |s| - 1 ==> !(s[i] == 0 && s[i+1] == 0))
  }

  // If big = [non-empty head] + small, then all big segments non-empty
  // iff all small segments non-empty.
  lemma ShiftAllNonEmpty(big: seq<seq<Carrier>>, small: seq<seq<Carrier>>,
                         head: seq<Carrier>)
    requires big == [head] + small
    requires |head| > 0
    ensures (forall k :: 0 <= k < |big| ==> |big[k]| > 0)
         <==> (forall j :: 0 <= j < |small| ==> |small[j]| > 0)
  {
    assert |big| == 1 + |small|;
    assert big[0] == head;
    forall k | 1 <= k < |big| ensures big[k] == small[k-1] { }
    if forall k :: 0 <= k < |big| ==> |big[k]| > 0 {
      forall j | 0 <= j < |small|
        ensures |small[j]| > 0
      {
        assert |big[j+1]| > 0;
        assert big[j+1] == small[j];
      }
    }
    if forall j :: 0 <= j < |small| ==> |small[j]| > 0 {
      forall k | 0 <= k < |big|
        ensures |big[k]| > 0
      {
        if k == 0 {
          // |big[0]| == |head| > 0
        } else {
          assert big[k] == small[k-1];
          assert |small[k-1]| > 0;
        }
      }
    }
  }

  // Inductive characterization: positional constraint ⟺ every segment non-empty.
  lemma SegmentsCharacterization(s: seq<Carrier>)
    requires |s| >= 1
    ensures PositionalConstraint(s) <==> AllFieldSegmentsNonEmpty(s)
    decreases |s|
  {
    if |s| == 1 {
      // Base case: solver handles by unfolding FieldSegments.
    } else if s[0] == 0 {
      // First segment is empty; PositionalConstraint fails on s[0]!=0.
      assert FieldSegments(s)[0] == [];
      assert !AllFieldSegmentsNonEmpty(s);
      assert !PositionalConstraint(s);
    } else if s[1] != 0 {
      // s[0]!=0, s[1]!=0: recurse on s[1..], both sides shift cleanly.
      SegmentsCharacterization(s[1..]);
      var rest := FieldSegments(s[1..]);
      assert |rest[0]| >= 1;  // s[1..] starts with non-zero
      var segs := FieldSegments(s);
      assert segs == [[s[0]] + rest[0]] + rest[1..];
      assert |segs| == |rest|;
      assert segs[0] == [s[0]] + rest[0];
      assert forall k :: 1 <= k < |segs| ==> segs[k] == rest[k];
      assert AllFieldSegmentsNonEmpty(s) <==> AllFieldSegmentsNonEmpty(s[1..]);
      assert PositionalConstraint(s) <==> PositionalConstraint(s[1..]);
    } else if |s| == 2 {
      // s = [non-zero, 0]: PositionalConstraint fails on s[|s|-1]!=0.
      var s1 := s[1..];
      var emptyseq: seq<Carrier> := [];
      assert |s1| == 1 && s1[0] == 0;
      assert |s1[1..]| == 0;
      assert s1[1..] == emptyseq;
      assert FieldSegments(emptyseq) == [emptyseq];
      var rest := FieldSegments(s1);
      assert rest == [emptyseq] + [emptyseq];
      assert |rest| == 2 && rest[0] == emptyseq && rest[1] == emptyseq;
      var segs := FieldSegments(s);
      assert segs == [[s[0]] + rest[0]] + rest[1..];
      assert |segs| == 2;
      assert segs[1] == rest[1];
      assert segs[1] == emptyseq;
      assert |segs[1]| == 0;
      assert !AllFieldSegmentsNonEmpty(s);
      assert s[|s|-1] == 0;
      assert !PositionalConstraint(s);
    } else {
      // |s| >= 3, s[0] != 0, s[1] == 0: recurse on s[2..].
      SegmentsCharacterization(s[2..]);
      var s1 := s[1..];
      var emptyseq: seq<Carrier> := [];
      assert s1[0] == 0;
      assert s1[1..] == s[2..];
      var rest2 := FieldSegments(s[2..]);
      assert FieldSegments(s1) == [emptyseq] + rest2;
      var rest := FieldSegments(s1);
      assert rest == [emptyseq] + rest2;
      assert rest[0] == emptyseq;
      assert rest[1..] == rest2;
      var segs := FieldSegments(s);
      assert segs == [[s[0]] + rest[0]] + rest[1..];
      assert [s[0]] + rest[0] == [s[0]];
      assert segs == [[s[0]]] + rest2;
      ShiftAllNonEmpty(segs, rest2, [s[0]]);
      assert AllFieldSegmentsNonEmpty(s) <==> AllFieldSegmentsNonEmpty(s[2..]);
      assert PositionalConstraint(s) <==> PositionalConstraint(s[2..]);
    }
  }

  lemma SyntacticEquivalence(t: Tumbler)
    requires InT(t)
    ensures FieldSegmentConstraint(t) <==>
            AllFieldSegmentsNonEmpty(t.components)
  {
    SegmentsCharacterization(t.components);
    var s := t.components;
    assert |s| == Length(t);
    // Forward: FieldSegmentConstraint(t) ⟹ PositionalConstraint(s).
    if FieldSegmentConstraint(t) {
      assert s[0] == Component(t, 1);
      assert s[|s|-1] == Component(t, Length(t));
      forall i | 0 <= i < |s|-1
        ensures !(s[i] == 0 && s[i+1] == 0)
      {
        assert s[i] == Component(t, i+1);
        assert s[i+1] == Component(t, i+2);
        assert 1 <= i+1 < Length(t);
      }
    }
    // Backward: PositionalConstraint(s) ⟹ FieldSegmentConstraint(t).
    if PositionalConstraint(s) {
      assert Component(t, 1) == s[0];
      assert Component(t, Length(t)) == s[|s|-1];
      forall i | 1 <= i < Length(t)
        ensures !(Component(t, i) == 0 && Component(t, i+1) == 0)
      {
        assert Component(t, i) == s[i-1];
        assert Component(t, i+1) == s[i];
        assert 0 <= i-1 < |s|-1;
      }
    }
  }
}
