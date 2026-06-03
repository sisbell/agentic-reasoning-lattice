# Review of ASN-0070

I read the note in full and checked each proof, the worked examples, the weakest-precondition analysis, and the derived-property catalogue against the foundations. I also applied the forward-reference accretion lens flagged for this note.

## REVISE

None. The substantive proofs hold up under scrutiny:

- **F-canonical** establishes *both* existence (Step 2a's per-maximal-run construction, with N1/N2 proved directly) and uniqueness (the consecutivity characterization, acyclicity ruling out cycles via T1 irreflexivity/transitivity, and the V-restricted↔full denotation bridge that lifts S9). The case split on `k = actionPoint(ℓ)` is jointly exhaustive (`k < m` excluded by infinitude via T0(a); `k = m` proved by mutual inclusion; `k > m` impossible by the ActionPoint bound). No "by similar reasoning" gaps.
- **Boundary cases are covered**: empty result (F-empty, both denotational and representational halves), undefined `m_S(d)` (vacuous-subspace convention), multiplicity (F-multi, with the CL-UNIQ contrast correctly confining realisability to the content subspace), and cross-subspace straddle (Configuration 5 exercises the `⊎` non-trivially with both components populated).
- **F-sound/F-complete** are correctly identified as the two inclusions of the postcondition's set equality, each derived from F0+F1.
- **Worked examples** verify the named guarantees against concrete arrangements, including state-dependence under a real K.μ⁻ transition (Configuration 4) with L12-invariance of the link.
- **WP analysis** is non-trivial (notes `i ∈ {1,2,3}` always admissible via L3 but higher indices need checking) and concludes minimality.

Anti-bloat pass: I checked for the named accretion patterns (consumer enumeration in definitions, axiom-rationale sub-paragraphs, document-ordering justification, reviser-drift cases imagining excluded scenarios, cross-section deferrals to a common location). The "Discussion: System Guarantees" section is essay content but sits in a correctly-labelled Discussion slot, not in a structural claim slot, and the F-multi "structural admissibility" paragraph is substantive (cites S5/K.μ⁺/CL-UNIQ to establish non-vacuousness, not defensive filler). The repeated "block I-extents are depth-`m_a`" clause across worked examples is mild redundancy but each instance is tailored to its configuration. Nothing rises to an actionable finding, and a generic dep/inline-proof bloat audit was already deliberated and declined in a prior cycle.

## OUT_OF_SCOPE

### Topic 1: Cross-home resolution, concurrency semantics, and transclusion-lineage relationships
**Why out of scope**: These are the note's own three Open Questions. They are correctly deferred to future ASNs rather than treated as gaps in FOLLOWLINK — the present operation is a state-pure inverse-image query, and each open question introduces new state-relationship obligations beyond resolution itself.

VERDICT: CONVERGED
