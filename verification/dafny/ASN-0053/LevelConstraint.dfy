// ASN-0053: S6 — LevelConstraint (AXIOM / design-requirement)
// For a well-formed level-uniform span σ = (s, ℓ):
//   #start(σ) = #width(σ) = #reach(σ) = #s
include "IntersectionClosure.dfy"

module LevelConstraint {
  import opened IntersectionClosure
  import opened CarrierSetDefinition

  lemma {:axiom} LevelConstraint(sigma: SpanValue)
    requires ValidSpan(sigma)
    requires LevelUniform(sigma)
    ensures Length(sigma.start) == Length(sigma.length)
    ensures Length(sigma.length) == Length(ReachOf(sigma))
}
