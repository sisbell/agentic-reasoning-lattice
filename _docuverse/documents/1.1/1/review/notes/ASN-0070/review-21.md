# Review of ASN-0070

I checked the central proof obligations: the inverse-image definition (F0), the canonical-uniqueness theorem (F-canonical), the V-restricted denotation machinery, the worked configurations, and each derived lemma. The proofs are complete to a degree that resists the usual failure modes.

Specifically verified:

- **F-canonical Step 1** (ordinal-displacement widths) is genuinely exhaustive over `actionPoint(ℓ) ∈ [1, m]`: the `k < m` case yields an infinite V-restricted denotation (excluded by S8-fin finiteness, both inclusions shown), `k = m` yields the displacement (both inclusions shown). No case skipped.
- **The consecutivity Characterisation** reverse direction is proved by explicit induction on position, with all three impossible `(q, q')` divergence combinations ruled out via T0 irreflexivity/discreteness — not a "by similar reasoning."
- **F-canonical existence (Step 2a)** actually constructs the canonical form (maximal-run partition → per-run ordinal-displacement spans) and verifies N1/N2, rather than asserting existence from S8 alone. Left- and right-closure of inter-component gaps are both handled, including the `s_j.m = 1` positivity sub-case.
- **F-subspace** reverse direction (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`) is the load-bearing non-trivial step and is proved via S3★-aux + L14, not assumed.
- **F-multi** correctly distinguishes the implication (holds for both subspaces, vacuously for `s_L`) from realizability (only `s_C`, since CL-UNIQ forbids link-subspace multiplicity) — the interaction with CL-UNIQ is acknowledged, not overlooked.
- **Boundary cases**: empty document (`m_S(d)` undefined → `⟨⟩` convention), empty endset (vacuous coverage), no-reach, partial reach, and fragmentation are each exercised against a concrete configuration. The sixth configuration instantiates F-contig at non-zero offset (`j=1, c<n`), which the prior five never reached.
- **wp analysis** is non-trivial and lands on exactly the stated preconditions; the frame's `wp = true` is correctly noted.
- The V-restricted denotation does not require `dom(M(d))` membership, but the postcondition equality forces it, and the maximal-run construction guarantees the representation introduces no spurious lattice points. Consistent.

All ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058) — no self-contained-violation. The note specifies a state-pure query, its postcondition, and invariant-style consequences abstractly; the "Computation via Decomposition" section is explicitly labeled as one admissible strategy, not mandated mechanics. No drift.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, transclusion-lineage correspondence, concurrency semantics, canonical-form contracts for citation
The ASN's own Open Questions enumerate these. They concern downstream system-level contracts (citation artifacts, replication concurrency, multi-document lineage relations) that build on `follow` rather than belonging to its specification. Correctly deferred, not errors here.

VERDICT: CONVERGED
