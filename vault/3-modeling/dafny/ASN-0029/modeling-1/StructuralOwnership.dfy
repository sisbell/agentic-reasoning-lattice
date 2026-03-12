include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"

module StructuralOwnership {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  // ASN-0029 D3 — StructuralOwnership (INV, predicate(DocId))
  // account(d) is computable from d's tumbler address alone,
  // without consulting any mutable state.

  // Find first zero at or after position i
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

  // Precondition: d has at least two zero separators
  predicate HasTwoZeros(s: seq<nat>) {
    exists i, j :: 0 <= i < j < |s| && s[i] == 0 && s[j] == 0
  }

  // Account prefix: everything before the second zero separator.
  // For d = [N-fields, 0, U-fields, 0, D-fields], returns [N-fields, 0, U-fields].
  // Pure function of the address — no mutable state consulted.
  function Account(d: DocId): Tumbler
    requires HasTwoZeros(d.components)
  {
    var z1 := FirstZeroFrom(d.components, 0);
    var z2 := FirstZeroFrom(d.components, z1 + 1);
    Tumbler(d.components[..z2])
  }

  // D3: account(d) is structurally determined by d's tumbler address.
  // Witnessed by Account being a pure function (no State parameter).
  // The predicate asserts that for any address with at least two zeros,
  // the account prefix is well-defined and is a proper prefix of d.
  ghost predicate StructuralOwnership(d: DocId) {
    HasTwoZeros(d.components) ==>
      IsPrefix(Account(d), d) &&
      HierarchicalParsing.CountZeros(Account(d).components) == 1
  }
}
