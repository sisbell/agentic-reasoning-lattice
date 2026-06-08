# Review of ASN-0113

I checked each introduced claim's derivation, the boundary cases (empty document, allocated-but-empty, one-occupied-subspace, minimal depth `m=2`, and a non-trivial `m=3`), the foundation citations, and the anti-bloat patterns flagged for this note.

## Correctness and rigor

The proofs hold under scrutiny:

- **W4 (ExactCoverage)** correctly uses T5 with prefix `[S,1,…,1]` of length `m_S−1` (legal since S8a forces `m_S ≥ 2`, so `#p ≥ 1`); `start_S ≤ t < reach` gives `start_S ≤ t ≤ reach`, T5 pins the prefix, and the half-open bounds pin `1 ≤ t_{m_S} ≤ n_S`. Both completeness and exclusivity are shown, and the `m=3` worked instance genuinely exercises the interior-position confinement that `m=2` leaves vacuous.
- **W3** reach computation via OrdinalShift checks out (`actionPoint(δ(n_S,m_S)) = m_S ≤ #start_S`, level-uniform).
- **W10/W11** confinement-then-disjointness argument via T1 first-divergence is sound for tumblers of any depth, and correctly closes through SC-NEQ.
- **W13** normalization is verified directly against N1/N2 by T1 (not by S8–S10, which would have needed level-compatibility the two members may lack — correctly avoided since disjointness obviates merging).
- **W19** wp is a genuine weakest-precondition partition of the allocated states by the two emptiness bits, with W-pre correctly conjoined so `d ∉ dom(M)` is failure, not `⟨⟩`.
- **W20** honestly separates *arranged* links (counted) from *home* links (a superset), grounding the CL-OWN/CL-UNIQ bijection and refusing to over-claim a standing creation-coupling.

All claims carry explicit derivations, three concrete instances verify the key postconditions, wp analysis is non-trivial, and cross-document/derived consequences (W14, W15, W16, W17) are derived rather than asserted. The depth standard is met.

## Foundation usage and scope

Every cross-ASN reference resolves to a listed foundation (ASN-0034, ASN-0036, ASN-0047, ASN-0053, ASN-0093). Local notation (`VSlice`, `ext`, `occupied`, `O(d)`) is genuine helper definition, not reinvention of foundation concepts. Out-of-scope topics (single overall extent, link counting/discovery, transclusion, versioning) appear only as Open Questions, properly deferred.

## Anti-bloat

The motivational passages (e.g. the opener of "Why text and links must be reported apart," the third worked instance's justification) are statements of what the operation does and what each example adds — informative, not meta-prose under the note's own standard. The consultation/Gregory references function as implementation evidence grounding the precondition and faithfulness claims, not as specification mechanics. I found no forward-reference deferrals, no use-site inventories, no axiom-rationale sub-paragraphs, and no duplicated paragraphs. The note reads as already-cleaned.

The ASN specifies abstract state-query guarantees an alternative implementation would have to satisfy. It has not drifted into implementation mechanics.

VERDICT: CONVERGED
