# Review of ASN-0094

## REVISE

### Issue 1: FDD contract's ordering with Sh-conf gates is implicit

**ASN-0094, *FDD functional-dependency contract* (Definition under FunctionalDependencyDiscipline)**: Clauses (i)–(iii) presuppose `slot_addrs(F)` is well-defined, which requires canonical-form `F`. But unlike the *Sh4 idempotency contract*, which has an explicit "Ordering with Sh-conf" paragraph stating "canonical-form gate first, Sh4 contract second, cardinality/target-domain gates third," the FDD contract makes no such statement.

**Problem**: Sister contracts (Sh4 and FDD) treat the gate-ordering question asymmetrically. A reader cannot determine from the FDD contract alone whether canonical-form failure rejects before or after the FDD candidate-set computation runs. If after, `slot_addrs(F)` would be invoked on non-canonical `F`, where it is undefined.

**Required**: Add an "Ordering with Sh-conf" paragraph to the FDD contract specifying: Sh-conf clauses (a)/(b) execute *before* FDD clauses (i)–(iii); Sh-conf clauses (c)/(d) execute *after*. Match the structure of Sh4's paragraph verbatim.

### Issue 2: AllocatedAddressAntichain Step 3.1 contradiction is elliptical

**ASN-0094, AllocatedAddressAntichain proof, Step 3.1**: "If a has a zero at any m ∉ {n_1, n_2, n_3}: at m ≤ #x, componentwise agreement forces x_m = 0, contradicting zeros(x) = 3"

**Problem**: The contradiction is correct but implicit. The reader must reconstruct: `x_m = 0` adds position `m` to `Z_x`; combined with `{n_1, n_2, n_3} ⊆ Z_x` and pairwise distinctness `m ∉ {n_1, n_2, n_3}`, we get `|Z_x| ≥ 4`, contradicting `zeros(x) = |Z_x| = 3`. This reconstruction is non-trivial because the four-element bound is not stated.

**Required**: Spell out the contradiction explicitly: "Adding `m` to the zero-index set `Z_x` gives `{n_1, n_2, n_3, m} ⊆ Z_x` (pairwise distinct by hypothesis `m ∉ {n_1, n_2, n_3}` plus `n_1 < n_2 < n_3`), so `|Z_x| ≥ 4`, contradicting `zeros(x) = 3`."

### Issue 3: Audit table mixes acceptance and rejection awkwardly

**ASN-0094, Sh5 audit table**: The framework demonstrates Sh5(b) falsifiability by including a rejected `K_is_fresh` row alongside ten accepted rows, then relocating it to a separate Layer Composites section with an additional callout.

