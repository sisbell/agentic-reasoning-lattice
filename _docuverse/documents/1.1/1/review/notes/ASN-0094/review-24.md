# Review of ASN-0094

## REVISE

### Issue 1: AllocatedAddressAntichain — no concrete example

**ASN-0094, "The Address-Set Projection" section**: The lemma proves `cov_allocated({(x, δ(1, #x))}, Σ) = {x}` via an intricate Case 1 (link-link), Case 2 (content-content), Case 3 (cross-domain, split into 3a/3b with shared Steps 3.1, 3.2 and divergent Step 3.3a/3.3b).

**Problem**: The lemma is foundational — invoked in Sh4's contract clause (i.a)'s per-element argument, and the entire shape framework relies on its "slot at `x` denotes exactly `{x}`" reading. Steps 3.1 (NAT-card zero-position enumeration) and 3.2 (T4b E-field first-position agreement) are dense multi-step derivations. No worked example demonstrates the lemma's claim on a specific `x ∈ A^Σ`.

**Required**: Walk through at least the cross-domain Case 3 explicitly. Pick a concrete tumbler (e.g., `x = [1.0.2.0.1.0.5] ∈ dom(Σ.C)` with components in subspace `s_C`, and a hypothetical `a = [1.0.2.0.1.0.5.7]` claimed to be in `dom(Σ.L)`) and trace the derivation of the contradiction at Step 3.3 — showing why componentwise agreement at position `n_3 + 1` forces `s_C = s_L`. This verifies the proof's claim that the per-element zero-position derivation closes.

### Issue 2: RetractionTargetNotOnChain — no concrete example

**ASN-0094, "Lemma — RetractionTargetNotOnChain" section**: The lemma proves `b ⋠ a_emit(Σ, d)` for every `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`. Case II contains a careful zero-count additivity argument (NAT-card enumeration of `Z_a`, `Z_b`, `Z_w^shift`; bijection `Z_w^shift ↔ Z_w`; concatenation `f_a'` preserving strict monotonicity at the seam).

**Problem**: The Case II argument is one of the densest passages in the ASN — multiple cited NAT-* primitives, multiple substitution steps to derive `zeros(w) = 0`, then a downstream `home(a) = home(b)` derivation against the case hypothesis. No worked example verifies the lemma's claim on a chosen `(b, d)` pair.

**Required**: Provide a concrete example. Pick a `d ∈ dom(Σ.M)` with `zeros(d) = 2`, an existing `b ∈ dom(Σ.L)` with `home(b) ≠ d`, and verify `b ⋠ a_emit(Σ, d)` by exhibiting the candidate `a = b · w` and computing `home(a) = home(b) ≠ d`. A second example for Case I (same-home, distinct chain indices) would cover both branches.

### Issue 3: EffectiveWpSimplification — no concrete walkthrough

**ASN-0094, "Corollary — EffectiveWpSimplification" section**: The corollary discharges `NoCraftedSpanReachesD(Σ, d)` and the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` disjunct via the RetractionTargetNotOnChain lemma. Step 1 quantifies over `L_R^Σ` to discharge the first conjunct; Step 2 case-splits on `K ≁ R` vs `K ~ R`.

**Problem**: The corollary's discharge depends on Sh1 and Sh3 applied at `K := R` to pin down prior R-tuple G-endset structure. No concrete example traces this through a state Σ containing prior R-tuples (e.g., from the Attributed Retraction walkthrough at Σ_2) followed by a fresh `Emit_R` call, showing exactly how `wp_086`'s two non-trivial conjuncts are discharged step-by-step.

**Required**: Extend the Attributed Retraction walkthrough or add a standalone example. From a state with at least one prior `L_R^Σ` tuple, walk through both Step 1 (apply RetractionTargetNotOnChain at each prior R-tuple's G-slot address `b'`) and Step 2 (case-split on the new emission's K).

### Issue 4: `latest_K_for_addr` empty-`S_d` path not exercised concretely

**ASN-0094, "Coverage instantiation" section**: The template specifies:

