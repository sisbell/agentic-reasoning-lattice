include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module IdentityByAddress {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0029 D6 — IdentityByAddress (INV, predicate(DocId, DocId))
  // d₁ = d₂  ⟺  fields(d₁) = fields(d₂)

  // Parsed document address fields
  datatype DocFields = DocFields(node: seq<nat>, user: seq<nat>, doc: seq<nat>)

  // Find first zero at or after index i
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

  // Document-level address: form [N..., 0, U..., 0, D...] with exactly
  // two zero separators and all field components nonzero
  predicate IsDocAddr(d: DocId) {
    |d.components| >= 5 &&
    d.components[0] != 0 &&
    d.components[|d.components| - 1] != 0 &&
    (exists j :: 0 <= j < |d.components| && d.components[j] == 0) &&
    (var z1 := FirstZeroFrom(d.components, 0);
     z1 + 2 <= |d.components| &&
     (exists j :: z1 + 1 <= j < |d.components| && d.components[j] == 0) &&
     (var z2 := FirstZeroFrom(d.components, z1 + 1);
      z2 < |d.components| - 1 &&
      (forall j :: z2 < j < |d.components| ==> d.components[j] != 0)))
  }

  // Extract the three address fields from a document address
  function Fields(d: DocId): DocFields
    requires IsDocAddr(d)
  {
    var z1 := FirstZeroFrom(d.components, 0);
    var z2 := FirstZeroFrom(d.components, z1 + 1);
    DocFields(d.components[..z1], d.components[z1+1..z2], d.components[z2+1..])
  }

  // Build a document address from its three field sequences
  function Compose(f: DocFields): DocId {
    Tumbler(f.node + [0] + f.user + [0] + f.doc)
  }

  // Round-trip: parsing then composing recovers the original address
  lemma FieldsRoundTrip(d: DocId)
    requires IsDocAddr(d)
    ensures Compose(Fields(d)) == d
  { }

  // D6: identity by address — document identity is determined by fields
  ghost predicate IdentityByAddress(d1: DocId, d2: DocId) {
    IsDocAddr(d1) && IsDocAddr(d2) ==>
      (d1 == d2 <==> Fields(d1) == Fields(d2))
  }

  lemma IdentityByAddressHolds(d1: DocId, d2: DocId)
    requires IsDocAddr(d1) && IsDocAddr(d2)
    ensures d1 == d2 <==> Fields(d1) == Fields(d2)
  {
    if Fields(d1) == Fields(d2) {
      FieldsRoundTrip(d1);
      FieldsRoundTrip(d2);
    }
  }
}
