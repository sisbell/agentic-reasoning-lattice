# Review of ASN-0094

## REVISE

### Issue 1: T4-validity dependency for content addresses is implicit
**ASN-0094, AllocatedAddressAntichain proof, Step 3.2**: "T4(iv) applied to x gives x_{#x} ≠ 0, while x_{n_3} = 0, so n_3 ≠ #x"
**Problem**: T4(iv) requires x to be T4-valid. For the link side (Case 3a), L1c (LinkAllocatorConformance) supplies T4-validity via T10a.4 — but the proof's "Element-level character" prelude cites only L1 and L1b, not L1c. For the content side (Case 3b), the scaffolding clause "Element-level content addresses" asserts only `zeros(a) = 3` and `#E(a) ≥ 2`, never asserting T4-validity. T4-validity is implicitly required (since `#E(a)` is well-defined only when `a ∈ dom(N)`, which is the T4-valid subset per T4b), but the dependency is invisible.
**Required**: Either (a) strengthen the scaffolding clause to "Every `a ∈ dom(Σ.C)` is T4-valid with `zeros(a) = 3` and `#E(a) ≥ 2`", or (b) explicitly derive T4-validity in the proof from the scaffolding's two clauses (zeros = 3 + #E ≥ 2 combined with the implicit prerequisite that `#E` be defined). Symmetrically, the link-side prelude should cite L1c for T4-validity, not just L1/L1b for element-level character. The lemma is load-bearing for the Sh4 contract's clause (i.a) over-approximation argument, so closing this gap matters.

### Issue 2: R3 overgeneralization in Sh0–Sh3 proofs
**ASN-0094, Sh0 inductive step**: "By R3 (TypedSliceMonotonicity, ASN-0086), `L_K^Σ ⊆ L_K^{Σ'}` for every transition; `L_K` never contracts."
**Problem**: R3 in ASN-0086 is stated only for `→`-transitions: `(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`. For `↦ \ →` (arrangement-modifying) transitions, monotonicity comes from LinkStoreInvarianceUnderArrangement (which gives equality, not just inclusion), not R3. The proof's Case A correctly cites LinkStoreInvarianceUnderArrangement for arrangement steps, but the opening claim attributes the monotonicity to R3 alone "for every transition", which conflates the two sources. The same imprecision appears in Sh1, Sh2, and Sh3 proofs.
**Required**: Replace the opening claim with the correct disjunction: "`L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3, equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement." Then the case split into A and B is justified.

### Issue 3: Imprecise R-numbering reference in introduction
**ASN-0094, opening paragraph**: "ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by R0–R7."
**Problem**: ASN-0086 has lemmas through R7a (with intermediate corollaries R0a, R0a-Cor1, R0a-Cor2, R5-Cor, R6c-Corollary). "R0–R7" undercounts. The framework actually consumes R0, R0a, R0a-Cor1, R1, R2, R3, R4, R5, R6a, R6b, R6c, R7a — essentially all of ASN-0086's lemma roster.
**Required**: Change to "governed by R0–R7a" or "governed by the lemma family R0…R7a of ASN-0086". Minor but worth tightening.

### Issue 4: Sh4 base case relies on initial-state baseline that appears later in the text
**ASN-0094, Sh4 proof, base case**: "At `Σ_0`, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous."
**Problem**: The identification `Σ_0 = Σ_init` is established in the Sh-conf section's "Initial-state baseline for preservation proofs" paragraph, which says "References to `Σ_0` in the proofs below denote this `Σ_init`." However, the Sh0 proof appears immediately after Sh-conf, and the baseline paragraph's `L_K^{Σ_init} = ∅` claim is conditional on the layer commitment being honored from `Σ_init` onward. The proof doesn't restate the baseline at each induction's base case; readers must remember the conditional reach.
**Required**: At each of Sh0, Sh1, Sh2, Sh3, Sh4 base case, cite the initial-state baseline explicitly: "At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption), `L_K^{Σ_0} = ∅`; …". This makes the conditional reach of each preservation theorem explicit at the site of its use.