> `latest_K_for_addr(d) ≡ ⊥` if `S_d = ∅`

And the *Partiality propagation rule* requires consumers to dispatch on `⊥` before composing further accessors.

**Problem**: The Coverage walkthrough exercises only the non-empty `S_d` case (Emissions C1, C2, C3 → `latest_K_for_addr(d_subject) = τ_3`). The empty-`S_d` path is mentioned in prose ("exercised explicitly at any state Σ with `dom(Σ.L) = ∅`") but never walked through, so the `⊥`-handling discipline is asserted rather than demonstrated.

**Required**: Add a brief subcase — at the initial state `Σ_0` prior to C1, verify `S_{d_subject} = ∅`, so `latest_K_for_addr(d_subject) = ⊥`, and note that any consumer attempting `from₁(latest_K_for_addr(d_subject))` without the `⊥`-check would read `from₁(⊥)`, undefined.

### Issue 5: Catalog-wide citation audit table omits the layer composite

**ASN-0094, Sh5 section, "Catalog-wide citation audit" table**: The table lists 10 rows enumerating catalog rows' template citations against the four discipline categories.

**Problem**: The table's bottom row addresses `K_is_fresh` ("Layer composite") and explicitly marks `mtime` as outside the four categories — but the row's narration says this is "the documented reason `K_is_fresh` is *not* part of the catalog's template families". The placement is consistent (showing the discipline rejects `K_is_fresh`), but the row labels itself as "not a base template", creating mild confusion about whether the table is auditing the catalog's *inclusions* or its *exclusions*. A reader scanning the table for "which symbols clear the discipline" sees one row that doesn't.

**Required**: Either (a) move the `K_is_fresh` row out of the audit table into a separate "exclusion examples" callout below it, or (b) add an explicit header on the table making clear that the `K_is_fresh` row is shown to illustrate a *failed* check, while all other rows show *passing* checks. The current placement reads as if it were a passing row at first glance.

### Issue 6: Sh-conf's interaction with K.σ/K.α not explicitly scoped

**ASN-0094, "The Conformance Axiom" section, "Scope" sub-paragraph**: The framework states "Sh-conf binds `Emit_K`, not the substrate primitive K.λ."

**Problem**: The wording focuses on K.λ-vs-Emit_K, but doesn't explicitly state that Sh-conf has no effect on K.σ (document registration) and K.α (content allocation). The Sh0–Sh3 inductive proofs implicitly cover this in Case A by noting that K.σ and K.α preserve `Σ.L`, but a reader checking "does the framework gate document registration?" or "does the framework gate content allocation?" has to infer the answer from the Sh-conf preconditions (only the framework's additions are `K ∈ T_cat` and `conf_K^Σ`, both of which presuppose an Emit-class invocation).

**Required**: Add one sentence to Sh-conf's *Scope* paragraph: "Sh-conf gates only Emit_K (class iii). The framework imposes no precondition on K.σ (document registration) or K.α (content allocation); these continue to operate per ASN-0086's contract."

## OUT_OF_SCOPE

### Topic 1: Multi-process Sh4 atomicity protocol
**Why out of scope**: The ASN explicitly scopes itself to single-process substrates, with multi-process coordination flagged as an Open Question. No revision needed; the framework's preservation theorems hold under their stated scope.

### Topic 2: Closure theorem for the composition language
**Why out of scope**: Consequence (b) explicitly disclaims a closure theorem, framing composition as a property of the layer's adopted composition language. The framework's structural guarantee is bounded at the atomic-template level.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: The current framework rejects ghost addresses in slot positions via Sh-conf clause (d). Whether a future shape family should admit ghost-targeting slots is acknowledged in Open Questions; it requires a new conformance discipline, not a revision to the current one.

### Topic 4: A sixth shape-tuple component for opt-in disciplines
**Why out of scope**: Open Questions notes the tradeoff (exhaustiveness vs catalog inflation). This is a future design decision, not an error in the current framework.

VERDICT: REVISE
