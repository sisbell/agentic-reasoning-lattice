# Review of ASN-0098

## REVISE

### Issue 1: Project function precondition absent from formal definition box
**ASN-0098, "The Projection Operation"**: The formal box reads
`project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`
**Problem**: For `Σ.M(d)` to be defined, `d ∈ dom(Σ.M)` is required. The surrounding prose says "a document `d ∈ dom(Σ.M)`" but the formal definition box does not state this precondition. By contrast, `discoverable_from` explicitly carries "defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`". This asymmetry creates an interpretation gap in LP8, where `project(e, d_new, Σ')` is invoked when `d_new ∈ dom(Σ'.M)` but `d_new ∉ dom(Σ.M)` — the function is well-defined at Σ' but undefined at Σ. The behaviour for unregistered documents is not stated anywhere.
**Required**: Add the precondition `d ∈ dom(Σ.M)` to the formal project definition box, matching the discoverable_from style. Alternatively, state a convention (e.g., `project(e, d, Σ) = ∅` when `d ∉ dom(Σ.M)`) and apply it consistently.

### Issue 2: LP10 boundary case — K.μ⁻ contracting to empty arrangement
**ASN-0098, LP10**: K.μ⁻ admits retention `n'_S = 0` for both subspaces (satisfying the strict-shrink clause from a non-empty pre-state), producing `dom(Σ'.M(d)) = ∅`.
**Problem**: The lemma holds vacuously in this case — the projection becomes empty for every endset, and the exact-difference formula reduces to the entire pre-state projection — but this boundary is never acknowledged. The ASN's standards demand boundary case coverage; "empty document" should be explicit, not derivable by careful reading.
**Required**: Add explicit note that when K.μ⁻ contracts to the empty arrangement, `project(e, d, Σ') = ∅` for every endset `e`, and the exact-difference formula yields `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)`. Mention that this case is admitted by the K.μ⁻ precondition whenever the pre-state has at least one position.

### Issue 3: LP16 statement informally phrased
**ASN-0098, LP16**: "If a document `d_new` transcludes content from another document `d_src`... then every link discoverable from `d_src` via those I-addresses is also discoverable from `d_new` via the corresponding V-positions in `d_new`."
**Problem**: Pure English with no formal symbols. The qualifier "via those I-addresses" is not defined precisely. The proof works against a more precise condition (`a* ∈ ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new))`) than the statement reads. Every other lemma in the ASN is formally stated; LP16 should match.
**Required**: Restate formally — for any link `a ∈ dom(Σ.L)` and slot `i ∈ {1, …, |Σ.L(a)|}`, if `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new)) ≠ ∅` at state Σ, then both `discoverable_from(a, d_src, Σ)` and `discoverable_from(a, d_new, Σ)` hold.

### Issue 4: LP19 multi-state chain obscures the lemma content
**ASN-0098, LP19**: The lemma names five distinct states (`Σ_e`, `Σ`, `Σ_post`, `Σ_n`, `Σ_{n+1}`) connected by two chains `Σ_e →* Σ →* Σ_post` and `Σ_post →* Σ_n → Σ_{n+1}`.
**Problem**: The state ordering is correct but obscures the actual content. The lemma bundles two distinct claims: (a) allocations preserve tightness exclusion (a_new ∉ coverage), and (b) consequent arrangement doesn't grow projection. The reader must track which "Σ" symbol carries which role, and the auxiliary "Σ_n", "Σ_{n+1}" are only used to bridge the two claims.
**Required**: Either split into two lemmas — (a) "fresh allocation falls outside tight coverage" stated against `Σ_e →* Σ → Σ_post` alone, and (b) "consequent arrangement preserves projection bounds" as a corollary applied at any later K.μ⁺ step — or simplify the chain notation by eliminating one of the intermediate states.

### Issue 5: LP12 existential lift left implicit
**ASN-0098, LP12 proof**: The two-sentence proof establishes the per-slot biconditional `project(a, i, d, Σ) ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` but does not explicitly bridge from per-slot to the existentially-quantified biconditional that LP12 actually states. The reader must supply the elementary lift.
**Problem**: Proof completeness — "trivial" lifts should still be acknowledged. The proof says "Direct from definitions" then derives per-slot equivalence; it should also note the existential-quantifier lift and the unfolding of `discoverable_from`.
**Required**: Add one sentence: "By per-slot biconditional, `(E i : project(a, i, d, Σ) ≠ ∅) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` follows; unfolding the left side via the discoverable_from definition completes the biconditional."

## OUT_OF_SCOPE

The Open Questions section appropriately identifies items belonging to future ASNs (reverse discovery primitive, V-order preservation under K.μ~, cross-link endset semantics, partial allocation interaction, replication confluence, fork-composite link-subspace projection). No additional items to flag.

VERDICT: REVISE
