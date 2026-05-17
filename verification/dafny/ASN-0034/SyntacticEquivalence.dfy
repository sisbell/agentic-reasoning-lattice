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
    } else if s[1] != 0 {
      // s[0]!=0, s[1]!=0: recurse on s[1..], both sides shift cleanly.
      SegmentsCharacterization(s[1..]);
      var rest := FieldSegments(s[1..]);
      assert |rest[0]| >= 1;  // s[1..] starts with non-zero
    } else if |s| == 2 {
      // s = [non-zero, 0]: PositionalConstraint fails on s[|s|-1]!=0.
      // FieldSegments(s) = [[s[0]], []], last segment empty.
      assert FieldSegments(s[1..]) == [[], []];
    } else {
      // |s| >= 3, s[0] != 0, s[1] == 0: recurse on s[2..].
      SegmentsCharacterization(s[2..]);
      var rest := FieldSegments(s[1..]);
      assert rest == [[]] + FieldSegments(s[2..]);
      var segs := FieldSegments(s);
      assert segs == [[s[0]]] + FieldSegments(s[2..]);
    }
  }

  lemma SyntacticEquivalence(t: Tumbler)
    requires InT(t)
    ensures FieldSegmentConstraint(t) <==>
            AllFieldSegmentsNonEmpty(t.components)
  {
    SegmentsCharacterization(t.components);
    // Bridge Tumbler/seq indexing: Component(t, i) == t.components[i-1],
    // Length(t) == |t.components|.
    assert FieldSegmentConstraint(t) <==> PositionalConstraint(t.components);
  }
}
