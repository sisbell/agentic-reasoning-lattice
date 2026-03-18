include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T4 — ValidAddress
module ValidAddress {
  import opened TumblerAlgebra

  // Count zero-valued components in a sequence
  function ZeroCount(s: seq<nat>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + ZeroCount(s[1..])
  }

  // No two adjacent components are both zero
  predicate NoAdjacentZeros(s: seq<nat>) {
    forall i :: 0 <= i < |s| - 1 ==> !(s[i] == 0 && s[i + 1] == 0)
  }

  // T4: A tumbler used as an address has at most three zero-valued
  // components (field separators), no two zeros are adjacent, and
  // does not begin or end with zero.
  predicate ValidAddress(t: Tumbler) {
    |t.components| >= 1 &&
    ZeroCount(t.components) <= 3 &&
    t.components[0] != 0 &&
    t.components[|t.components| - 1] != 0 &&
    NoAdjacentZeros(t.components)
  }
}
