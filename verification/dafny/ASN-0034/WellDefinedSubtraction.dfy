// ASN-0034: TA2 — WellDefinedSubtraction
// Corollary packaging TumblerSub's well-formedness and length postconditions:
//   (A a, w ∈ T : a ≥ w : a ⊖ w ∈ T ∧ #(a ⊖ w) = max(#a, #w)).
include "./TumblerSub.dfy"
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"

module WellDefinedSubtraction {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerSub

  lemma WellDefinedSubtraction(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures InT(TumblerSub.TumblerSub(a, w))
    ensures Length(TumblerSub.TumblerSub(a, w)) ==
            (if Length(a) >= Length(w) then Length(a) else Length(w))
  { }
}
