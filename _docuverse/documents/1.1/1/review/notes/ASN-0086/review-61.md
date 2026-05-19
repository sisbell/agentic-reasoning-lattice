# Review of ASN-0086

## REVISE

### Issue 1: ASN-0093 foundation not consulted; emission primitives reinvented

**ASN-0086, "Setup" and "SubstrateEmissionPrimitive (AXM)"**: "We work in systems satisfying ASN-0043 (and therefore ASN-0036 and ASN-0034)." ... "The substrate admits, as its primitive emission for the link store (the underlying form of class (iii)), *emit-at-any-L1c-conforming-fresh-address*."

**Problem**: ASN-0093 is a listed foundation that provides three operations — K.σ (DocumentRegistration), K.α (ContentAllocation), K.λ (LinkAllocation) — which correspond exactly to ASN-0086's classes (i), (ii), (iii). K.λ's preconditions already embed the sibling-frontier discipline (first emission `[d.0.s_L.1]`; subsequent emission `inc(ℓ_prev, 0)` from the max-homed link). ASN-0086 reinvents these as `SubstrateEmissionPrimitive` plus class-(i)/(ii)/(iii) frame conditions in broader form.

Per review standard 7: "If an ASN invents its own notation for something a foundation already defines, flag it as a REVISE item — the ASN should use the foundation, not reinvent it."

The downstream effect is significant: R0a (FlatLinkDomain), R0a-Cor1 (ContiguousPrefixUnderDiscipline), and R0a-Cor2 (DepthTwoLinkAddresses) become discipline-*conditional* in ASN-0086. Under ASN-0093's K.λ they are unconditional, since K.λ's preconditions exactly impose the sibling-frontier discipline. The entire Implementation Notes appendix and the discipline-conditionality discussion would vanish. The Open Question "Should the sibling-frontier discipline... be elevated to a substrate-level guarantee?" already has its answer in ASN-0093.

**Required**: Cite ASN-0093 as the substrate, replace SubstrateEmissionPrimitive with K.λ, replace class-(i)/(ii)/(iii) frames with K.σ/K.α/K.λ, and drop the conditional treatment of R0a/R0a-Cor1/R0a-Cor2. Alternatively, justify operating at the strictly more abstract ASN-0043 layer.

### Issue 2: Setup hypothesis duplicates ASN-0093 L0

**ASN-0086, "Setup hypothesis"**: "We additionally assume globally `s_C`-resident content: `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`."

**Problem**: ASN-0093's L0 (SubspacePartition) states `(A a ∈ dom(C) :: E(a)₁ = s_C)` directly, with `subspace_I(a) = E(a)₁` per ASN-0036. The "hypothesis" is just a foundation invariant.

**Required**: Replace the Setup hypothesis with a citation to ASN-0093 L0.

### Issue 3: Subspace-distinctness hypothesis duplicates SubspaceConventionAxiom

**ASN-0086, "Subspace-distinctness hypothesis"**: "We additionally assume that the content and link subspace identifiers are distinct first-element-field values: `s_C ≠ s_L`."

**Problem**: ASN-0093's SubspaceConventionAxiom posits `s_C = 1 ∧ s_L = 2`, immediately giving `s_C ≠ s_L`. The hypothesis is a consequence of an existing foundation axiom.

**Required**: Replace the hypothesis with a citation to ASN-0093's SubspaceConventionAxiom (specifically the SC-NEQ consequence noted there).

### Issue 4: L1cWitnessOnly axiom is restated content

**ASN-0086, "L1cWitnessOnly (AXM)"**: "The SubstrateEmissionPrimitive commits to a *witness-only* reading of L1c's existential."

**Problem**: ASN-0043's L1c is already stated as a structural existential: "Every link address `ℓ ∈ dom(L)` has a *structural inc-chain* from its home document to `ℓ`: a finite sequence... satisfies T10a's per-step admissibility constraints..." No operational re-execution is required by the existential's form. The new "axiom" adds no content; it clarifies the reading.

The clarification is consumed at exactly two sites (R0 Step 3, R7a precondition discharge). At both, the existential nature of L1c suffices without invoking a new axiom.

**Required**: Either drop L1cWitnessOnly as redundant, or recast it as a definitional remark on L1c rather than a substrate axiom.

