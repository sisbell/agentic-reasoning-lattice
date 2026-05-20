# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN references to ASN-0093 by number

**ASN-0094, multiple sites**: In Lemma — RetractionTargetNotOnChain Case II: "By L1a (LinkScopedAllocation, ASN-0043), home(b) is determined…" (fine, ASN-0043 is foundation). But also throughout: e.g., the SubstrateConformingLayer definition cites "ASN-0093's substrate invariants: M0, M1, C0, C1, C1b, C1c, C-fin" and "ASN-0093 L0 (SubspacePartition)" appears in the *Link subspace partition* scaffolding clause and the property table refers to a "concrete realization of L0's abstract `subspace_I(·)` as `E(·).1`."

**Problem**: ASN-0093 and ASN-0036 are not in this review's foundation list (only ASN-0034, ASN-0043, ASN-0086 are). Per the review rules, "If the ASN references another ASN by number, flag it as a REVISE item. The exception is foundation ASNs."

**Required**: Either redirect every "ASN-0093 …" / "ASN-0036 …" citation through a locally-named scaffolding clause without by-number attribution (the scaffolding section already establishes named entry points: *Link subspace partition*, *Document address structure*, etc.), or formally adopt ASN-0093/ASN-0036 as foundation prerequisites at the top of this ASN. The current mixed practice — scaffolding clauses named locally but proofs still citing the upstream ASN — is what the rule rejects.

### Issue 2: EffectiveWpSimplification's Step 1 underjustifies the past-to-present bridge

**ASN-0094, EffectiveWpSimplification proof, Step 1**: "For every prior R-tuple `(b̂, F', G') ∈ L_R^Σ`, Sh-conf admission at past emission forces (clauses (a)/(b)) `G'` canonical-slot, (clause (c) at `c_G = 1` of Retraction's catalog row) `|slot_addrs(G')| = 1`, and (clause (d) at `t_G = A_rel`) `slot_addrs(G') ⊆ A_rel^Σ = dom(Σ.L)`."

**Problem**: The Sh-conf check at past emission only guarantees conformance at the past state. The argument silently relies on R2 (TupleAddressPermanence, ASN-0086) plus allocated-set monotonicity to carry that conformance to the current state Σ. But there is a cleaner path available: Sh0, Sh1, and Sh3 are the named preservation theorems that establish current-state conformance for every τ ∈ L_K^Σ at every K ∈ T_cat. With R registered (baseline requirement), Sh1 and Sh3 apply directly to L_R^Σ.

**Required**: Replace "Sh-conf admission at past emission forces (clauses (a)/(b)) G' canonical-slot…" with "By Sh1 at K := R, G' is canonical-slot with `match(|slot_addrs(G')|, 1)`. By Sh3 at K := R, `slot_addrs(G') ⊆ A_rel^Σ`." This makes the proof's dependence on the preservation theorems explicit and avoids the implicit R2-plus-monotonicity step.

### Issue 3: Implicit Resolution-shape constraint on K_res is undocumented in the template signature

**ASN-0094, Comment instantiation walkthrough**: `unresolved_K_comments_via(K_res, d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}` where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

**Problem**: The body invokes `to₁(ρ)` and compares against `addr(τ) ∈ A_rel`. For this to type-check, K_res must have `c_G = 1` (so `to₁` is total) and `t_G = A_rel` (so the codomain matches addr(τ)). That is exactly the Resolution shape `(1, 1, A_doc, A_rel, ⊤)`. The catalog row's text mentions this in passing ("in any Resolution-shaped K_res"), but the template's formal signature does not. Sh5(b)'s discipline classifies this as a parametric template, but a parametric template whose well-formedness silently depends on the argument's shape is hard to falsify against the discipline.

**Required**: State the precondition in the template signature: `unresolved_K_comments_via : (K_res with shape(K_res) = (1, 1, A_doc, A_rel, ⊤)) × A_doc → ℘_fin(A_K^Σ)`, and explicitly call out that the parametric column entries are typed by their permitted shape, not just by name.

### Issue 4: Sh-conf "Effective wp" preview duplicates the Corollary and creates forward-reference fog

**ASN-0094, Sh-conf section, "Effective weakest-precondition under Sh-conf (preview)"**: The paragraph states the simplification result, qualifies it with "Within the shape framework, this regime (i) collapse is secured by Retraction's shape itself," then concludes "this paragraph is a *preview*; the formal collapse is established by Lemma — RetractionTargetNotOnChain (next subsection)…"

**Problem**: The preview repeats the simplification's content before any of its premises (the Lemma, Sh0–Sh3) are introduced, which works against the reader's ability to verify the chain of dependence on a first pass. The reader cannot tell, while reading Sh-conf, whether the simplification is asserted as an axiom-side claim or as a derived theorem.

**Required**: Either delete the preview entirely and let the Corollary speak for itself, or condense the preview to one sentence: "Under the framework's *Emit_K routing commitment*, ASN-0086's `wp_086` collapses; see Corollary — EffectiveWpSimplification below for the named result." The current 200-word preview restates content that is then proved in the next subsection.

