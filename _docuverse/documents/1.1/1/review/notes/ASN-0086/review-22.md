# Review of ASN-0086

## REVISE

### Issue 1: R0a's sibling-stream invariant strictly narrows L1b under the discipline
**ASN-0086, R0a proof (sibling-stream invariant)**: "every link address lies in its home document's link-element-field sibling stream, anchored at the Case A base `home(a).0.s_L.1`."
**Problem**: The Case A base has the form `d.0.s_L.1` with `#E = 2`, and `inc(·, 0)` preserves length (TA5(c)). The invariant therefore entails `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)` reachable under the discipline. This is strictly stronger than L1b's `#E(a) ≥ 2`. The ASN never flags this structural consequence, yet it has downstream implications: under the discipline, link addresses cannot be sited at element-field depth 3 or greater. A reader reasonably wonders whether the link model admits such deeper-sited links and, if so, whether they fall outside this note's substrate.
**Required**: Add a one-paragraph remark in the R0a section explicitly noting `#E(a) = 2` strictly under the discipline, with the structural reason (Case A produces `#E = 2`; Case B preserves `#E` via `inc(·, 0)`; induction). Either flag this as a deliberate narrowing of L1b (with rationale tied to the udanax-green flat-link-domain practice) or add an Open Question on whether the discipline should admit higher-depth siblings via additional Emit_K cases.

### Issue 2: R6 Consequence (d) anticipates R7's reduction without forward reference
**ASN-0086, R6 Consequences (d)**: "All visible state-transforming relational-layer operations reduce to `Emit_K`. File a comment, close it, retract a citation, retire a document..."
**Problem**: This consequence is presented unconditionally under R6 (ActiveSubsetWellDefinedness), but the actual reduction is R7 (NullifyIsEmit), which appears later. R6 alone establishes "`A_K^Σ` is computable from `Σ.L`," not the reduction claim. R7's own conclusion is properly hedged ("given the commitment" to Emit_K = R0 Step 2), but R6's anticipatory phrasing does not carry that hedge. Section-header text ("These three operations span all visible substrate change") repeats the unhedged form. Readers encountering R6 first see a strong claim without its supporting lemma or its stipulated half.
**Required**: Move consequence (d) under R7, or add a forward reference (e.g., "anticipating R7 below") that flags the dependency. The hedging on R7's stipulated half should propagate forward to every site that asserts the reduction unconditionally.

### Issue 3: R5's permission modality is consumed implicitly in downstream consequences and operations
**ASN-0086, R5 Consequences (a)–(d) and Definition of Nullify**: R5 is correctly labeled META (permission claim), with the Modal note acknowledging the difference from positive lemmas. Yet consequences (a) *Retraction*, (b) *Resolution*, (c) *Agent provenance* are stated as substrate facts ("A tuple in a designated relation `L_R` whose to-set contains..."), and Nullify's definition consumes R5's permission to embed a tuple address `a` in an endset.
**Problem**: A positive lemma would witness the construction (concretely exhibit an emission state Σ' with such an endset and verify all L-invariants). R5 instead enumerates non-opposing invariants; the witness is hidden behind a separate R0 invocation. Readers see consequences as facts but must reconstruct the dependency on R5-permission + R0-construction to know what supports them. The "may appear in the from-set or to-set" wording at R5 should propagate visibly into the operational definitions that consume it.
**Required**: Either restructure R5 into a positive emission lemma (with explicit witness construction, similar to R0's Step 2 and Step 4), turning consequences into corollaries; or in each consequence and in Nullify's definition, briefly trace the dependency chain "R5 permission + R0 construction at the chosen home → witness state with the required tuple". The Modal note alone is too far upstream to ground each downstream use.

### Issue 4: The "Shared depth-1 element-field allocator commitment" is labeled as commitment but largely entailed
**ASN-0086, Setup ("Shared depth-1 element-field allocator commitment")**: "This commitment is *consistent with* the foundation invariants and adopted as a model commitment of this note... we adopt it as a working commitment rather than claim it as a derived theorem."
**Problem**: The ASN's own argument shows L0 (subspace routing on first element-field) + T10a's at-most-once child-spawn axiom on `(d, 2)` + S7d's `zeros(d) = 2` jointly force the structure: only one allocator can be spawned at `(d, 2)`, that allocator is A_d, and its enumeration must index subspace identifiers (since L0 routes by E_1). The hedging "Strictly stronger alternatives that the foundation invariants do not literally rule out are not pursued here" leaves it unclear what specific alternatives are admitted. Either the commitment is forced (in which case it's a corollary, not a commitment) or there are genuine foundation-compatible alternatives that should be named.
**Required**: Tighten the argument to either (a) prove the commitment as a corollary of L0 + T10a + S7d (eliminating the hedge), or (b) exhibit a concrete L0-compatible alternative model and explain why this note rejects it. The current middle stance — entailed in argument but labeled commitment — leaves R0's Case A correctness on uncertain footing.

## OUT_OF_SCOPE

### Topic 1: Setup hypothesis relaxation under L14's native scoped form
**Why out of scope**: Globally `s_C`-resident content is a working hypothesis consumed at R0 (L14a-preservation step), R4, and R5. The slice-wise reformulation under L14's native scoped form is correctly identified in the Open Questions section as future work, not as a gap in this note.

### Topic 2: Higher-arity links (|Σ.L(a)| > 3)
**Why out of scope**: L3 admits N ≥ 3, but `L_K^Σ` is defined only over arity-3 standard triples. The Open Questions section flags whether higher-arity relations should use `L_K^{(n)}` or binary projections. This belongs in a future extension ASN.

### Topic 3: Sibling-frontier discipline elevation to substrate-level
**Why out of scope**: R0a, R0a-Cor1, and Nullify's single-tuple-scope are discipline-conditional. Whether to tighten Emit_K's spec or the substrate primitive to make the discipline automatic is correctly identified as future work in the Open Questions.

### Topic 4: Concurrency, atomicity, ordering of Observe
**Why out of scope**: The ASN does not address atomic Emit/Observe semantics, ordering guarantees on Observe results, or cardinality bounds on `nullified(Σ)`. These are operational concerns above the substrate model and are flagged in Open Questions.

### Topic 5: Allocator state evolution in `→`
**Why out of scope**: The Coarsening section acknowledges that `→` is one admissible projection of ASN-0034's transition relation, with finer alternatives (exposing allocator activation as separate steps) requiring different R-claim proof structures. This abstraction-choice question is correctly out of scope.

VERDICT: REVISE
