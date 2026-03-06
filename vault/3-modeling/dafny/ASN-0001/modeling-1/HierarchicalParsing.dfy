include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

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
  predicate ValidAddress(t: Tumbler) {
    |t.components| > 0 &&
    CountZeros(t.components) <= 3 &&
    t.components[0] != 0 &&
    t.components[|t.components| - 1] != 0 &&
    forall i :: 0 <= i < |t.components| - 1 ==>
      !(t.components[i] == 0 && t.components[i + 1] == 0)
  }
}