### Issue 5: AllocatedAddressAntichain Step 3.1's fourth-zero argument has a hidden case

**ASN-0094, AllocatedAddressAntichain proof, Step 3.1**: "Suppose, toward contradiction, that `a` has a fourth zero at some position `m ∈ {1, ..., #a} ∖ {n_1, n_2, n_3}`: if `m ≤ #x`, then `aₘ = 0` together with componentwise agreement forces `xₘ = 0`, adding a fourth zero to `x` and contradicting `zeros(x) = 3`; if `m > #x`, then `m` is a zero position in `a` outside `{n_1, n_2, n_3}` (which all lie at positions `≤ #x`), so `zeros(a) ≥ 4`, contradicting `zeros(a) = 3`."

**Problem**: The argument concludes "`a`'s three zero positions are exactly `n_1 < n_2 < n_3`" but it has only ruled out *additional* fourth zeros, not the case where one of `n_1, n_2, n_3` is *not* a zero of `a`. The componentwise agreement `aᵢ = xᵢ` for `1 ≤ i ≤ #x` does force `a` to have zeros at `n_1, n_2, n_3` (this is established earlier in the step), so the missing case is in fact already excluded. But the step would read more cleanly if it stated explicitly that `a` has zeros at exactly the three positions `n_1, n_2, n_3` because (a) componentwise agreement forces zeros there, and (b) the fourth-zero argument forbids any additional position.

**Required**: Add a one-clause statement that `a` has zeros at `n_1, n_2, n_3` (from componentwise agreement applied at those positions) before launching the contradiction argument for additional zeros. The current prose makes both halves rest on the same "fourth zero" framing, which obscures the structure.

### Issue 6: Sh4 Case D's "leaving" set lacks an explicit cardinality / antichain bound

**ASN-0094, Sh4 Case D**: "let `leaving := {τ ∈ A_R^Σ : addr(τ) ∈ coverage(G_{τ_new})}` exits."

**Problem**: Under Sh-conf at Retraction (`c_G = 1` plus canonical form), `G_{τ_new}` is a single unit-depth span `{(b, δ(1, #b))}` for `b ∈ A_rel^Σ`, so `coverage(G_{τ_new}) = {t : b ≼ t}`. By R0a (FlatLinkDomain), `{τ ∈ A_R^Σ : addr(τ) ∈ {t : b ≼ t}} ⊆ {τ ∈ A_R^Σ : addr(τ) = b}` — at most one element. So `|leaving| ≤ 1`. The proof never observes this and proceeds with `leaving` as "a non-empty subset", obscuring the structural simplicity.

**Required**: Add a sentence: "By R0a and Sh-conf at Retraction, `coverage(G_{τ_new})` intersects `{addr(τ) : τ ∈ A_R^Σ}` in at most one address, so `|leaving| ≤ 1`." This both tightens the argument and makes the substantive content (that the simultaneous step is `+1, −≤1`, not an arbitrary swap) visible to the reader.

## OUT_OF_SCOPE

### Topic 1: (0, 0) shape admissibility

**Why out of scope**: The Open Questions section explicitly raises this — would a `(0, 0, -, -, _)` shape be useful, and what would its template family look like? This is new shape territory, not a defect in the current catalog.

### Topic 2: Splitting Provenance into Provenance-with-target and Provenance-attribution-only

**Why out of scope**: The Open Questions section asks whether `(1, 0|1, A, A, ⊤)` should be split. The current Provenance row's `c_G = 0|1` with partial templates works; whether the canonical catalog should normalize partiality away is a future design question.

### Topic 3: Cross-process consistency for Sh4 and FDD contracts

**Why out of scope**: The framework's single-process scope is explicitly registered. Multi-process coordination protocols for layer-discipline contracts are a future extension, not a gap in the present specification.

### Topic 4: Idempotency as a derivable axis vs an independent shape component

**Why out of scope**: Listed in Open Questions. The current catalog admits `idem ∈ {⊤, ⊥}` independently of other components; whether this is the minimal independent set is a meta-question about shape-space economy.

### Topic 5: Ghost-targeting slot semantics

**Why out of scope**: Listed in Open Questions. L9 (TypeGhostPermission) admits ghost spans in endsets at the substrate level, but the shape framework rejects ghosts in slot positions of registered relations. Whether to extend the framework to admit ghost slots is a future design question.

### Topic 6: Composite shapes (relations whose F or G is constrained by another relation's content)

**Why out of scope**: Listed in Open Questions. Higher-order relational composition is beyond the canonical-shape catalog and would require a new restriction axis.

### Topic 7: Bipartite-coverage gaps in the catalog ((1, 1, A_rel, A_doc, _), (1, 1, A_rel, A_rel, _))

**Why out of scope**: The catalog itself acknowledges these gaps and notes they can be added by extension. Filling them requires concrete use cases that demand the templates; the framework does not pretend to be exhaustive over `{0, 1, *, 0|1}² × {A_doc, A_rel, A, -}² × {⊤, ⊥}`.

VERDICT: REVISE
