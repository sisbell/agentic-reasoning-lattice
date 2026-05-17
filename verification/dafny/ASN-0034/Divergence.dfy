// ASN-0034: Divergence — Divergence
// For distinct tumblers a, b ∈ T, divergence(a, b) is the index of
// the first divergence: either the smallest k ≤ min(#a, #b) with
// aₖ ≠ bₖ, or min(#a, #b) + 1 when all shared components agree.
include "./CarrierSetDefinition.dfy"

module Divergence {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  function FirstMismatch(a: Tumbler, b: Tumbler, start: nat, m: nat): nat
    requires InT(a) && InT(b)
    requires m <= Length(a) && m <= Length(b)
    requires 1 <= start <= m + 1
    ensures start <= FirstMismatch(a, b, start, m) <= m + 1
    ensures FirstMismatch(a, b, start, m) <= m ==>
      Component(a, FirstMismatch(a, b, start, m)) != Component(b, FirstMismatch(a, b, start, m))
    ensures forall i :: start <= i < FirstMismatch(a, b, start, m) ==>
      Component(a, i) == Component(b, i)
    decreases m + 1 - start
  {
    if start > m then m + 1
    else if Component(a, start) != Component(b, start) then start
    else FirstMismatch(a, b, start + 1, m)
  }

  lemma FirstMismatchSymmetric(a: Tumbler, b: Tumbler, start: nat, m: nat)
    requires InT(a) && InT(b)
    requires m <= Length(a) && m <= Length(b)
    requires 1 <= start <= m + 1
    ensures FirstMismatch(a, b, start, m) == FirstMismatch(b, a, start, m)
    decreases m + 1 - start
  {
    if start > m {
    } else if Component(a, start) != Component(b, start) {
    } else {
      FirstMismatchSymmetric(a, b, start + 1, m);
    }
  }

  function Divergence(a: Tumbler, b: Tumbler): nat
    requires InT(a) && InT(b)
    requires a != b
    ensures Length(a) < Length(b) &&
            (forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i))
            ==> Divergence(a, b) == Length(a) + 1
    ensures Length(b) < Length(a) &&
            (forall i :: 1 <= i <= Length(b) ==> Component(a, i) == Component(b, i))
            ==> Divergence(a, b) == Length(b) + 1
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    FirstMismatch(a, b, 1, m)
  }

  // Symmetry: divergence(a, b) = divergence(b, a) for all a ≠ b.
  // Dafny disallows this as a self-referential ensures on Divergence
  // (the postcondition's swapped call has no strictly-decreasing measure),
  // so the contractual guarantee is encoded as this companion lemma.
  lemma DivergenceSymmetric(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires a != b
    ensures Divergence(a, b) == Divergence(b, a)
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    FirstMismatchSymmetric(a, b, 1, m);
  }
}