**Problem**: The same artifact appears in three places (audit table row, expository callout, Layer Composites section). The relocation is documented but circuitous: an item labeled "Rejected" in the catalog audit re-enters scope under a different registration, with the registration discipline left to the reader to construct from the prose. The reader is asked to track which `mtime`-citation is admissible (Layer Composites' explicit declaration) versus inadmissible (the rejected row).

**Required**: Choose one presentation. Either keep the rejected row in the audit table and remove the callout (which duplicates the row's content); or remove the rejected row from the table and present the rejection only in a single labeled "Rejected candidate" callout that links to Layer Composites. The current three-place presentation hides where the actual catalog admission boundary is drawn.

### Issue 4: Notational inconsistency across worked examples

**ASN-0094, Worked Examples**: The Comment walkthrough uses `Σ_4'` (Tuple-Classifier), `Σ_3'` (in Coverage rejection), and unnumbered transitions in other places. The Attributed Retraction walkthrough uses `Σ_3'` for the EffectiveWpSimplification example.

**Problem**: Different example contexts re-use the same primed-state names with no shared meaning, and several states are introduced without explicit `→`-step numbering. A reader cross-referencing examples cannot determine which `Σ_n'` matches which.

**Required**: Adopt a uniform per-walkthrough state-naming scheme. Either use consecutive integer subscripts unique within each walkthrough (`Σ_0, Σ_1, Σ_2, ...`) with no primed notation, or use a per-walkthrough prefix (`Σ^cmt_n`, `Σ^cov_n`, `Σ^fdd_n`) to scope state names.

### Issue 5: Open Questions conflates fundamental limitations with refinement questions

**ASN-0094, Open Questions section**: The seven items range from refinement design choices (admit `(0, 0)` shapes, split Provenance) to fundamental scope limitations (cross-process atomicity, ghost-targeting slot semantics).

**Problem**: Cross-process atomicity is not just an open question — the framework's *Sh4 idempotency contract* and *FDD functional-dependency contract* are scoped to single-process substrates by design ("the framework's scope is restricted to single-process substrates"). This is a scope decision the framework commits to, not a topic awaiting future investigation. A reader scanning Open Questions cannot distinguish "design choice we haven't made" from "this is the framework's structural boundary."

**Required**: Either move cross-process consistency from Open Questions to a "Scope Limitations" section, or annotate each Open Questions item with whether it represents an unresolved design choice, a scope boundary, or a refinement candidate.

### Issue 6: Length and density obscure the substantive content

**ASN-0094, document as a whole**: The ASN runs to roughly 700+ lines of prose, with many definitions, contracts, lemmas, and worked examples interleaved.

**Problem**: Material that supports the framework (worked checks, scaffolding clause justifications, audit tables) is interleaved with the framework's substantive content (Sh-conf, Sh0–Sh4, the lemmas). Multiple worked examples for the same case (e.g., RetractionTargetNotOnChain Case II has three sub-examples) add bulk without sharpening the proof. The "Notational distinction between Σ_init and Σ_0 in this walkthrough" paragraph alone runs ~150 words to explain that the walkthrough's `Σ_0` is reachable from `Σ_init` by content-only steps.

**Required**: Move repeated worked examples (e.g., RetractionTargetNotOnChain's three Case II walkthroughs collapse to one with a note that the other two follow by analogous argument), the Sh5 audit table's full classification (could be in an appendix), and the catalog-wide citation audit to supporting material. Keep the core ASN body focused on the axiom, lemmas, and shape catalog.

### Issue 7: "Framework" used throughout without definition

**ASN-0094, throughout**: The term "the framework" appears 80+ times. It refers to the shape discipline atop ASN-0086, but is never explicitly defined.

**Problem**: A reader encountering "the framework" early in the document (e.g., "the framework rejects non-conformant emissions") has no anchor for what comprises the framework. Is it Sh-conf? Sh-conf + Sh0–Sh4? Sh-conf + Sh0–Sh5 + the contracts? The implicit scope shifts as the document develops.

**Required**: Add a one-paragraph definition near the start (perhaps after "Scope and Substrate Scaffolding") naming the framework's components: the axiom Sh-conf, the preservation lemmas Sh0–Sh4, the META catalog Sh5, the four layer-discipline contracts, and the scaffolding interface.

### Issue 8: Resolution row's mechanical-generation claim needs verification at a non-Comment consumer

**ASN-0094, Canonical Shape Catalog, Resolution row** and **Resolution worked example**: The catalog row claims Resolution generates the same five-template base family as DirectedPair mechanically per Sh5(b), and the worked example exercises `pair_{K_res}` and `to_addrs_{K_res}` directly. But Resolution differs from DirectedPair on the `t_G` axis (`A_rel` vs `A_doc`), and the worked example reuses `ρ_1, ρ_2` from the Comment walkthrough — where Resolution is already in use as `K_res`.

**Problem**: The worked example does not exercise Resolution at a use site independent of Comment's parametric consumption. The catalog row asserts Resolution's base templates are usable standalone, but every walkthrough threads them through NonIdempotentDirectedPair's `_via` templates. A reader cannot verify the standalone-usability claim from the examples provided.

**Required**: Either add a worked example registering a Resolution-shape K with no NonIdempotentDirectedPair consumer in scope (e.g., a layer-defined "ApprovedBy" relation where reviewers approve standalone documents), or weaken the row's framing to acknowledge that all examples thread Resolution through a parametric consumer.

## OUT_OF_SCOPE

### Topic 1: Multi-process / distributed substrate consistency

**Why out of scope**: The framework explicitly restricts itself to single-process substrates ("Scope: single-process substrate" paragraph). Cross-process coordination protocols (distributed locking at the `~`-equivalence class scope, causal consistency of `T_cat` registration, etc.) are genuinely new territory requiring a distinct coordination model. Belongs in a future ASN on distributed relational-layer execution.

### Topic 2: Higher-arity link shapes

**Why out of scope**: The framework's *Arity scope* paragraph explicitly limits to arity-3 (standard-triple) links. Extending shape constraints to general N-ary links would require additional shape components per extra slot plus an extended template machinery. Belongs in a separate ASN extending the catalog to higher arities.

### Topic 3: Ghost-targeting slot semantics

**Why out of scope**: The framework forbids ghost addresses in slot positions (Sh-conf clause (d) requires `slot_addrs(F) ⊆ t_F^Σ` against the *allocated* set). Whether shape-conformant emissions targeting future-to-be-allocated addresses should be admitted under a state-dependent conformance rule is a design question for a future shape-extension ASN.

### Topic 4: Procedural derivation of templates from shapes

**Why out of scope**: Sh5(a) acknowledges templates are hand-curated, not mechanically derived. A procedural recipe that would generate template families from arbitrary shapes (sharpening Sh5's META status into a derivation theorem) is future work, not a defect in the present catalog construction.

### Topic 5: Lifetime extension of `T_cat`

**Why out of scope**: The framework forbids runtime extension of `T_cat`. Mechanisms for safely admitting new types mid-execution (verifying `L_K^{Σ_registered} = ∅` at the registration point, or alternative empty-baseline discharge strategies) are a separate concern, addressed only by the framework's prohibition.

VERDICT: REVISE
