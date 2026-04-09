include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"

module PositiveTumbler {
  // PositiveTumbler — PositiveTumblerDefinition
  // t > 0 iff (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  ghost predicate IsPositive(t: Tumbler) {
    exists i :: 0 <= i < |t.components| && t.components[i] != 0
  }

  ghost predicate IsZero(t: Tumbler) {
    forall i :: 0 <= i < |t.components| ==> t.components[i] == 0
  }

  // Negative: t cannot be less than z when t is positive and z is zero
  lemma NotLessThanZero(t: Tumbler, z: Tumbler)
    requires IsPositive(t)
    requires IsZero(z)
    ensures !LessThan(t, z)
  { }

  // Negative: positive and zero tumblers are not equal
  lemma PositiveNotZero(t: Tumbler, z: Tumbler)
    requires IsPositive(t)
    requires IsZero(z)
    ensures t != z
  { }

  // Postcondition: t > 0 ∧ z is zero ⟹ z < t under T1
  lemma PositiveGtZero(t: Tumbler, z: Tumbler)
    requires IsPositive(t)
    requires IsZero(z)
    ensures LessThan(z, t)
  {
    LessThanTrichotomy(z, t);
    PositiveNotZero(t, z);
    NotLessThanZero(t, z);
  }
}
