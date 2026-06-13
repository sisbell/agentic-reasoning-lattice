# Review of ASN-0132

I reviewed this note adversarially: re-derived the worked example by hand, checked each wp derivation against the cited FL-WP cases, traced the forking/version-refraction argument through J4, and ran the anti-bloat scan the classifier calls for. My verification notes:

- **Worked example checks out end to end.** `coverage(F) = [1.0.1.0.1.0.1.5, 1.0.1.0.1.0.1.13)` (re-derived `s ⊕ δ(8,8) = [...,13]`, the eight ordinals 5–12). `nullified(Σ) = {a₂}` — verified `a_R`'s to-coverage `{t : a₂ ≼ t}` meets `dom(Σ.L)` only at `a₂`, since the five equal-length link addresses are pairwise prefix-incomparable (Prefix/T3). `addressable(Σ) = {a₁, a₃, a₄, a_R}`; per-link contributions 1/0/1/0/0 give `count(q,Σ) = 2`; `count(q*,Σ) = 4`; `count(q_H,Σ) = 2`; `count(q_H',Σ) = 0` is a genuine CN-ZERO (`d₂ ⋠ d₁`, equal-length divergence at the document component), not the degenerate FL-EMP zero. The dynamic chain 2→3 (ordinary K.λ at `…2.6`, `L_R` fixed), 3→3 (K.μ⁻, F-PRES), 3→2 (retraction K.λ at `…2.7` nullifying counted `a₁`, CN-MONO hypothesis correctly *failing*) all verify, including sibling-chain frontier advancement.
- **CN-MONO wp derivations are faithful.** Ordinary case reproduces FL-WP(a) including the inherited (not re-derived) `¬(∃ standing retraction covering ℓ)` conjunct, which collapses under ASN-0086's disciplined-domain simplification + R0a. Retraction case correctly identifies the hypothesis as load-bearing against collateral withdrawal and pulls the self-retraction term `b ∉ coverage(G')` from FL-WP(b). The multi-step `count(Σ) ≤ count(Σ')` is sound: every link counted at Σ survives to Σ' under the hypothesis (L12/LP13 fix `sat`, hypothesis fixes addressability), and CN-STAB+F-PRES make K.λ the sole count-changing transition.
- **CN-UNIT, CN-ZERO, CN-STAB, CN-RETRACT, CN-ORPHAN, CN-OBT** all sound. CN-ORPHAN's superset/gap arithmetic (`count = |⋃_d surfaced satisfying| + |orphans|`) checks against FL-REACH(d). The forking-is-link-store-inert argument is correct against J4 (K.δ + K.μ⁺ over `V_{s_C}` + K.ρ, no K.λ, no K.μ⁺_L).
- **Citations** are all to foundation ASNs (0034/0036/0043/0047/0058/0086/0093/0098/0121/0127); no notation reinvented; Standard 7 satisfied. No drift into implementation mechanics — the operation is specified as the cardinality of a set, abstractly, with Gregory's back end correctly framed as deviating *from* the spec.

**Anti-bloat scan (below the obstruction threshold).** The worst patterns are absent: no axioms (so no axiom-rationale sub-paragraphs), no downstream-consumer inventories at definitions, no document-ordering justifications, no paragraphs reasoning inside a case the precondition excludes (the CN-MONO collateral-withdrawal discussion exists to prove the hypothesis load-bearing, and the worked example instantiates the failure — purposeful, not drift), deferrals route to *distinct* open questions. The only residue is two single-clause exposition justifications ("it is worth walking the three cases rather than asserting the conclusion"; "because it diverges from the ordinary case, we walk it in full rather than cite it"); each rides on substantive content and neither obstructs following its claim, so neither meets the "have to skip past meta-prose to follow a claim" bar for a finding. The Nelson-style interpretive prose is house-style analogy, explicitly carved out as non-meta-prose.

## REVISE

None.

## OUT_OF_SCOPE

None — the note's own scope-exclusions and six open questions (federated count, count/enumeration concurrency, caching, fragmentation-dedup, cost-vs-enumeration asymmetry, content delivery) already park the future-ASN territory correctly.

VERDICT: CONVERGED
