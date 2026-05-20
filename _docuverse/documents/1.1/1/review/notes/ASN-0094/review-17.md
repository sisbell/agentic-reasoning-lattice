# Review of ASN-0094

## REVISE

### Issue 1: "Content-side scaffolding" name covers more than content

**ASN-0094, Scope and Substrate Scaffolding**: The section's bullet list is labeled "content-side scaffolding" and self-references appear throughout the body (e.g., "(content-store finiteness scaffolding for `dom(Σ.C)`)"). But of the ten clauses, four are link-side (Link subspace partition, Per-document link sub-allocator chains, Uniform link sub-allocator chain length, Link sub-allocator chain-index function) and one is document-side (Document address structure).

**Problem**: The label is misleading; downstream proofs cite "the content-side scaffolding" when invoking link-side facts (e.g., RetractionTargetNotOnChain Case I uses the *Uniform link sub-allocator chain length* clause).

**Required**: Rename to "substrate-conforming-layer scaffolding" or "the scaffolding clauses", and update self-references throughout (Scope section, AllocatedAddressAntichain proof, Lemma — RetractionTargetNotOnChain, Coverage walkthrough, Properties Introduced table).

### Issue 2: Retraction catalog row's primary-consumption wording

**ASN-0094, Canonical Shape Catalog table, Retraction row**: "*primary consumption:* by R6's active-subset definition (`nullified(·)` reads `to_K`'s coverage)".

**Problem**: `to_K(b)` is defined in the Retraction walkthrough as `{τ ∈ A_K^Σ : to₁(τ) = b}` — ranging over the *active* subset `A_R^Σ`. But ASN-0086's `nullified(Σ)` reads `coverage(G')` over `L_R^Σ` (audit slice), explicitly committed by R6b's "audit-slice reading (adopted)". An active-subset reading would create the recursive fixpoint R6b rejects. The parenthetical equates two notions that R6b distinguishes.

**Required**: Rephrase to reflect the audit-slice semantics, e.g., "primary consumption: by ASN-0086's nullified definition, which reads each L_R-tuple's G-coverage directly over the audit slice (not via the active-subset `to_K` accessor)".

### Issue 3: Retraction's pair_K signature departs from the other catalog rows without justification

**ASN-0094, Per-Shape Template Walkthroughs, Retraction**: `pair_K(F̂, b)        ≡ (E τ ∈ A_K^Σ :: slot_addrs(F_τ) = F̂ ∧ to₁(τ) = b)`.

**Problem**: Every other catalog row's `pair_K(a, b)` takes two *addresses* — even Provenance's, where the to-slot may be empty (its body checks `to₁⁻(τ) = b` against an address `b`). Retraction's `pair_K` switches its first argument to an *address-set pattern* `F̂` checked by exact set equality, while `from_K(a)` on the same row uses membership `a ∈ slot_addrs(F_τ)`. The asymmetry — set-equality at `pair_K`, set-membership at `from_K` — is asserted (in the paragraph beginning "The four set-valued templates take an *address* on the from-side") but no derivation establishes why Sh5(b)'s mechanical generation forces this divergence; another reading would be `pair_K(a, b) ≡ (E τ :: a ∈ slot_addrs(F_τ) ∧ to₁(τ) = b)`, matching the membership semantics used elsewhere on the row.

**Required**: Either (a) derive the set-equality reading from the shape components plus Sh5(b)'s discipline (showing that membership would be ill-typed or redundant with `from_K`), or (b) document this as a deliberate role-specific design choice in the catalog row, distinguishing it from the mechanically-derived bodies and noting that the choice is permitted because Retraction's `c_F = *` makes "exact pattern match" the only operational reading of "is there a tuple with this attribution".

### Issue 4: Sh5(b) discipline statement is unfalsifiable as written

**ASN-0094, Template Catalog (Sh5)**: "(b) META discipline. This framework's catalog adheres to the rule that every catalog row's templates depend only on (i) the shape components, (ii) K's name, and (iii) explicitly named layer-supplied accessors registered in the row's opt-in or parametric columns".

**Problem**: The discipline is offered as the criterion by which the catalog is falsifiable, but no procedure is given to check whether a candidate template "depends only on" the three permitted inputs. The Coverage walkthrough's `latest_K_for_addr` consumes `emission_order`, which is defined as `chain_index(addr(τ), d_K)` — but `d_K` is bound by SingleHomeCoverageDiscipline (per-K data), and `chain_index` is a scaffolding clause not registered in the catalog row's "opt-in" column. By the criterion's literal reading, this template fails the discipline. The walkthrough waves at this with "secured by SingleHomeCoverageDiscipline" but the discipline column lists the discipline, not the scaffolding clause, leaving the criterion's "explicitly named" requirement ambiguous.

**Required**: Either spell out the criterion precisely (what counts as "explicitly named" — discipline registrations only, or scaffolding clauses too?), or strengthen the catalog row to list every scaffolding clause each template consumes.

### Issue 5: Sh-conf return-type extension creates an unfixed boundary with ASN-0086

**ASN-0094, Sh-conf section**: "The framework extends ASN-0086's `Emit_K` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` where `⊥` is a distinguished rejection token".

