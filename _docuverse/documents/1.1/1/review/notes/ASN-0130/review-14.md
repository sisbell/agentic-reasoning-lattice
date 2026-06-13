# Review of ASN-0130

I reviewed this against the strand model, link ontology, allocation substrate, and the predicate-language stack (ASN-0126/0128/0129). I checked the hard claims rather than the easy ones: the born-nullified scoping of both emit surfaces, the substitution induction in PR3a, the acyclicity argument in PR2, both directions of the PR0 weakest precondition, the coverage-exactness derivation for the lint, and the aggregate-rule extension in PR5. They hold.

## REVISE

None.

For the record, the claims I expected to find skipped and did not:

- **PR3a substitution induction.** The WT-α / WT-W / PC2 chain is complete. Both weakening uses discharge their provisos (expansion-name binders disjoint from author names; `yⱼ ∉ dom(Γ)`; freshness against every `Eⱼ`), the simultaneous-to-sequential reduction is justified (no `yⱼ` in any `Eᵢ`), and "last parameter first" peels the context correctly. Type preservation `Γ ⊢ replacement : C_r` carries the host derivation through QD-node and domain positions via the blanket "every other node's WT rule is preserved," which is adequately general — a `℘_fin(T)`-valued reference in a reflected-domain slot re-types by the same sort-preservation.
- **PR2 acyclicity.** (a) instantiated at `e₁(D)` gives `e₁(r) < e₁(D)` correctly; (b) self-reference exclusion turns on canonical shaping under the discipline (all validated tuples at one start I0-equal, so a miss has no active witness for the self-edge). Unconstructibility of mutual recursion is sound.
- **PR0 wp, both directions.** The attainability convention is invoked consistently with I6; necessity genuinely needs canonical shaping (off-discipline counterexample is real), and `C2` drops out because `pdef ≁ R`. The scoping to registration-disciplined derivations is tight, not decorative.
- **PR5 aggregate extension.** PD0's per-rule soundness consumes only fixity of the threshold; a bound ℕ parameter is as fixed as a literal across a step, so extending the `count(D) ≥ c` / `≤ c` rules from "literal" to "bound value" is sound, and the worked `count(L_W) ≥ x` case confirms the gap it closes.
- **Coverage exactness for `is_pd_stable`.** Run-starts are pairwise prefix-incomparable (same-origin by NonNestingSiblingPrefixes; cross-origin by anchor incomparability + two-prefixes-comparable), so `t ∈ subtree(t')` between starts forces `t' = t`. The universal-lint vacuous-violation caveat is documented honestly.
- **`shift(x,1) = inc(x,0)`** on resident content addresses, hence "run = K.α chain segment," and PR0 (i)'s contiguity check are correct and content-intrinsic.

Foundation usage is clean (all citations resolve to 0034/0036/0043/0086/0093/0126/0128/0129; no non-foundation cross-references, no reinvented notation). On the anti-bloat pass: the prose is dense but load-bearing. The justificatory asides ("enforce-by-rejection … would be a lie," the certificate "lesson," the two-runs motivation) fall under the guidance's carve-outs for analogies, concrete examples, and statements of what an operation does; the "What this note commits" summary is a skippable abstract, not prose interrupting a claim. Nothing I had to work around to follow an argument.

## OUT_OF_SCOPE

### Topic 1: Version signature compatibility
PR4 reuses `supersedes` (S2) without requiring `sig(successor)` to be compatible with `sig(predecessor)` — a Bool predicate can be superseded by a `℘_fin(T)` definition, and `tip()` resolves regardless. The note correctly punts adjudication to readers and claims no signature preservation, so this is not an error here.
**Why out of scope**: A typed-versioning discipline (lineages constrained to one signature) is a new design commitment, a future ASN, not a defect in this one.

### Topic 2: A predicate-sort classifier for the unscoped universal lint
The note shows PL cannot narrow `M_pdef` to Boolean-sorted definitions (result sort is outside the read surface), so the unscoped `(A t ∈ M_pdef :: is_pd_stable(t))` is vacuously violated by any legitimately non-predicate definition. The per-definition atom is exact and the protocol-scoped filter works; only the global form carries the caveat, which is documented.
**Why out of scope**: Shipping a Unary "Boolean-definition" classifier to enable the narrowed lint is a new designated class — the catalog-growth question instantiated again, future territory.

VERDICT: CONVERGED
