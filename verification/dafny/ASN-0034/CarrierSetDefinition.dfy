// ASN-0034: T0 — CarrierSetDefinition
// T is the set of nonempty finite sequences over ℕ.
include "./NatCarrierSet.dfy"

module CarrierSetDefinition {
  import opened NatCarrierSet

  datatype Tumbler = Tumbler(components: seq<Carrier>)

  ghost predicate InT(a: Tumbler) {
    |a.components| >= 1
  }

  function Length(a: Tumbler): nat {
    |a.components|
  }

  function Component(a: Tumbler, i: nat): Carrier
    requires InT(a)
    requires 1 <= i <= Length(a)
  {
    a.components[i - 1]
  }

  // Axiom: every tumbler has at least one component.
  lemma {:axiom} Nonemptiness(a: Tumbler)
    requires InT(a)
    ensures 1 <= Length(a)

  // Axiom: component projection is total and natural-valued on the index domain.
  lemma {:axiom} ComponentProjectionSignature(a: Tumbler, i: nat)
    requires InT(a)
    requires 1 <= i <= Length(a)
    ensures InCarrier(Component(a, i))

  // Axiom: comprehension — every nonempty finite sequence of naturals is in T.
  lemma {:axiom} Comprehension(p: nat, r: nat -> Carrier)
    requires p >= 1
    ensures exists t: Tumbler ::
      InT(t) &&
      Length(t) == p &&
      forall i :: 1 <= i <= p ==> Component(t, i) == r(i)

  // Axiom: extensionality — equal length and pointwise-equal components implies equal.
  lemma {:axiom} Extensionality(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) == Length(b)
    requires forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
    ensures a == b
}
