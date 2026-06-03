# Review of ASN-0070

I checked the F-canonical proof through every step (including the newly added vacuous-subspace Step 0), the Step 1 action-point case split, the Step 2 consecutivity characterisation, the Step 3/4 existence-uniqueness bridge, all six worked configurations, the wp analysis, and the derived-property lemmas. I also ran the requested forward-reference / anti-bloat pass.

## REVISE

(none)

The substantive items I looked for are all discharged:

- **F-canonical completeness.** Step 1's case split on `k = actionPoint(ℓ)` is jointly exhaustive (`1 ≤ k < m` excluded by infinite `⟦σ⟧_V` vs. finite `R`; `k = m` proved by mutual inclusion). Step 2's consecutivity characterisation proves both directions, with the reverse done by full induction and closed at position `m` via T0 discreteness. Step 4 bridges `⟦·⟧_V → ⟦·⟧` directly (maximal-run reconstruction with both right- and left-closure), so S9 is not hand-waved.
- **Edge cases exercised concretely.** Empty resolution (Config 2), vacuous link subspace (Config 6), within-document multiplicity (Config 4), interior-offset clip `j > 0, c < n` (Config 5), cross-subspace straddle with both result components non-empty (Config 4), multi-document (Config 6). The `X = ∅`-in-populated-subspace case is handled (F-empty derivation, dispatched by subspace status). All six configurations are numerically consistent with `δ`-displacement arithmetic.
- **wp analysis is non-trivial.** It unpacks well-definedness of `L(ℓ).eᵢ`, `M(d)`, `coverage`, and the subspace projection, recovering exactly the three stated preconditions; the frame's `wp = true` is correctly justified.
- **Foundation usage.** All cross-ASN citations are to the listed foundation ASNs (0034/0036/0043/0047/0053/0058); no non-foundation ASN is referenced in the body (the ASN-0093 mentions live only inside the quoted ASN-0047 foundation text, not in this note). No reinvented notation — `subspace_I`, `coverage`, `home`, `δ`, `shift`, T12, S8/S9 are used from foundations.

**Anti-bloat pass.** I specifically checked the flagged patterns: redundant vacuous-subspace explanation appears in four locations (V-Restricted Denotation, F-canon-form, F-canonical Step 0, F-empty), but each is a distinct role — definition, shape clause, theorem discharge, application — not restatement; Step 0 closes a real existence/uniqueness gap (the theorem's "exactly one" claim is otherwise undefined when `m_S(d)` is undefined), so it is load-bearing, not accretion. The roadmap sentences ("we dispatch... then treat...", "Steps 1 and 2 constrain the shape... we now exhibit one") are proportionate to a genuine five-step proof. The F-origin Nelson sentence and F-multidoc's `home`-aside are significance/analogy content, which the guidance protects. No skippable meta-prose obstructs a claim.

## OUT_OF_SCOPE

The note's own Open Questions (multi-home resolution relationship across transcluding documents; BEBE multi-server traversal consistency) are correctly deferred — multi-home is future territory, BEBE is explicitly out of scope.

VERDICT: CONVERGED
