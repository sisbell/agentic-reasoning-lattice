# Review of ASN-0091

I checked the abstract Vstream-only class definition, the K.μ~ realisation (both directions), every per-invariant discharge against ASN-0047's `ExtendedReachableStateInvariants` list, the arithmetic of all four worked examples plus the two-step composition, and the edge-case handling (empty, identity, collapse, shared I-addresses, interior cuts).

## REVISE

(none)

Specific checks that passed and could have failed:

- **Realiser case-split is sound, not hand-waved.** The non-trivial (K.μ~) vs. collapse (empty composite) split is correctly keyed to clause (ii) `M'(d) ≠ M(d)`, not to value-uniformity. The period-2 example (`a,b,a,b` under `gcd(w_α,w_β)=2`) genuinely distinguishes the two thresholds, and its R-P1/R-P2 arithmetic reproduces the pre-state exactly, confirming collapse with the distinct-value precondition still satisfied. The empty composite is correctly justified as the zero-step case of `→*`.
- **Forward direction (clauses i–v) closed without circularity.** The per-invariant discharges of S3★, D-CTG★, etc. are sourced from REARRANGE_K's own definitions (RA-dom via K.μ~-FIX, fact (b) constructive subspace-preservation, RE-C/RE-L), not from RA-adm — the S3★ discharge explicitly avoids the circular appeal. Clause (iii) length-preservation correctly routes link-subspace positions through RE-sub (π(v)=v) and content positions through the fixed `m_S`.
- **RE-subpres two-stage argument is necessary and complete.** Stage 1 (binary constraint via S3★-aux) is genuinely load-bearing — without it the conditional S3★ implications would be vacuously satisfiable at a third subspace value — and both cross-directions are run.
- **ChainDisjointAdjacency is parametric in chain identity**, so it correctly covers the proper-prefix document case where a positional-divergence argument would fail; the T10a.6 alternative is also offered.
- **All worked-example admissibility checks** verify S2, S3★, S8★, P4★, CL-OWN/UNIQ, and P4a concretely; the bijection-non-uniqueness example confirms RE-proj's set image is witness-independent.

Minor (non-blocking) observation, recorded but not raised as REVISE: the paraphrase of ASN-0047's K.δ Document-case "effect clause" (`M'(d') = M(d')` for `d' ≠ e`) is a substantively-correct interpretation of the `dom(M') = dom(M) ∪ {e}` frame rather than a literal quote; the discharge of RA-reg is unaffected.

## OUT_OF_SCOPE

The five Open Questions (same-source split transclusion guarantees, link-subspace rearrangement semantics, observational equivalence at discoverability granularity, run-cardinality increase bound, realisability of arbitrary well-formedness-preserving bijections by cut compositions) are correctly deferred — each is new territory, not a gap in this ASN's stated scope.

VERDICT: CONVERGED
