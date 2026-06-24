// ASN-0053: S6 — LevelConstraint (AXIOM, design-requirement)
include "SpanDefs.dfy"

module LevelConstraint {
  import opened SpanDefs
  import opened CarrierSetDefinition

  // level_compat(t₁, t₂) ≡ #t₁ = #t₂
  ghost predicate LevelCompat(t1: Tumbler, t2: Tumbler) {
    Length(t1) == Length(t2)
  }

  // σ = (s, ℓ) is level-uniform when level_compat(s, ℓ)
  ghost predicate LevelUniform(sigma: SpanEntry) {
    LevelCompat(sigma.start, sigma.width)
  }

  // S6 (LevelConstraint): for a well-formed level-uniform span,
  // start, width, and reach share a single tumbler length.
  lemma {:axiom} LevelConstraint(sigma: SpanEntry)
    requires ValidSpan(sigma)
    requires LevelUniform(sigma)
    ensures Length(sigma.start) == Length(sigma.width)
    ensures Length(sigma.start) == Length(Reach(sigma))
    ensures Length(sigma.width) == Length(Reach(sigma))
}
