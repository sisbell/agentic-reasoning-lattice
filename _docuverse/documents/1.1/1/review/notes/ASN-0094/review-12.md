# Review of ASN-0094

## REVISE

### Issue 1: `latest_K_for_addr` signature mismatch with body

**ASN-0094, NonIdempotentDirectedPair Coverage instantiation**: The accessor is given as

`latest_K_for_addr : A_doc → A_rel^Σ ∪ {⊥}`

with body `latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)`.

**Problem**: `argmax` returns an element of `S_d` — a tuple in `A_K^Σ`, not an address in `A_rel^Σ`. The Coverage walkthrough confirms the tuple return: "latest_K_for_addr(d_subject) = ... = τ_3 (chain-index 2). Reading the witness off the returned tuple: from₁(τ_3) = d_witness." If consumers read accessors off the returned value, the codomain must be the tuple set, not the address set.

**Required**: Either change the signature to `A_doc → A_K^Σ ∪ {⊥}` (or `L_K^Σ ∪ {⊥}`) to match the tuple return, or wrap the body in `addr(·)` and document that consumers must re-query `Σ.L` to recover slot accessors.

### Issue 2: Retraction row's base templates not formally defined

**ASN-0094, Canonical Shape Catalog table (Retraction row) and Per-Shape Template Walkthrough — Retraction**: The Retraction row claims base templates "inherited from `(*, 1, A, A_rel, ⊤)` per Sh5(b)" with parenthetical hints: "pair_K(F̂, b)", "from_K(a) (set-valued on the from-slot under c_F = *)", "to_K(b)", "from_addrs_K(b)", "to_addrs_K(a)".

**Problem**: The DirectedPair canonical base templates (the source pattern Sh5(b) is supposed to inherit from) are defined for `c_F = 1` and use `from₁` as a point accessor — `from_K(a) ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`. Under `c_F = *`, `from₁` is not defined; the natural reformulation is `from_K(a) ≡ {τ ∈ A_K^Σ : a ∈ slot_addrs(F_τ)}`, but the catalog only hints with "set-valued on the from-slot". Similarly `pair_K(F̂, b)` shifts from address-input to address-set-pattern-input without specifying the matching predicate (`F̂ ⊆ slot_addrs(F_τ)`? exact equality? coverage-containment?). Sh5(a) commits to hand-curating templates per shape — no such curation appears for this row.

**Required**: Provide explicit template bodies and signatures for the `(*, 1, A, A_rel, ⊤)` shape, parallel to the DirectedPair walkthrough's enumeration. Or explicitly note that the row's templates are deferred and downstream of R6's consumption.

### Issue 3: T_cat lifetime constancy not explicitly stated

**ASN-0094, Definition — ShapeRegistry and Definition — TypedRelationCatalog**: "shape : T_cat → Shape ... Lifetime constancy. shape is fixed across the substrate's lifetime; it does not change as states evolve. ... Mutable shape re-registration (e.g., relaxing a cardinality bound after some tuples are already emitted) would invalidate the induction; the framework forbids it."

**Problem**: The ASN states `shape`'s values are lifetime-fixed but is silent on whether `T_cat`'s domain is lifetime-fixed. Sh0–Sh3 inductions begin with the baseline "At Σ_0, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous." If `T_cat` may grow at runtime to admit a new `K'`, then for that `K'`, `L_{K'}^{Σ_init}` is not necessarily empty (prior class-(iii) emissions might have populated it before `K'` was registered). The inductive baseline would not hold for late-added types, and the proofs would silently fail.

**Required**: State explicitly whether `T_cat` is lifetime-fixed at `Σ_init`, or, if T_cat may grow, specify when the inductive baseline applies to a newly-added K (e.g., require `L_K^{Σ_registered} = ∅` at the registration point as a precondition for adding K to T_cat).

### Issue 4: Direct references to non-foundation ASNs

**ASN-0094, Scope and Substrate Scaffolding and Lemma — RetractionTargetNotOnChain proof**: Multiple direct references to ASN-0036 (`S0–S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ`) and ASN-0093 (`M0, M1, C0, C1, C1b, C1c, C-fin, ChainMembershipForOrigin, ChainEnumerationInjectivity, ChainUniformLength`, etc.) appear by number/property name — including "by S7d and M0 from ASN-0093" in the RetractionTargetNotOnChain proof.

