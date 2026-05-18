# Review of ASN-0086

## REVISE

### Issue 1: R7a's proof gap for ↝-steps that add documents
**ASN-0086, R7a — NoExtraClassAffectsL**: "there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_n` (`n ≥ 1`) of class-(iii) `→`-steps with `Σ_n.L = Σ'.L`"
**Problem**: The proof says "the substrate emission primitive's class-(iii) frame admits, at state `Σ_{k-1}`, a `→`-step ... provided `a_k ∉ dom(Σ_{k-1}.L)`". But the substrate emission primitive also requires L1a at Σ_{k-1}, i.e., `home(a_k) ∈ dom(Σ_{k-1}.M)`. Class-(iii) steps don't extend `dom(M)`, so `dom(Σ_{k-1}.M) = dom(Σ.M)`. If the original `↝`-step is a composite that added both a fresh document `d` and a fresh link `a_k` with `home(a_k) = d`, then `home(a_k) ∉ dom(Σ.M)` and no class-(iii) step at Σ can emit `a_k`. The claim's "purely class-(iii) finite sequence" formulation fails for such composites.
**Required**: Either (a) restrict R7a to `↝`-steps with `dom(Σ'.M) = dom(Σ.M)`; (b) reformulate as "the `Σ.L`-affecting effect of any `↝`-step decomposes into class-(iii) `→`-steps possibly interleaved with class-(i) and class-(ii) setup steps"; or (c) argue the proof obligation explicitly that `home(a_k) ∈ dom(Σ.M)` for every `a_k ∈ Δ`, contradicting the categorical "any-layer" framing.

### Issue 2: R0 Step 4's grouped L-invariant verification
**ASN-0086, R0 proof, Step 4**: "L2, L5, L6, L8, L11b, L13 are definitional/existential properties of the substrate model preserved by membership in the same model class. L4(c), L7, L9, L10 are permissions licensing the emission's content, not state-bound values."
**Problem**: Six invariants dismissed in one sentence, four more in another. R5's verification later argues comprehensively against L-invariants by category; R0 Step 4 should match that depth. Specifically, each grouped invariant should be discharged with one line each (e.g., "L2: home(a) is computed from a alone; a is fixed; ✓"). The current treatment is proof-by-similarly across ten distinct invariants.
**Required**: Per-invariant discharge of L2, L5, L6, L8, L11b, L13 — one sentence each. The "permissions, not values" group (L4(c), L7, L9, L10) is acceptable as-is.

