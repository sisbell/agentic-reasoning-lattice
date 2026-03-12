module HierarchicalParsing {
  import opened TumblerAlgebra

  // T4 — HierarchicalParsing

  // Count of zero-valued components in a sequence
  function CountZeros(s: seq<nat>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + CountZeros(s[1..])
  }

  // Structural constraint on valid I-space addresses:
  // at most three zeros (field separators), no adjacent zeros,
  // first and last components strictly positive.
  // Find position of first zero in s starting from index i
  function FirstZeroFrom(s: seq<nat>, i: nat): nat
    requires i <= |s|
    requires exists j :: i <= j < |s| && s[j] == 0
    ensures i <= FirstZeroFrom(s, i) < |s|
    ensures s[FirstZeroFrom(s, i)] == 0
    ensures forall j :: i <= j < FirstZeroFrom(s, i) ==> s[j] != 0
    decreases |s| - i
  {
    if s[i] == 0 then i
    else FirstZeroFrom(s, i + 1)
  }

  // d has at least one zero separator with a component after it
  predicate HasAccountLevel(d: Tumbler) {
    (exists j :: 0 <= j < |d.components| && d.components[j] == 0) &&
    FirstZeroFrom(d.components, 0) + 1 < |d.components|
  }

  // Extract the account prefix: prefix through the component after the first zero
  function AccountPrefix(d: Tumbler): Tumbler
    requires HasAccountLevel(d)
  {
    var z := FirstZeroFrom(d.components, 0);
    Tumbler(d.components[..z+2])
  }

  predicate ValidAddress(t: Tumbler) {
    |t.components| > 0 &&
    CountZeros(t.components) <= 3 &&
    t.components[0] != 0 &&
    t.components[|t.components| - 1] != 0 &&
    forall i :: 0 <= i < |t.components| - 1 ==>
      !(t.components[i] == 0 && t.components[i + 1] == 0)
  }
}
