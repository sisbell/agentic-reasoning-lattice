# Review of ASN-0094

## REVISE

### Issue 1: `K_sidecar_of` well-definedness incorrectly attributed to Sh4

**ASN-0094, Attribute walkthrough**: "K_sidecar_of(d) requires Sh4 enforcement on the candidate set `{τ ∈ A_K^Σ : from₁(τ) = d}`: under Sh4, the set is empty or singleton, so the value-returning template is well-defined."

**Problem**: Sh4 enforces pairwise distinctness of `(slot_addrs(F), slot_addrs(G))` pairs, not pairwise distinctness of `slot_addrs(F)` alone. Concrete counterexample: with K = Attribute (shape `(1,1,A_doc,A_doc,⊤)`), emissions `Emit_K(Σ, h, {(d,δ₁)}, {(s₁,δ₂)})` and `Emit_K(Σ', h, {(d,δ₁)}, {(s₂,δ₃)})` with `s₁ ≠ s₂` both pass Sh4's contract (different `G`-slots → distinct slot-pairs → `C(F,G,Σ') = ∅` at the second call). The result is `A_K^{Σ''} = {τ₁, τ₂}` with `from₁(τ₁) = from₁(τ₂) = d` and `to₁(τ₁) ≠ to₁(τ₂)`. So `{τ ∈ A_K^{Σ''} : from₁(τ) = d}` has cardinality 2, not 0 or 1. K_sidecar_of(d) is ill-defined even with Sh4 fully enforced.

**Required**: Either (a) remove `K_sidecar_of` from Attribute's template family, leaving only `K_sidecars_of`; (b) register a stronger per-K discipline ("at-most-one-to-slot per from-slot value") and condition `K_sidecar_of` on it, distinct from Sh4; or (c) qualify the existing wording to acknowledge that the singleton conclusion needs a stronger discipline than Sh4. The same issue propagates to `K_is_fresh` under Layer Composites, which calls `K_sidecar_of(d)`.

### Issue 2: Sh4 proof's case-split misses the mixed K = R scenario

**ASN-0094, Sh4 proof**: Cases A (`A_K^{Σ'} = A_K^Σ`), B (`A_K^{Σ'} = A_K^Σ ∪ {τ_new}`), C (`A_K^{Σ'} ⊆ A_K^Σ` strictly).

**Problem**: When `K = R` and an `Emit_R`-step fires, two effects compose simultaneously: τ_new joins `A_R` (if not self-retracting), and other R-tuples whose addresses lie in `coverage(G_{τ_new})` leave `A_R`. The resulting `A_R^{Σ'} = (A_R^Σ \ leaving) ∪ {τ_new}` is neither A, nor B, nor C. The proof never addresses this mixed case explicitly. The conclusion still holds (the surviving tuples' pairwise distinctness is inherited; τ_new is slot-pair-distinct from all of A_R^Σ ⊇ survivors), but the argument is missing.

**Required**: Restructure the case-split, or add an explicit Case D covering simultaneous addition and contraction, with a one-line argument that pairwise distinctness on `(A_R^Σ ∪ {τ_new}) \ leaving` follows from pairwise distinctness on `A_R^Σ ∪ {τ_new}` restricted to the subset.

### Issue 3: References to non-foundation ASNs

**ASN-0094, SubstrateConformingLayer Definition and Coverage walkthrough**: "*ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ." and "*ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin." and "ChainMembershipForOrigin (ASN-0093)" and "ASN-0093's R0a-Cor1 and FreshEmissionAddress".

**Problem**: ASN-0036 and ASN-0093 are not in the foundation list (ASN-0034, ASN-0043, ASN-0086). The content-side scaffolding section does inline the relevant properties as local assumptions, which is the right discipline, but the SubstrateConformingLayer definition still enumerates non-foundation invariants by source-ASN reference, and the Coverage walkthrough cites ASN-0093 claims directly.

**Required**: Replace the "ASN-0036/ASN-0093 invariant lists" with abstract names for the substrate-conforming-layer interface (the scaffolding bullets already do this well). Replace direct ChainMembershipForOrigin / R0a-Cor1 / FreshEmissionAddress references with either foundation citations (ASN-0086 contains R0a-Cor1 and FreshEmissionAddress already) or restated local assumptions.

### Issue 4: Sh4 contract atomicity scope is wrong-grained

**ASN-0094, Sh4 contract**: "the layer commits to executing clauses (i)–(iii) atomically with respect to other Sh4-emitters at the same K"

**Problem**: `L_K` is `~`-class indexed: `L_K = L_K'` whenever `K ~ K'`. Two concurrent emitters using `Emit_K` and `Emit_{K'}` at distinct-but-`~`-equivalent type indices write to the same active subset and can race. Atomicity "at the same K" admits this race.

**Required**: Restate as "at the same `~`-equivalence class of K." One-word fix.

### Issue 5: Shape syntactic well-formedness underspecified

**ASN-0094, Shape Definition**: "Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-` (used when the corresponding cardinality is `0`)."

**Problem**: The parenthetical hints that `t_F = -` requires `c_F = 0`, but this is not posited as a well-formedness constraint. Conversely, the syntax admits `(c_F = 0, t_F = A_doc)` — observationally equivalent to `(c_F = 0, t_F = -)` (both make Sh-conf clause (d) vacuous on F) but syntactically distinct. Per-class constancy and downstream catalog reasoning assume a canonical form.

**Required**: Add explicit well-formedness: `t_F = - ⟺ c_F = 0`, and symmetrically for G. Without this, two registry entries with the same operational meaning can disagree on the registered shape value, breaking the per-class-constancy clause.

### Issue 6: Attribute and Citation share structural shape but list disjoint templates

**ASN-0094, Canonical Shape Catalog**: Attribute = `(1, 1, A_doc, A_doc, ⊤)`, Citation = `(1, 1, A_doc, A_doc, ⊤)` — identical tuples.

**Problem**: Sh5 says "for each canonical shape `Sh_canon`, the shape framework specifies a hand-curated template family." If Attribute and Citation share the same `Sh_canon`, they share the same template family. But the catalog lists them with different templates: `has_K / K_sidecar_of / K_sidecars_of` vs. `cites_K / K_incoming`. The frameworks's structural rigor requires identical shapes to produce identical template families; the differing template lists are naming conventions for *consumers*, not structural derivations from the shape.

**Required**: Either (a) merge Attribute and Citation into a single canonical shape entry with the union of templates exhibited under role-neutral names (`by_from`, `by_to`, `pair_exists`, etc.); or (b) introduce a distinguishing shape component (e.g., a "naming intent" tag) that justifies separate template families. Currently the catalog presents two rows whose structural specs are identical but whose template families are presented as disjoint — inconsistent with Sh5's per-shape-derives-template-family claim.

### Issue 7: Sh1 proof says "Symmetric to Sh0" with no exhibited substitution

**ASN-0094, Sh1 proof**: "Symmetric to Sh0, with the same two-case induction over `↦*`."

**Problem**: While `F` and `G` are symmetric in the Sh-conf clauses (a)/(b) and (c), Dijkstra-style review does not accept "symmetric" without exhibiting the substitution. Sh0's argument cites Sh-conf clause (a) for canonical-slot form of F; the corresponding Sh1 step cites clause (b) for G. The cardinality match in Sh0 reads `match(|slot_addrs(F)|, c_F)`; in Sh1 it reads `match(|slot_addrs(G)|, c_G)`. The symmetry is real but should be witnessed by naming the clauses substituted.

**Required**: Replace "Symmetric to Sh0" with a one-paragraph proof that names Sh-conf clauses (b) and (c) explicitly at the corresponding sites.

## OUT_OF_SCOPE

### Topic 1: Cross-process shape registry consistency
**Why out of scope**: Acknowledged in Open Questions. Substrate-process boundary is downstream of this ASN's single-process framework.

### Topic 2: Composite shape framework (shapes whose slots are constrained by other relations)
**Why out of scope**: Acknowledged in Open Questions. Requires a new restriction axis not present here.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Acknowledged in Open Questions. L9 admits ghost spans generally; the shape framework's restriction to allocated slot-targets is intentional for this ASN.

### Topic 4: `(0, 0)` shapes
**Why out of scope**: Acknowledged in Open Questions. Pure existence markers; their utility is a downstream design question.

### Topic 5: Whether idempotency derives from cardinality + target-domain
**Why out of scope**: Acknowledged in Open Questions. The catalog empirically supports independence (Comment vs. Citation), but a proof would require a new axis of analysis.

VERDICT: REVISE