### Issue 3: Inconsistency between State transition relation and Substrate emission primitive
**ASN-0086, Setup**: State transition relation paragraph: "(iii) `Emit_K` as defined later in this note (which composes the underlying ASN-0043 link-store extension) extends `dom(Σ.L)` by one address." Substrate emission primitive paragraph: "The substrate admits, as its primitive emission for the link store, emit-at-any-L1c-conforming-fresh-address ..."
**Problem**: The first identifies class (iii) with Emit_K (disciplined subset). The second describes class (iii) as the broader L1c-conforming primitive. Emit_K is later defined as the *narrower* disciplined version. Either class (iii) is the disciplined Emit_K (then the substrate emission primitive's broader admission is wrong) or class (iii) is the broader substrate primitive (then "(iii) Emit_K" misidentifies). R7a's proof and R0a's discipline-conditionality depend on getting this right.
**Required**: Clarify whether `→` class (iii) is the disciplined Emit_K or the broader substrate primitive. The most natural reading is: class (iii) is the broader substrate primitive (so R7a's existence claim is on broader →-steps), and Emit_K is the relational layer's discipline-restricted subset (so the relational-layer corollary follows by definitional commitment, not by class (iii) coinciding with Emit_K).

### Issue 4: Convention — RetractionDirectionality is load-bearing without principled rationale
**ASN-0086, Convention — RetractionDirectionality**: "For the retraction coverage class [R], the to-set carries the retraction's targets ... and the from-set is reserved for attribution-bearing endset content."
**Problem**: The Definition of `nullified(Σ)` quantifies over `coverage(G')` only. The Convention is therefore load-bearing: a reverse or symmetric convention would yield a different `nullified` and a different `A_K`. The note acknowledges this ("A reformulation under the reverse convention would replace G' with F' here") but doesn't justify why the to-set convention is chosen over alternatives. This is a chosen direction with no principled grounding; downstream layers building on `A_K` inherit the convention without recourse.
**Required**: Either (a) provide a principled rationale (e.g., L7's directional-flexibility leaves the choice to the link type, and this Convention is the relational layer's adoption); or (b) restate `nullified` symmetrically as `coverage(F') ∪ coverage(G')` and note that the Convention narrows it.

### Issue 5: Emit_K's seed-independence is conditional on the trajectory, not on the state
**ASN-0086, Emit_K Definition, "Case B's seed-independence" paragraph**: "`Emit_K` is a function of `(Σ, d, F, G)` on the disciplined-reachable sub-domain."
**Problem**: The function-ness claim restricts Emit_K's domain to states Σ reachable from a Σ_0 with `dom(Σ_0.L) = ∅` via `→_D*`. This is a trajectory-level constraint, not a state-level one — two states Σ_1, Σ_2 with identical `Σ_i.L` may have different reachability classifications, and Emit_K would be a function on one but non-deterministic on the other. The note acknowledges: "Outside that sub-domain ... `Emit_K` remains an operation whose output address may depend on which seed b the implementation chooses".
**Required**: Either (a) elevate the sibling-frontier discipline to a substrate-level commitment (then every state has the contiguous-prefix property and Emit_K is unconditionally a function), or (b) state the function-ness conditionality at the signature level rather than as a post-hoc restriction. The current treatment leaves Emit_K with a function/relation duality based on trajectory history, which is operationally awkward.

### Issue 6: Meta-prose accretion flagged by the review-mode.anti-bloat classifier
**ASN-0086, multiple locations**: The note has accumulated meta-prose around forward references, hypothesis classifications, and naming choices. Specific items:

(a) **"Terminology note" in zero-count depth Definition**: Explains naming choice ("chosen to avoid clashing with T4b's 'element field'"). This is meta-prose; the term either fits or doesn't, but justifying its name doesn't advance reasoning.

(b) **"Hypothesis status" paragraph in *Implementation hypotheses***: "The Sparse-allocator hypothesis is substrate-defining ... The remaining two disciplines are per-claim conditionalities, each tagged at its claim's site." Pure meta-prose classifying hypotheses without advancing them.

(c) **"Implementation realizability" note**: References to udanax-green's `findisatoinsertmolecule (granf2.c:170–175)`. Implementation evidence that doesn't ground a claim; flag-worthy under the classifier.

(d) **R0a's "Initial-state assumption" paragraph**: Lengthy meta-prose justifying the antecedent's structural role: "Operationally, the substrate's initial state at system genesis has `dom(Σ.L) = ∅` ... the existential's structural role is to make the empty-link-store base case explicit as the anchor of the induction." This is justification for the proof technique, not the proof itself.

(e) **R4's "Remark on the underlying structural mechanism"**: Re-derives L14's chain across L0/L0a/T3/T7 even though L14 is directly invoked. The note then says "R4 invokes only the consolidated L14, deferring this chain to ASN-0043's derivation" — but having said that, the entire remark is redundant.

(f) **R4's "Remark on L14's scoped form"**: Forward-pointing rationale to "future work" — "Where future work admits s_L-resident content, R4 would be replaced..." Speculative, not load-bearing.

(g) **Definition — TypedRelation's "Rationale" sub-note**: Defensive prose justifying coverage-equivalence over literal-endset matching. The Definition is precise; the rationale belongs elsewhere or omitted.

(h) **The `↝` categorical relation paragraph**: "The definition is given by quantifier range rather than by enumeration of mechanisms" — defensive justification of definitional approach.

(i) **Setup's Frame conditions paragraph closer**: "These commitments constrain only the visible values of `Σ.C, Σ.M, Σ.L` after the transition; concrete implementations may maintain auxiliary backing structures (index trees, POOM entries) without violating any frame condition." Implementation guidance, not specification.

**Required**: Remove or compress each of (a)-(i). Test: if the prose can be deleted without breaking a proof or making a definition ambiguous, delete it.

### Issue 7: R5's Stage 2 use-site inventory
**ASN-0086, R5 — TupleSelfTargeting, Stage 2**: "Enumeration of ASN-0043's L-invariants by what they constrain confirms no opposition: *address-side constraints* (L0, L0a, L1, L1a, L1b, L1c, L11a) name the link's address ... *slot-structure constraints* (L3, L5, L6, L8, L10) name arity, slot semantics, directionality, type-equivalence, and type hierarchy ..."
**Problem**: This is a use-site inventory of every L-invariant in ASN-0043 with categorical labels. The actual lemma needs L4(c) + L13 + R0 (named in Stage 1). The enumeration is defensive — proving non-opposition by exhaustive cataloging — when the load-bearing fact is "no L-invariant constrains endset target content beyond L4(c)'s explicit permission".
**Required**: Reduce Stage 2 to: "No L-invariant constrains endset target content beyond L4(c); the construct is therefore admissible by L4(c) + L13 + R0's invariant-preservation argument at Step 4."

### Issue 8: Multiple "see X below" / "deferred to Y" patterns
**ASN-0086, multiple locations**:
- "By the Sparse-allocator hypothesis (below, *Implementation hypotheses*) ..."
- "(per the asymmetry noted above)"
- "establishes the construct as well-formed and span-target-admissible at the link subspace"
- "the regime distinction governing exactly when a class-(iii) `Emit_K` step contributes to `A_K` versus to `L_K \ A_K` is established at Emit_K's *A_K^{Σ'} membership* note above"

**Problem**: The classifier flags "multiple paragraphs in different sections defer to the same downstream location". Several spots forward-reference within the document, and several backward-reference to prior paragraphs by italicized name. The cumulative effect is a reading experience requiring frequent cross-section traversal.
**Required**: Linearize: state the dependency at first use; cross-references that the reader can resolve from a single read-through don't need named back-references.

### Issue 9: Worked Sketch covers one cycle without `↦`-transition example
**ASN-0086, Worked Sketch**: The sketch instantiates Step 1 (Nullify) and Step 2 (Restore by re-emission), both pure `→`-transitions.
**Problem**: R6c-Corollary lifts persistence to `↦` (including arrangement modifications). The worked sketch doesn't illustrate this corollary — no `↦`-step is exhibited where arrangement changes between Σ_1 and some Σ_arr while `nullified(Σ_arr) = nullified(Σ_1)` is maintained. The Corollary is stated but never instantiated.
**Required**: Either (a) extend the worked sketch with an `↦`-step modifying arrangement and verifying `A_K^{Σ_arr} = A_K^{Σ_1}`; or (b) drop R6c-Corollary if it's not load-bearing for the relational layer's substrate vocabulary.

### Issue 10: SharedDepthOneAllocator lemma's step (d) is asserted, not proved
**ASN-0086, Setup, SharedDepthOneAllocator Lemma, step (d)**: "*Conditional independence of depth-2 subspace-specific allocators.* ... they are opened by *distinct* spawn pairs `(d.0.s_C, 1) ≠ (d.0.s_L, 1)` (parent tumblers distinct by L0 + the subspace-distinctness hypothesis), so T10a imposes no joint constraint and they evolve independently."
**Problem**: "T10a imposes no joint constraint" is asserted but not derived. T10a's at-most-once is on spawn pairs `(t, k')`, so distinct `(d.0.s_C, 1)` and `(d.0.s_L, 1)` are independent by T10a's structure. The proof would benefit from naming the at-most-once axiom by clause and showing the two pairs satisfy distinctness directly.
**Required**: One additional sentence citing T10a's at-most-once axiom and showing `(d.0.s_C, 1) ≠ (d.0.s_L, 1)` from `s_C ≠ s_L` (subspace-distinctness hypothesis).

## OUT_OF_SCOPE

### Topic 1: Multi-arity links and their projections
**Why out of scope**: The note explicitly restricts to standard-triple links (arity 3); higher-arity links (admitted by L3) are present in `dom(Σ.L)` but outside `L_K`'s scope. This is acknowledged in the Open Questions list (item 2). A separate ASN would be needed to extend `L_K^{(n)}` to higher arities.

### Topic 2: Concurrency and atomicity guarantees
**Why out of scope**: The note treats `→` as one-step substrate transitions but doesn't address concurrent observation or emission. Open Question 5 acknowledges this. A future ASN on the operational layer would need to address consistency models.

### Topic 3: Interaction with arrangement modifications
**Why out of scope**: The `↦` relation includes arrangement modifications (from ASN-0036), but R6c-Corollary is the only place this layer interacts with arrangements. The full integration with strand-model arrangements is the subject of ASN-0047 (state transitions), not this ASN's relational vocabulary.

### Topic 4: Type catalog coordination across layers
**Why out of scope**: Open Question 8 raises this: "what happens when two layers independently choose colliding type addresses?" This is a coordination concern at the layered architecture level, not a substrate property.

### Topic 5: Relaxation paths from R0a-Cor2's depth-2 narrowing
**Why out of scope**: Open Question 7 raises whether the sibling-frontier discipline can be relaxed to admit deeper-sited link addresses. A relaxed discipline would require re-deriving R0a's antichain and Nullify's single-tuple scope over a tree of allocators. This is a substantial design exploration, not a finding within this ASN.

VERDICT: REVISE
