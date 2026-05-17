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

  lemma SyntacticEquivalence(t: Tumbler)
    requires InT(t)
    ensures FieldSegmentConstraint(t) <==>
            AllFieldSegmentsNonEmpty(t.components)
  { }
}