**Problem**: ASN-0086's `Emit_K` definition specifies the return type `Σ' × A_rel^{Σ'}` with no ⊥-case. Callers within ASN-0086's scope (the relational layer's other operations, e.g., `Nullify`'s aliasing as `Emit_R(...)`) assume the bare return type. The framework's extension is announced but no audit is performed against ASN-0086's existing callers — `Nullify` in particular invokes `Emit_R`, and ASN-0086's `Nullify` postcondition assumes a `Σ'` is produced. Under Sh-conf rejection at unregistered R, every `Nullify` call returns ⊥, leaving ASN-0086's `Nullify` postcondition unmet.

**Required**: Either (a) add an explicit clause that Sh-conf cannot reject `Nullify`-routed `Emit_R` calls (justified by the baseline R-registration requirement plus the substrate's structural admission of well-formed Nullify), or (b) declare that the framework's preservation theorems apply only to substrates where R is registered, and reframe ASN-0086's `Nullify` postcondition accordingly.

### Issue 6: AllocatedAddressAntichain Sub-case 3 invokes Step 3.2's conclusion `E(x) ≼ E(a)` but uses only the first index

**ASN-0094, AllocatedAddressAntichain proof, Step 3.2**: "With `#E(x) ≤ #E(a)` and componentwise agreement on `1 ≤ j ≤ #E(x)`, the Prefix definition (ASN-0034) gives `E(x) ≼ E(a)`. In particular, taking `j = 1`, `E(x).1 = E(a).1`."

**Problem**: The proof goes through Prefix to derive `E(x) ≼ E(a)` and then takes the first-position conjunct. This is more than needed — `E(x).1 = E(a).1` follows directly from componentwise agreement at `i = n_3 + 1` (taking `j = 1` in T4b's index offset). The Prefix derivation introduces an unnecessary step that requires `#E(x) ≥ 1` (which the proof carefully establishes via T4(iv)), when in fact only componentwise agreement at one position is consumed. The careful T4(iv) derivation establishing `#E(x) ≥ 1` is load-bearing for the Prefix step but not for the actually-needed `E(x).1 = E(a).1`; a future reader will not be able to tell which step is essential.

**Required**: Either (a) drop the Prefix step and derive `E(x).1 = E(a).1` directly from componentwise agreement at position `n_3 + 1` of `x ≼ a` plus T4b's index offset, or (b) note explicitly that the Prefix derivation is bookkeeping that documents the relation between E-fields without being load-bearing for the contradiction.

### Issue 7: RetractionTargetNotOnChain Case II asserts "TA5(c) with k = 0 ... or equivalently, T10a.8" but the equivalence is not exact

**ASN-0094, Lemma — RetractionTargetNotOnChain, Case II**: "in the subsequent-emission branch `a_emit(Σ, d) = inc(ℓ_prev, 0)` preserves `zeros` (TA5(c) with `k = 0`, ASN-0034, modifies only position `sig(ℓ_prev)`, and on T4-valid `ℓ_prev` that position is the last with non-zero value, whose incremented value remains non-zero — equivalently, T10a.8, UniformSiblingZeroCount, ASN-0034)".

**Problem**: TA5(c) at `k = 0` modifies position `sig(ℓ_prev)` from `t_{sig(t)}` to `t_{sig(t)} + 1`. T10a.8 is stronger: it concludes that across the *entire* sibling chain produced by repeated `inc(·, 0)`, every sibling has `zeros(tₙ) = zeros(t₀)`. The lemma needs only the single-step preservation that TA5(c) supplies — not T10a.8's chain-level conclusion. Calling these "equivalent" is imprecise: TA5(c) is the per-step fact; T10a.8 is the closure. The latter consumes the former plus T10a.4 plus T4(iv). The "equivalently" suggests they're interchangeable at the proof site, but the proof uses only the per-step reading.

**Required**: Replace "equivalently, T10a.8" with the single citation appropriate to the proof: either TA5(c) alone (with the inline argument that the modified position's incremented value remains non-zero given T4-validity of `ℓ_prev`), or T10a.8 alone (consumed at the appropriate generality). Don't claim both for the same step.

### Issue 8: "Layer commitment" is used to refer to four distinct things

**ASN-0094, throughout**: The phrase "the layer commitment" or "layer-discipline contract" appears for (a) the framework's Emit_K routing requirement, (b) the Sh4 contract, (c) the FDD contract, and (d) the SingleHomeCoverageDiscipline commitment, with additional reference to (e) ASN-0086's "unit-depth retraction discipline". The Sh4 preservation proof's Case B says "By the layer commitment (Scope and Substrate Scaffolding), this K.λ-step originates as an `Emit_K` call" — meaning (a); then continues "By contract clause (iii)" — meaning (b).

**Problem**: Five distinct commitments share overlapping nomenclature. A reader reaching, e.g., the FDD preservation theorem's Case B clause "By the layer commitment, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By the FDD contract clause (iii)..." must hold two different "layer commitments" simultaneously without distinct names.

**Required**: Introduce explicit names: "the Emit_K routing commitment" for (a), "the Sh4 idempotency contract" for (b), "the FDD functional-dependency contract" for (c), "the single-home commitment" for (d), and use these consistently. The framework's commitments are non-interchangeable, and conflating them obscures which commitment is being invoked where.

### Issue 9: Worked Example "Rejection case 4" example uses K_ghost ∈ T_admissible but example shape parameters not stated

**ASN-0094, Worked Example: K = comment, Rejection case 4**: "Let `K_ghost ∈ T_admissible \ T_cat` be a non-empty type endset that has not been registered with the catalog... Sh-conf's first conjunct `K_ghost ∈ T_cat` is *false* at the literal-membership test against the registered catalog. The emission is rejected at this gate; `Emit_K` returns `⊥`."

**Problem**: The example claims rejection at the `K ∈ T_cat` gate, but never specifies the registered catalog T_cat for this walkthrough. From earlier in the walkthrough, T_cat must include `comment` (the example's K) and `K_res` (the resolver) and `R` (mandatory baseline). Nothing has explicitly stated which other Ks are or are not registered. The reader cannot verify that `K_ghost` is actually outside the catalog without an explicit list. The rejection is asserted but the precondition (`K_ghost ∉ T_cat`) is stipulated, not derived from a stated registration set.

**Required**: At the start of the worked example, list `T_cat = {comment, K_res, R, …}` explicitly so that "K_ghost ∉ T_cat" is verifiable from the example's setup. Otherwise the rejection case is a tautology ("we assume the type isn't registered, and observe that unregistered types are rejected").

### Issue 10: Sh4 preservation proof's Case A residual scenario is dispatched but its enumeration is incomplete

**ASN-0094, Sh4 preservation Case A**: "One residual scenario falls under Case A by the case-equation but is *not* listed in the principal-transitions enumeration: `K ~ R` together with a τ_new whose G-coverage targets `addr(τ_new)` (self-retraction-only, no prior R-tuple exits)".

**Problem**: This residual is the only one enumerated, but the framework offers no argument that it's the *only* residual. Consider another residual: `K ~ R` with τ_new whose G-coverage targets multiple addresses, of which exactly one is in `A_R^Σ` and is itself τ_new's fresh address. Or: an `Emit_R` step where the entire `leaving` set equals `{τ_new}` (impossible since τ_new wasn't in A_R^Σ pre-step, but conceptually analogous). The proof's claim that "the principal-transitions enumeration above is exhaustive in practice, with the case-equation acting as the formal closure" leans on the case-equation `A_K^{Σ'} = A_K^Σ` as the operative criterion — but then the residual analysis is unnecessary; either the case-equation closes the case, or it doesn't.

**Required**: Either (a) drop the residual analysis and rely solely on the case-equation `A_K^{Σ'} = A_K^Σ` (since the IH plus this equation suffices), or (b) prove that the listed residual is the unique non-principal scenario under the case-equation. The current text occupies an awkward middle: it acknowledges the case-equation is the formal closure but still enumerates a particular residual without exhausting them.

### Issue 11: SingleHomeCoverageDiscipline preservation is not separately proved

**ASN-0094, SingleHomeCoverageDiscipline**: The discipline commits that every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K`. The Coverage walkthrough's `latest_K_for_addr` consumes this through `emission_order`.

**Problem**: Unlike Sh4 and FDD, SingleHomeCoverageDiscipline is not accompanied by a preservation theorem. The discipline is asserted as a registration constraint, but no inductive proof shows that the discipline holds at every reachable state (in the sense that no Emit_K call for K-tuples ever uses a home `d ≠ d_K`). The catalog row presents `latest_K_for_addr` as enabled by the discipline, but the discipline's enforcement protocol is not specified.

**Required**: Either (a) add a preservation theorem analogous to Sh4 and FDD — specifying the layer-discipline contract for SingleHomeCoverageDiscipline (e.g., the layer rejects `Emit_K(Σ, d, F, G)` with `d ≠ d_K`) and proving inductively that under the contract, all K-emissions use home `d_K` — or (b) explicitly note that SingleHomeCoverageDiscipline is a precondition on the registration commitment with no inductive content, and that the catalog row's `latest_K_for_addr` template assumes the layer enforces single-home emission at each call site.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate concurrency

The Sh4 and FDD contracts are scoped to single-process substrates. Multi-process substrates would require a coordination protocol at the `~`-equivalence class scope.

**Why out of scope**: Acknowledged in Open Questions; designing distributed coordination protocols is properly a separate ASN.

### Topic 2: Schema evolution

`T_cat` is fixed at `Σ_init` and lifetime-constant. Adding new typed relations dynamically (after the framework's preservation theorems are in effect) is not addressed.

**Why out of scope**: The framework explicitly chooses lifetime-constant `T_cat` to discharge Sh0–Sh4 inductive baselines. Schema evolution is a separate design problem.

### Topic 3: Ghost-targeting slot semantics

The framework rejects emissions whose slot addresses target tumblers outside `A^Σ`, even though L9 (ASN-0043) admits ghost spans in endsets generally.

**Why out of scope**: Acknowledged in Open Questions as a future design choice.

### Topic 4: Composite shapes (one slot's content constrained by another relation's content)

Whether such shapes need a new restriction axis or decompose into existing primitives.

**Why out of scope**: Acknowledged in Open Questions.

VERDICT: REVISE
