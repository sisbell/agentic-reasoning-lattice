# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN references to ASN-0093 and ASN-0036 without foundation inclusion
**ASN-0094, Definition — SubstrateConformingLayer**: "*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093"; "ASN-0093 substrate invariants: M0, M1, C0, C1, C1b, C1c, C-fin."
**Problem**: ASN-0094 directly references ASN-0093 and ASN-0036 by number, but neither appears in the foundation block (which contains only ASN-0034, ASN-0043, and ASN-0086). Per the self-containment standard, non-foundation ASN references must be flagged.
**Required**: Either include ASN-0093/ASN-0036 in the foundation set (if they are verified), or abstract the catalog reference through ASN-0086's existing SubstrateConformingLayer Definition (which already enumerates these invariants), rather than restating the enumeration here.

### Issue 2: Worked examples implicitly assume `dom(Σ₀.L) = ∅` without stating it
**ASN-0094, Worked Example: K = comment, Emission 1**: "K.λ's first-emission branch fires at home_K: `{ℓ' ∈ dom(Σ₀.L) : origin(ℓ') = home_K} = ∅` (no comment-tuples homed at home_K have been emitted yet, since we start from Σ₀ with empty L_K)."
**Problem**: The K.λ first-emission predicate quantifies over *all* of `dom(Σ.L)`, not just `L_K`. The justification "since we start from Σ₀ with empty L_K" establishes only that no K-typed links are homed at home_K, but does not preclude non-K links from being homed there. If `dom(Σ₀.L)` contains *any* link homed at home_K (of any type, including types outside `T_cat`), the first-emission branch does not fire and the address `[home_K.0.s_L.1]` would not be produced.
**Required**: State explicitly that `dom(Σ₀.L) = ∅` (or, more weakly, that no link is homed at home_K or home_R at Σ₀). The same fix is needed for the Coverage walkthrough (Emission C1) and the Tuple-Classifier/Provenance walkthroughs.

### Issue 3: R registration in T_cat assumed but not stated as a baseline requirement
**ASN-0094, Sh-conf interaction with Nullify**: "Sh-conf admits every well-formed Nullify call; the substrate's retraction primitive is shape-conformant by construction, with no special-case exemption needed."
**Problem**: `Nullify` reduces to `Emit_R`, which Sh-conf admits only if `R ∈ T_cat`. If a layer instantiates the framework without registering R, every Nullify call fails Sh-conf's first conjunct (`K ∈ T_cat`) and is rejected, even though Nullify is a substrate primitive (per ASN-0086). The framework's preservation theorems (Sh0–Sh4) implicitly assume the substrate's retraction primitive remains callable — which requires R registration.
**Required**: State explicitly that R ∈ T_cat (with shape `(*, 1, A, A_rel, ⊤)`) is a baseline registration required by the framework. Add this to the catalog row for Retraction or to the framework's preconditions.

### Issue 4: Sh4 Case D textual error — "below" should be "above"
**ASN-0094, Sh4 proof, Case D**: "...τ_new's slot-pair distinctness from every member of A_R^Σ (the IH is the *off-diagonal* content of Sh4's universal — see scope clarification below — and τ_new's diagonal `(τ_new, τ_new)` case is trivially satisfied by reflexivity..."
**Problem**: The "scope clarification" referenced is the "Universal scope" subsection at the start of the Sh4 statement, which appears *above* the proof. "Below" is incorrect.
**Required**: Change "see scope clarification below" to "see scope clarification above".

### Issue 5: Catalog rows for Resolution and Retraction omit base templates, tension with Sh5 META discipline (b)
**ASN-0094, Canonical Shape Catalog table, Resolution and Retraction rows**: "Resolution | (1, 1) | A_doc | A_rel | ⊤ | (consumed parametrically by NonIdempotentDirectedPair's `_via` templates)"; "Retraction | (\*, 1) | A | A_rel | ⊤ | (consumed by R6's active-subset definition)".
**Problem**: Sh5's META discipline (b) states that templates depend only on shape components + K's name + named accessors, and Sh5 explicitly says "structurally identical shapes necessarily share the same canonical *base* template family by Sh5: there is no design freedom in base template selection once the shape is fixed." But Resolution's shape `(1, 1, A_doc, A_rel, ⊤)` should mechanically generate base templates analogous to DirectedPair's `pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` (with the t_G domain changed); similarly Retraction's shape `(*, 1, A, A_rel, ⊤)` should mechanically generate base templates. Listing only "consumed parametrically by..." or "consumed by R6..." mixes role-specific use cases with the shape-determined template family, creating apparent inconsistency between the catalog presentation and the META discipline.
**Required**: Either (a) list the shape-determined base templates explicitly for Resolution and Retraction (matching what their shape mechanically generates per Sh5(b)), or (b) qualify the catalog presentation by noting these rows display only the *commonly-used* templates and the base templates are inherited from the shape components per Sh5(b).

