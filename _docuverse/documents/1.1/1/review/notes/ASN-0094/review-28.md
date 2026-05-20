# Review of ASN-0094

## REVISE

### Issue 1: Sh4 and FDD contract interaction at FDD-registered K is underspecified

**ASN-0094, FunctionalDependencyDiscipline section**: "the discipline is enforced by the layer at Emit time via the same Observe-then-Emit protocol used for the *Sh4 idempotency contract*, with the candidate-set restricted to from-slot match alone."

**Problem**: FDD requires `shape(K).idem = ⊤`, so the *Sh4 idempotency contract* also applies at every FDD-registered K. The framework documents each contract's ordering relative to Sh-conf gates (canonical-form gate → contract → cardinality/target-domain gate) but never specifies the ordering of Sh4 and FDD relative to each other. The framework establishes `C ⊆ C_fd`, but it is left unstated whether:
(a) Sh4's clause (i)-(iii) fires first, then FDD's (redundant but harmless when both succeed);
(b) FDD's clause (i)-(iii) supersedes Sh4's at FDD-registered K (only the stricter check runs);
(c) Both run in parallel.

FDD's preservation proof cites only the FDD contract — not Sh4 — to discharge Case B, suggesting reading (b), but the *Sh4 idempotency contract* introduction's text says Sh4 applies "uniformly across every reachable state" whenever idem = ⊤, suggesting reading (a) or (c). The runtime semantics matter for layers implementing the contracts, even though the framework's preservation outcome is identical regardless.

**Required**: Either explicitly state that FDD subsumes Sh4 at FDD-registered K (and that Sh4's contract is dormant at such K, despite the bare idem = ⊤ admission test), or specify the ordering between the two contracts at a single call site.

### Issue 2: RetractionTargetNotOnChain Case II's home-equality step compresses T4b structure

**ASN-0094, Lemma — RetractionTargetNotOnChain, Case II final step**: "Since `a` shares its first `#b` components with `b` (the prefix relation gives this directly) and `w` contributes no additional zeros, `a`'s three zero positions lie within positions `1..#b`, agreeing pointwise with `b`'s three zero positions. Hence `N(a) = N(b)`, `U(a) = U(b)`, `D(a) = D(b)`, so `home(a) = home(b)`."

**Problem**: The leap from "shared zero positions" to "N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)" requires citing T4b's positional index ranges (N occupies positions 1..n_1-1, U occupies n_1+1..n_2-1, D occupies n_2+1..n_3-1). The proof cites only L1a, which gives the formula `home(a) = N(a).0.U(a).0.D(a)` but does not directly establish that the three projections agree when zero positions coincide and componentwise agreement holds on the prefix. The reader must reconstruct: (i) T4b's index ranges for N, U, D; (ii) those ranges all lie within `1..n_3 - 1 ≤ #b - 1 < #b`; (iii) componentwise agreement on `1..#b` from `x ≼ a` therefore forces N(a) = N(b), U(a) = U(b), D(a) = D(b).

**Required**: Add an explicit step citing T4b's positional index ranges (or a brief inline derivation matching the worked example's mechanics). The AllocatedAddressAntichain proof handles the symmetric argument with full Step 3.1/3.2 unpacking; RetractionTargetNotOnChain's Case II would benefit from comparable detail.

### Issue 3: Provenance `to_K`'s exclusion of attribution-only tuples could be explained at the catalog row

**ASN-0094, Provenance walkthrough**: "`to_K(b) ≡ {τ ∈ A_K^Σ : to₁⁻(τ) = b}` (tuples with `to₁⁻(τ) = ⊥` are excluded because `⊥ ≠ b` for any `b ∈ A^Σ`)"

**Problem**: The catalog row table for Provenance lists `to_K` without comment, but the body's behavior differs from DirectedPair's `to_K` (which under c_G = 1 includes every tuple). A consumer reading the catalog row table — before drilling into the walkthrough — sees `to_K(b)` and might assume it inverts `to_K^Σ(τ) = slot_addrs(G)` for all τ; the asymmetry at `to₁⁻(τ) = ⊥` is buried in the walkthrough. The framework provides `outgoing_K` as the alias for full from-slot-indexed coverage, but the catalog row doesn't flag that `to_K` is the *target-indexed* accessor that necessarily excludes attribution-only tuples.

