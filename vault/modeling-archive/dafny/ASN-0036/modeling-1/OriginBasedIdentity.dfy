include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

// S4 — OriginBasedIdentity
module OriginBasedIdentity {
  import opened TumblerAlgebra
  import TumblerAllocation

  // S4: For I-addresses a1, a2 produced by distinct allocation events,
  // a1 != a2, regardless of whether C(a1) = C(a2).
  // Derived from GlobalUniqueness (ASN-0034).
  lemma OriginBasedIdentity(
    a1: Tumbler, a2: Tumbler,
    origin1: Tumbler, origin2: Tumbler
  )
    requires IsPrefix(origin1, a1)
    requires IsPrefix(origin2, a2)
    requires
      (LessThan(a1, a2) || LessThan(a2, a1))
      ||
      (!IsPrefix(origin1, origin2) && !IsPrefix(origin2, origin1))
      ||
      |a1.components| != |a2.components|
    ensures a1 != a2
  { }
}
