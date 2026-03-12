include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module AccountPrefixModule {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0029 account — AccountPrefix (INV, function(DocId): Tumbler)
  // account(d) = max≼ {a ∈ AccountAddr : a ≼ d}
  // The unique account-level prefix of d: the longest prefix with exactly
  // one zero separator. For address N.0.U.0.D..., extracts Tumbler([N, 0, U]).

  // Find index of first zero in s starting from position i
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

  // d has at least one zero separator and a component after it
  predicate HasAccountLevel(d: Tumbler) {
    (exists j :: 0 <= j < |d.components| && d.components[j] == 0) &&
    FirstZeroFrom(d.components, 0) + 1 < |d.components|
  }

  // Extract the account prefix: prefix through the component after the first zero
  function AccountPrefix(d: DocId): Tumbler
    requires HasAccountLevel(d)
  {
    var z := FirstZeroFrom(d.components, 0);
    Tumbler(d.components[..z+2])
  }
}