**Problem**: Per review Standard 7, only the listed foundations (ASN-0034, ASN-0043, ASN-0086) are admissible as direct cross-references. References to ASN-0036 and ASN-0093 break self-containment. While `ASN-0086`'s `SubstrateConformingLayer` Definition (which is foundation here) enumerates these invariants by name, ASN-0094's proofs also cite them directly, going outside the foundation interface.

**Required**: Either restructure the dependencies to consume ASN-0036/0093 only through ASN-0086's exported `SubstrateConformingLayer` predicate (treating individual invariants as opaque inside that bundle), or surface the specific properties needed (e.g., "every document address has zeros = 2", "every link sub-allocator emits in a forward-ordered chain") as named scaffolding clauses without attributing them to a numbered upstream ASN.

### Issue 5: Sh4 Case A enumeration omits a covered sub-case

**ASN-0094, Sh4 — IdempotencyDiscipline, inductive step Case A**: "This case covers all K.σ-steps and K.α-steps ... all K.λ-steps emitting a tuple of any type K' with K' ≁ K and K' ≁ R (so L_K and nullified are both untouched at K), and all arrangement-modifying steps in ↦ \ →."

**Problem**: The enumeration's exclusions "K' ≁ K and K' ≁ R" omit the scenario where K' ~ R and K ~ R, with τ_new self-targeting (its G covers `addr(τ_new)`) and no prior R-tuples exiting. Under that sub-case, `L_R` extends with `τ_new` and `nullified` gains `addr(τ_new)`, but `τ_new ∉ A_R^{Σ'}` (filtered out) and no prior `A_R^Σ` element exits, so `A_R^{Σ'} = A_R^Σ` — satisfying Case A's defining equation. The case definition covers this scenario, but the prose enumeration does not. Separately, this sub-case is structurally impossible under Sh-conf clause (d) (since `τ_new`'s G would need to target the to-be-allocated fresh address, which is not in `A_rel^Σ`), but the proof's enumeration does not invoke this exclusion.

**Required**: Either extend the enumeration to include the K=R + self-retraction-only sub-case, or explicitly note that (a) the enumeration lists exemplary transitions while the case is defined by the equation `A_K^{Σ'} = A_K^Σ`, and (b) self-retraction is structurally precluded by Sh-conf clause (d).

### Issue 6: AllocatedAddressAntichain hypothesis under-specified

**ASN-0094, Lemma — AllocatedAddressAntichain**: "For every reachable state `Σ` and every `x ∈ A^Σ`: `cov_allocated({(x, δ(1, #x))}, Σ) = {x}`."

**Problem**: Case 3 of the proof requires `zeros(x) = 3` and `#E(x) ≥ 1` (i.e., `x` is element-level with a non-empty element field). These hold for any `x ∈ A^Σ` because `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is entirely element-level (by L1 for the link side and the content-side scaffolding for the content side), but the statement does not make this dependency explicit. The span `(x, δ(1, #x))`'s well-formedness via T12 also presumes `#x ≥ 1`, which is implicit in `x ∈ T`.

**Required**: State the implicit hypothesis explicitly — either "For every reachable Σ and every element-level x ∈ A^Σ (zeros(x) = 3, #x ≥ 1)" or add a parenthetical noting that A^Σ's element-level character follows from L1 + scaffolding.

## OUT_OF_SCOPE

### Topic 1: Composite predicates closure theorem
**Why out of scope**: The ASN explicitly acknowledges no closure theorem is established for composition. Establishing what predicates the compositional language can/cannot express is genuinely new work, not a gap in this ASN.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: The ASN flags this as an open question. Admitting ghost addresses (currently outside A^Σ) as slot targets requires a new conformance rule and likely new shape components.

### Topic 3: Cross-process shape registry consistency
**Why out of scope**: Lifetime constancy is stated as a single-process commitment. Distributed-substrate concurrency for shape registration is genuinely new territory.

### Topic 4: Bipartite catalog completeness
**Why out of scope**: The ASN notes "the current catalog enumerates the rows demanded by present-day predicate templates; further bipartite entries can be added by extending the catalog." Filling in absent bipartite rows (e.g., Tuple-DirectedPair for `(1, 1, A_rel, A_rel, ⊤)`) is future catalog extension, not an error in this ASN.

VERDICT: REVISE