### Issue 5: Definition of `→` reinvents foundation operations

**ASN-0086, "State transition relation"**: "The primitive dom-extending transitions are exactly the substrate-level emissions inherited from the underlying ASNs and lifted here: (i) document allocation (ASN-0036, S7a, S7d)... (ii) content emission (ASN-0036, S0–S3)... (iii) the SubstrateEmissionPrimitive..."

**Problem**: ASN-0093 explicitly defines K.σ, K.α, K.λ as the primitive operations for these three classes. The ASN cites ASN-0036's invariants (S7a, S7d, S0-S3) rather than ASN-0093's operations that satisfy them. The class-(i) Frame omits T10a's runtime activation chain ("opaque to this layer") — but ASN-0093's K.σ specifies the operation precisely and ASN-0093's allocator-chain axioms (SubAllocatorAxiom and its lemmas) make T10a's activation explicit.

**Required**: Express `→` as the union of K.σ, K.α, K.λ from ASN-0093, citing them by label.

### Issue 6: R0a/R0a-Cor1 inductive argument's discipline-propagation step lacks explicit Σ_D closure proof

**ASN-0086, "Closure of Σ_D under Emit_K"**: "Binding the R0 Step 2 construction into the signature, together with the `Σ_D` input restriction, closes `Σ_D` under Emit_K: if `Σ ∈ Σ_D`, then `Σ' ∈ Σ_D`, because the issued `→`-step is itself disciplined."

**Problem**: The claim "the issued `→`-step is itself disciplined" is asserted but the proof obligation is left implicit. Specifically, R0 Step 2's construction (Case A or Case B) is asserted to satisfy the sibling-frontier discipline, but the link from "R0 Step 2's construction" to "sibling-frontier discipline" requires showing that R0 Step 2's output never deposits at a strict prefix-extension of an existing link address — which is precisely R0a's antichain conclusion applied prospectively to the post-state. The argument is structurally tight but not fully unpacked.

Also: R0 Step 2 Case B picks "any `b ∈ dom(Σ.L)` with `home(b) = d`" without specifying which. The Emit_K function-ness lemma cites R0a-Cor1 to make the output `b`-independent, but R0a-Cor1's proof itself depends on the discipline-restricted reachability of Σ. There is a subtle circularity in the framing: Σ_D is defined via `→_D*`, but `→_D*` is defined via the discipline, which is defined via R0 Step 2's construction, whose well-definedness needs R0a-Cor1.

