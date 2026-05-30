# Channel Assignment — ASN-0082 review-63

**Date:** 2026-05-30 11:22

## Issue 1: OrdinalExceedsDisplacement is stated for "any V-position v" but its conclusions hold only within subspace 1
Reason: Internal fix. The unsoundness and its remedy are both visible in the ASN: OrdinalOrderEquivalence's stated preconditions (subspace and depth agreement) and the fact that all downstream uses instantiate v ∈ R ⊆ V_1(d). Adding `subspace(v) = 1` to the quantifier is derivable from the ASN's own lemma signatures.

## Issue 2: I3-S omits the `n ≥ 1` precondition its proof relies on
Reason: Internal fix. The required precondition is fixed by the cited foundation signatures already present in the ASN (OrdinalShift and TS3 both require n ≥ 1, per the registry rows). Stating `n ≥ 1` adds no new content beyond what the citations dictate.

## Issue 3: Anti-bloat — redundant restatement after OrdAddHom
Reason: Internal fix. Pure editorial deletion of a sentence that duplicates OrdAddHom clause (a)'s own gloss; no design intent or implementation evidence bears on it.

## Issue 4: Anti-bloat — NAT-CA introduction explains why the axiom is needed rather than what it states
Reason: Internal fix. Pure editorial trim of justifying meta-prose; the axiom statement is self-sufficient and no external channel informs the wording.
