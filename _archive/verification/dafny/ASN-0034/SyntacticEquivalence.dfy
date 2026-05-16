module SyntacticEquivalence {
  // T4a — SyntacticEquivalence (corollary of T4)
  // The non-empty field constraint is equivalent to three syntactic
  // conditions: no adjacent zeros, first component != 0, last component != 0.

  datatype Tumbler = Tumbler(components: seq<nat>)

  ghost predicate ValidTumbler(t: Tumbler) {
    |t.components| >= 1
  }

  // Length of the field (consecutive non-zero elements) starting at `start`
  function FieldLen(s: seq<nat>, start: nat): (len: nat)
    requires start <= |s|
    ensures start + len <= |s|
    ensures forall j :: start <= j < start + len ==> s[j] != 0
    ensures start + len < |s| ==> s[start + len] == 0
    decreases |s| - start
  {
    if start == |s| || s[start] == 0 then 0
    else 1 + FieldLen(s, start + 1)
  }

  // Structural: every zero-delimited field has at least one component
  ghost predicate FieldsNonEmpty(s: seq<nat>, start: nat)
    requires start <= |s|
    decreases |s| - start
  {
    if start == |s| then true
    else if s[start] == 0 then false
    else
      var len := FieldLen(s, start);
      var next := start + len;
      next == |s| || (next + 1 < |s| && FieldsNonEmpty(s, next + 1))
  }

  // Syntactic: three conditions
  ghost predicate SyntacticWF(s: seq<nat>)
    requires |s| >= 1
  {
    s[0] != 0 &&
    s[|s| - 1] != 0 &&
    forall i :: 0 <= i < |s| - 1 ==> !(s[i] == 0 && s[i + 1] == 0)
  }

  // Forward: fields non-empty implies syntactic conditions
  lemma ForwardImpl(s: seq<nat>, start: nat)
    requires start <= |s|
    requires FieldsNonEmpty(s, start)
    ensures start < |s| ==> s[start] != 0
    ensures start < |s| ==> s[|s| - 1] != 0
    ensures forall i :: start <= i < |s| - 1 ==> !(s[i] == 0 && s[i + 1] == 0)
    decreases |s| - start
  {
    if start < |s| {
      var len := FieldLen(s, start);
      var next := start + len;
      if next == |s| {
      } else {
        ForwardImpl(s, next + 1);
      }
    }
  }

  // Backward: syntactic conditions imply fields non-empty
  lemma BackwardImpl(s: seq<nat>, start: nat)
    requires start <= |s|
    requires start < |s| ==> s[start] != 0
    requires start < |s| ==> s[|s| - 1] != 0
    requires forall i :: start <= i < |s| - 1 ==> !(s[i] == 0 && s[i + 1] == 0)
    ensures FieldsNonEmpty(s, start)
    decreases |s| - start
  {
    if start < |s| {
      var len := FieldLen(s, start);
      var next := start + len;
      if next < |s| {
        BackwardImpl(s, next + 1);
      }
    }
  }

  // T4a: the non-empty field constraint <=> three syntactic conditions
  lemma SyntacticEquivalence(t: Tumbler)
    requires ValidTumbler(t)
    ensures FieldsNonEmpty(t.components, 0) <==> SyntacticWF(t.components)
  {
    if FieldsNonEmpty(t.components, 0) {
      ForwardImpl(t.components, 0);
    }
    if SyntacticWF(t.components) {
      BackwardImpl(t.components, 0);
    }
  }
}
