# Review of ASN-0070

I read this as a pure-query operation note: FOLLOWLINK computes the inverse image `R(d, e) = M(d)⁻¹(coverage(e))`, projected per subspace, represented as a per-subspace family of V-span-sets. I checked the central theorem (F-canonical), the supporting lemmas, the edge cases, and — given the active `review-mode.anti-bloat` classifier — scanned for forward-reference accretion.

## Findings

**Rigor.** The load-bearing proof is F-canonical (existence + uniqueness of the canonical form). I traced all five steps:
- Step 1's action-point case split (`1 ≤ k < m_S` infinite ⟦σ⟧_V, excluded by finiteness; `k = m_S` gives the ordinal-displacement progression) is sound, both inclusions of `⟦σ⟧_V = E` are shown explicitly, and the case split is genuinely exhaustive via the ActionPoint bound.
- Step 2's consecutivity characterisation, the single-valued-successor + acyclicity argument for the partition into chains, and the inductive forward/reverse proofs are complete and correct.
- Steps 3–4 (per-run existence; uniqueness via the V-restricted↔full denotation bridge, including both right- and left-closure of maximal runs, with the `s_j.m = 1` positivity sub-case handled) hold up.

**Edge cases.** Empty document (`dom(M(d)) = ∅`), empty endset (`eᵢ = ∅`, only `e₃ ≠ ∅` forced by L3), vacuous subspace vs. coverage-misses-arrangement (distinguished in F-empty and Config 6), multiplicity in content subspace blocked by CL-UNIQ in link subspace — all covered. F-subspace's biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` correctly leans on S3★ + L14 + S3★-aux.

**Cross-ASN references.** All citations (0034, 0036, 0043, 0047, 0053, 0058) are to foundation ASNs. No non-foundation reference; no reinvention of foundation notation (`coverage`, `home`, `origin`, span/displacement algebra are all used, not redefined).

**Anti-bloat scan.** I checked for the named accretion patterns — phantom cases excluded by preconditions, relocated-not-removed findings, axiom-rationale sub-paragraphs, shared downstream deferrals, document-ordering justifications, consumer-enumeration in definitions, twinned paragraphs. The note has no new axioms; the "negative" lemmas (F-state/F-persist/F-origin/F-multidoc/F-slot) each state a distinct non-dependence, which the review standard explicitly classifies as legitimate, not meta-prose. The Nelson attribution in F-origin is design provenance and should be retained, not stripped. The six worked configurations each exercise a property no earlier configuration reaches (F-contig's interior clip in Config 5 and the vacuous-subspace branch in Config 6 are not redundant with Configs 1–4). The prior cycle's commit already trimmed the F-multi forward-reference and sharpened the concurrency open question; I found no residual accretion that survives at source.

The two open questions are legitimately forward-looking (cross-home resolution relationship; BEBE concurrency) and correctly sit in the Open Questions slot rather than defining out-of-scope claims.

I could not identify a load-bearing rigor gap, a missing boundary case, or accretion prose that obstructs the argument.

VERDICT: CONVERGED