### Issue 5: Stratification of inductive proofs is implicit
**ASN-0094, Sh4 contract clause (i.a)**: "Under Sh0/Sh1, every τ ∈ A_K^Σ has canonical-form slot endsets… By Sh2 applied to τ, y ∈ t_F^Σ ⊆ A^Σ, so y is allocated."
**Problem**: The Sh4 contract specification (and hence Sh4's preservation proof) invokes Sh0, Sh1, Sh2 at the current state Σ. This is sound because Sh0–Sh3 are proved independently of Sh4. But the stratification (Sh0–Sh3 first, then Sh4 uses them; FDD uses Sh-conf preservation symmetrically) is implicit. A reader who doesn't notice the order could suspect circularity, especially since the contract specification's per-element argument uses Sh2 which itself is proved inductively.
**Required**: Add a brief note before Sh4 stating the stratification: "Sh4's preservation argument consumes Sh0–Sh3 as established lemmas at state Σ. These are proved independently by their own inductions over `↦*` and are not part of Sh4's inductive hypothesis." Same note before FunctionalDependencyDiscipline's preservation proof.

### Issue 6: Sh-conf's effective-wp derivation has forward dependency
**ASN-0094, Sh-conf section, effective-wp paragraph**: "Within the shape framework, this regime (i) collapse is secured by Retraction's shape itself: … Consequently `NoCraftedSpanReachesD(Σ, d)` holds automatically at every Sh-conf-admitted Retraction call site (by Lemma — RetractionTargetNotOnChain, stated and proved immediately below this derivation, which spells out the per-home and cross-home chain-element argument)…"
**Problem**: The effective-wp derivation cites RetractionTargetNotOnChain forward, with explicit acknowledgment that "The reader may take this derivation as preliminary on first pass". The forward reference is admitted to be reader burden. More substantively: the effective-wp's simplification to `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)` is a load-bearing claim used by every downstream rejection-mode analysis, but is presented as a preliminary derivation depending on a lemma proved afterward.
**Required**: Either (a) reorder so RetractionTargetNotOnChain is proved before the effective-wp derivation, or (b) explicitly hoist the effective-wp simplification into a labeled Consequence/Corollary after the lemma is established, so downstream proofs cite the Consequence rather than the preliminary derivation.

### Issue 7: Atomicity scope for Sh4 contract is described inconsistently
**ASN-0094, Sh4 contract**: "The layer commits to executing clauses (i)–(iii) atomically with respect to other Sh4-emitters at the same ~-equivalence class of K — emission and retraction events at any K' with K' ~ K that could split (i)'s observation from (iii)'s emission must be serialized by the layer."
**Problem**: The opening phrase says "Sh4-emitters at the same ~-class". The dash-clause then expands to "emission and retraction events". These are different scopes. The FDD contract uses the broader formulation directly ("other emitters and retractors at the same ~-equivalence class of K"). The inconsistency is unimportant in practice — the dash-clause's expansion is what governs — but a reader scanning for the atomicity scope sees two different statements.
**Required**: Use one phrasing consistently. The expanded form ("emission and retraction events at any K' with K' ~ K") is the operative one and matches FDD.

### Issue 8: The `slot_addrs(F)` as set-valued function should clarify well-definedness
**ASN-0094, CanonicalSlotForm definition**: "`X_F` is uniquely recoverable from any canonical-form `F` by reading the start address of each unit-depth span; equivalently, `X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}` is a well-defined set-valued function of `F`."
**Problem**: The equivalence "`X_F` recovered by reading start addresses" presumes that a canonical-form `F = {(x, δ(1, #x)) : x ∈ X_F}` has unique start addresses per span — which is true (each `x ∈ X_F` contributes one span), but the prose doesn't explicitly link the comprehension's witness `s` to the original `X_F`. A careful reader needs to verify that the recovered set matches the source set: for any `s ∈ T`, `(E (s, ℓ) ∈ F :: ℓ = δ(1, #s))` iff `s ∈ X_F`. This holds because `F`'s span set is exactly `{(x, δ(1, #x)) : x ∈ X_F}`, so a span has start `s` iff `s = x` for some `x ∈ X_F` iff `s ∈ X_F`.
**Required**: Add one sentence explicitly verifying the equivalence: "The comprehension `{s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}` recovers exactly `X_F` because `F`'s span set is `{(x, δ(1, #x)) : x ∈ X_F}`, so a span has start `s` iff `s ∈ X_F`."

## OUT_OF_SCOPE

### Topic 1: Multi-process atomicity protocol
**Why out of scope**: The Open Questions section explicitly notes that Sh4's contract is scoped to single-process substrates and that cross-process consistency requires a coordination protocol not specified by this framework. This is correctly deferred.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: The framework restricts `slot_addrs(F) ⊆ t_F^Σ` to allocated addresses, precluding ghost-targeting in slot positions. Whether a future shape family should admit ghost-targeting slots is correctly listed as open.

### Topic 3: Composite shape registry
**Why out of scope**: The framework's catalog is bipartite (A_doc vs A_rel on the to-side) for current needs; further bipartite entries can be added by extending the catalog. Open Questions notes whether composite shapes (relations whose F or G is constrained by another relation's content) need a new restriction axis.

### Topic 4: Promoting per-K disciplines to shape-tuple component
**Why out of scope**: Open Questions raises whether FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline should become a sixth shape-tuple component. The current encoding as opt-in registrations is sufficient for present needs; the trade-off (registry exhaustiveness vs. canonical-shape space size) is correctly deferred.

VERDICT: REVISE