**Required**: Either (a) unpack the closure argument explicitly, showing that the R0 Step 2-constructed `a` is prefix-incomparable with every `a' ∈ dom(Σ.L)` *before* invoking R0a's antichain at Σ' (using only T10a sibling lemmas on `Σ` plus R0a at `Σ`), or (b) recast Σ_D as the trajectories along which every class-(iii) `→` step satisfies an externally-stated atomic discipline predicate (not appealing to R0 Step 2's construction).

### Issue 7: Stage 1 of R0a's cross-home argument relies on symmetry sketch

**ASN-0086, R0a Stage 1**: "By the same argument with `a` and `a'` swapped — every step relies only on the structural form of `≼` applied to its two variables, not on their order, and on `home` as a pure projection of its single argument — `a' ⊀ a` likewise."

**Problem**: The "by the same argument with swap" closes Stage 1 in one sentence. While the symmetry justification is correct (the predicates involved are symmetric in their argument positions), the argument leaves out the explicit substitution and re-derivation. For a foundational lemma whose conclusion is consumed downstream by every same-home appeal to disjointness across documents, the symmetric branch should be made explicit (it's short, but skipping it is exactly the "by symmetry" hand-wave that the review standards forbid).

**Required**: Either restate the swapped derivation in full or explicitly identify the symmetry as a one-line substitution of variables `(a, a', d, d') → (a', a, d', d)` in each named premise.

### Issue 8: Worked sketch does not exercise R0 Case A's first-emission construction

**ASN-0086, "Worked Sketch"**: The setup pre-establishes `a₁ ∈ dom(Σ_0.L)`; all three subsequent emissions (a₁'s own pre-existence implicitly, b₁ retraction, a₂ restoration) use Case B.

**Problem**: R0 Case A (first link emission under a document with empty homed set) constructs a non-trivial chain (`(d, 2)` spawn, sibling sweep of `s_L − 1` steps, `(·, 1)` spawn). The construction is detailed in the proof but never concretely exercised. The worked sketch's `a₁` materializes as if from setup. Per review standard "no concrete example... is a REVISE item," at least one concrete Case A trace would be valuable.

**Required**: Add a worked Case A walkthrough — e.g., starting from `Σ_{-1}` with `dom(Σ_{-1}.L) = ∅` and `d ∈ dom(Σ_{-1}.M)`, exhibit the emission yielding `a₁ = 1.0.1.0.1.0.2.1` step by step through the three-stage chain (`(d, 2)` → `1.0.1.0.1.0.1`; sibling step → `1.0.1.0.1.0.2`; `(·, 1)` → `1.0.1.0.1.0.2.1`).

### Issue 9: R7a's conformance scope hidden in proof's opening, not in the claim

**ASN-0086, R7a statement**: "For any state-affecting transition `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L`..."

**Problem**: R7a quantifies over `↝` (the categorical relation across all layers). The proof's first paragraph then narrows: "R7a is stated for layers that conform to all substrate invariants on `(Σ.C, Σ.M, Σ.L)`." The conformance assumption is load-bearing for the entire proof (L12, L12a, S0, S1 are quantified over `↝`-steps in the proof but only over `→`-steps in their source ASNs), but appears only in the proof body rather than in the claim statement.

**Required**: Lift the conformance assumption into R7a's precondition explicitly: "For any state-affecting transition `Σ ↝ Σ'` from a layer conforming to L12, L12a, S0, S1 over `(Σ.C, Σ.M, Σ.L)`..."

### Issue 10: Definition of `Σ.L`-affecting effect lacks a concrete witness for the non-trivial branch

**ASN-0086, R7a "Worked example"**: A composite create-document-with-initial-link is decomposed into class-(i) prefix + class-(iii) emission.

**Problem**: The worked example exercises the *length-2* decomposition (one prefix + one emission). The claim allows arbitrary `m ≥ 1` decompositions interleaving multiple class-(i) and class-(iii) steps. A composite operation emitting two links homed at *different* fresh documents would exercise the genuinely interleaved case (two class-(i) prefixes interleaved with two class-(iii) emissions). Without exercising this, the proof's iteration loop is exercised only at iteration 1.

**Required**: Add a worked decomposition of an `m = 4` composite (e.g., create-two-fresh-documents-each-with-an-initial-link) to verify that the iteration's home-document precondition discharge works across distinct fresh home documents.

### Issue 11: WP Case 1 conjunct SFD(Σ) load-bearing but not formally specified

**ASN-0086, WP Case 1**: "SFD(Σ) — the sibling-frontier emission discipline holds along the `→`-chain reaching Σ..."

**Problem**: `SFD(Σ)` appears as a wp conjunct without a formal specification. The Implementation Notes describe the discipline informally but don't expose it as a checkable predicate over `Σ` (or its trajectory). A wp expression with an informal predicate is not a wp.

**Required**: Define SFD precisely. Candidate form: "`Σ ∈ Σ_D`" — but Σ_D is defined via the discipline, so this is circular without a direct atomic predicate. The cleanest formulation is "Σ is in the image of the disciplined-reachable subset," but this needs to be expressed as a checkable property (e.g., as the conjunction "for every existing class-(iii) step in the trajectory, the emitted address was R0 Step 2-constructed" — still trajectory-bound, not Σ-bound).

## OUT_OF_SCOPE

### Topic 1: Higher-arity link relations

The ASN restricts `L_K^Σ` to standard-triple links and notes "Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here." This is appropriate scoping.

**Why out of scope**: Multi-arity relational vocabulary is a substantive new direction.

### Topic 2: Atomicity and concurrency

The Open Questions ask "Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?" The ASN's `→` is single-step but says nothing about multi-thread concurrency.

**Why out of scope**: Concurrency model is a future ASN.

### Topic 3: Type catalog dynamics

The Open Questions ask whether two layers independently choosing colliding type addresses could interact. The ASN treats `T_admissible` as static.

**Why out of scope**: Type catalog evolution is a future ASN.

### Topic 4: Cardinality bounds on nullification

The Open Questions ask "What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`?"

**Why out of scope**: Quantitative bounds are a future ASN.

VERDICT: REVISE