**Required**: Either annotate the catalog row's Provenance entry (e.g., "`to_K` excludes tuples with empty G-slot, by definition of target-indexed accessor"), or add a brief note at the row explaining the consequence of `c_G = 0|1` on `to_K`'s semantics — that "target-indexed" accessors are necessarily partial domain when G is partial.

### Issue 4: Sh4 Case B's qualifier framing is informational but invites confusion

**ASN-0094, Sh4 proof, Case B**: "*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with no concurrent nullification of any τ ∈ A_K^Σ).*"

**Problem**: The case-statement carries a qualifier ("no concurrent nullification") that is then immediately defused: "the qualifier's substantive content is fully absorbed by the case-decomposition." The decomposition argument (K ≁ R → automatic; K ~ R → routed to Case D) is correct, but the qualifier remains in the case heading where it appears to be a substantive precondition. A reader who reaches Case B without first reading the post-hoc explanation may think Case B is conditional and ask "what if concurrent nullification *did* occur during a K.λ-step at K ≁ R?" — a question whose answer is "impossible per ASN-0086's class-decomposition of `→`."

**Required**: Either remove the qualifier from the case heading (since the case-decomposition handles it structurally) or rewrite it as a structural restriction ("K.λ-step at type K with K ≁ R", which is what the decomposition enforces). The current formulation is technically correct but presents structural impossibilities as if they were preconditions.

### Issue 5: AllocatedAddressAntichain Step 3's symmetry claim could be tightened

**ASN-0094, AllocatedAddressAntichain Lemma, Case 3**: "*Case-symmetry across Sub-cases 3a and 3b.* Sub-cases 3a and 3b share the hypothesis `x ≼ a` and discharge Steps 3.1 and 3.2 identically... The two sub-cases diverge only at Step 3.3, where the subspace partition scaffolding clauses assign `E(·).1` based on domain membership..."

**Problem**: The symmetry claim is correct, but the proof then writes Step 3.3 explicitly for *both* sub-cases (3.3a and 3.3b), exhibiting effectively identical arguments with the side labels swapped. This is defensive but somewhat redundant given the symmetry claim. Either the symmetry claim suffices (and only one of 3.3a or 3.3b need be written, with the other noted by symmetry), or the symmetry claim is decorative and the two explicit derivations carry the real argument. The current structure does both, which makes the proof longer than necessary without strengthening it.

**Required**: Pick one structure — symmetry claim with single explicit sub-case OR two explicit sub-cases without redundant symmetry claim. The current "both" approach is technically correct but adds bulk.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate atomicity for layer-discipline contracts
**Why out of scope**: The framework explicitly commits to single-process substrates and flags multi-process consistency as a scope boundary in Open Questions. Cross-process race conditions between Sh4-emitters at coverage-equivalent K's would require a distributed coordination protocol; this is not the territory of a single-process framework spec.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: Sh-conf clause (d) requires `slot_addrs ⊆ t_·^Σ`, so unallocated (ghost) addresses are excluded from slot positions. The framework correctly flags this as a design choice in Open Questions. Admitting ghost-targeting slots would require a new state-dependent conformance rule and is appropriately deferred.

### Topic 3: Cross-process registry consistency
**Why out of scope**: Lifetime constancy of T_cat and `shape` is asserted as a single-process commitment. Distributed-substrate consistency would require a coordination protocol on the registry itself, which is outside this framework's scope.

### Topic 4: Document-level container targeting
**Why out of scope**: The framework provides no target-domain symbol for `dom(Σ.M)` addresses; container-level relations must be recorded against a content address within each container's element field. This is a structural limit clearly noted in the "Reach of the framework's target-domain symbols" sub-paragraph at the Canonical Shape Catalog. Extending the framework to admit container-level targeting would require introducing a fifth target-domain symbol and adapting Sh-conf clause (d) accordingly.

### Topic 5: Higher-arity links (N ≥ 4)
**Why out of scope**: The framework's `Link = {(e₁, ..., eₙ) : N ≥ 3}` admits higher-arity links, but the shape framework restricts to the arity-3 standard-triple slice `L^Σ`. The Scope and Substrate Scaffolding section explicitly notes this. Extending to higher arities would require additional shape components per extra slot and is appropriately deferred.

VERDICT: REVISE