### Issue 6: Variable name "home_K" reused across walkthroughs without disambiguation
**ASN-0094, Tuple-Classifier walkthrough**: "Register `K = endorsed` with shape `(0, 1, -, A_rel, ⊤)`... Working from Σ_4 of the Comment example, with τ_2 ∈ A_rel^{Σ_4}: `Emit_K(Σ_4, home_K, ∅, {(a_2, δ(1, #a_2))})`."
**Problem**: `home_K` was bound in the K = comment walkthrough as the home document for comment-tuples. The Tuple-Classifier walkthrough switches K to `endorsed` but reuses the symbol `home_K` without clarification — is this the *same* home document (now hosting both comment and endorsed emissions), or a new home for endorsed? Similar reuse appears in the Provenance Form 2 walkthrough and the Attributed Retraction example.
**Required**: Either rename home symbols per-walkthrough (e.g., `home_endorsed`, `home_provenance`) or state explicitly when a home is shared across types (e.g., "we reuse home_K from the Comment example as the home for endorsed emissions, exercising the framework's permission for multiple relations to share a home document").

### Issue 7: Definition — RetractionType is restated but not used; relationship to ASN-0086's machinery is unclear
**ASN-0094, Definition — RetractionType and Definition — RetractionDirectionality**: Both definitions appear at the start of the Scope/Substrate Scaffolding section but are never explicitly cited later in the document.
**Problem**: These two definitions establish naming conventions (the retraction coverage class `[R]`, the retraction's directional convention for to-set) that are presupposed by the Retraction shape `(*, 1, A, A_rel, ⊤)` later in the catalog. But they are stated upfront without being woven into the proofs or worked examples, and they appear redundant with ASN-0086's existing Definition — RetractionType. The reader cannot tell whether ASN-0094 is restating ASN-0086's definitions for convenience, or introducing additional commitments.
**Required**: Either remove these definitions (referring to ASN-0086 instead) or explicitly state how they extend/specialize ASN-0086's definitions and cite them at the use sites (in the Retraction catalog row, in the Attributed Retraction example).

### Issue 8: AllocatedAddressAntichain Case 3 Step 3.2 — implicit dependence on `#E(·) ≥ 1`
**ASN-0094, AllocatedAddressAntichain proof, Step 3.2**: "T4b's E-field index range is `n_3 + 1 .. #x` with length `#E(x) = #x − n_3`, so non-emptiness gives `n_3 + 1 ≤ #x`, i.e., `n_3 < #x` (T4(iv) excludes `n_3 = #x` independently, since `x_{#x} ≠ 0` while `x_{n_3} = 0`)."
**Problem**: The argument that `#E(x) ≥ 1` (and hence j = 1 is a valid index) is woven through L1b and the content-side scaffolding's `#E(·) ≥ 2` clause earlier in the same step. But the actual conclusion `E(x).1 = E(a).1` only needs `#E(x) ≥ 1`, not `≥ 2`. Why is `#E(·) ≥ 2` cited rather than `≥ 1`? If only `≥ 1` is needed, the proof should cite the weaker form (which follows from T4(iv) alone). If `≥ 2` is needed elsewhere (e.g., for some structural property of E-field comparison not yet explicit), make that explicit.
**Required**: Either (a) revise to cite only `#E(·) ≥ 1` (derivable from T4(iv)) if that is sufficient, or (b) explicitly identify where the second component of E is consumed and explain why `#E(·) ≥ 2` is needed.

### Issue 9: Sh-conf's "effective wp" under non-relational-layer regimes is under-specified
**ASN-0094, Sh-conf, Effective wp section**: "Since `T_cat ⊆ T_admissible` (T_cat definition), `K ∈ T_cat` absorbs `K ∈ T_admissible`, and the effective wp simplifies under the relational layer's committed operations to: `wp_eff = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`"
**Problem**: The simplification depends on the unit-depth retraction discipline collapsing `NoCraftedSpanReachesD(Σ, d)` to ⊤ and the `(K ≁ R ∨ a_emit ∉ coverage(G))` clause to ⊤. Under shape-conformant Retraction emissions, G must be `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ` (Sh-conf + Retraction shape) — which secures the discipline. But the ASN does not derive this explicitly; the reader must infer it. The simplified form depends on a step (Retraction's shape securing the unit-depth discipline) that is mentioned in the Retraction walkthrough but not cited at the wp_eff derivation site.
**Required**: At the effective-wp simplification, cite that Retraction's shape `(*, 1, A, A_rel, ⊤)` (combined with Sh-conf clauses (a)/(b) forcing canonical-slot form and clause (c) forcing `|slot_addrs(G)| = 1`) is what secures the unit-depth discipline, hence makes the wp_086 simplification applicable to every shape-conformant emission.

## OUT_OF_SCOPE

### Topic 1: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Explicitly listed as an open question. Would require a new restriction axis beyond cardinality/target-domain/idempotency.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: Explicitly listed as an open question. L9 permits ghost spans in endsets but the framework forbids ghost addresses in slot positions of registered relations; admitting them would require a state-dependent conformance rule.

### Topic 3: Higher-arity links (N ≥ 4)
**Why out of scope**: The framework explicitly restricts itself to the standard-triple slice `L^Σ` (arity-3 links). Extending to higher arities requires per-extra-slot shape components and is acknowledged as future work.

### Topic 4: Cross-process consistency of the shape registry
**Why out of scope**: Explicitly listed as an open question. The lifetime-constancy commitment is intra-process; distributed substrate consistency is future work.

### Topic 5: `(0, 0)` shapes (single-tuple existence flags with no attribution)
**Why out of scope**: Explicitly listed as an open question. Whether such relations are needed by the substrate is open.

VERDICT: REVISE
