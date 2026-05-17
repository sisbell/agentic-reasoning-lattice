# Review of ASN-0086

## REVISE

### Issue 1: R0 Step 4's bulk discharge of L-invariants conflates invariant types

**ASN-0086, R0 Step 4, "Routine L-invariants discharged uniformly via FramePreservation"**: The paragraph bundles L11b alongside L2, L12, L4, L8, L13, etc.

**Problem**: L11b (NonInjectivity) is an *existential* about model extensibility — "(E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a))". It is not a preservation property in the same sense as L12 (LinkImmutability). Citing FramePreservation specialization (a) for "L11b permits, does not require, value-level coincidence" is the wrong shape of justification — L11b's existential remains witnessable trivially because the model class includes Σ' extending Σ with duplicates, not because the class-(iii) frame preserves any specific value-level fact. Similarly, L4(c) is the *enabling* invariant for cross-subspace endset content; calling it "preserved" alongside L13 (which is a definition of valid targets, not an invariant per se) conflates definitional permissions with preservable predicates.

**Required**: Separate the bundle into three distinct shapes: (a) genuine invariants whose values the frame preserves (L12, L12a, L12b, L-fin); (b) definitional or existential claims for which the post-state continues to be a member of the right class (L11b, L13, L5, L6); (c) enabling permissions used constructively at the emission (L4(c), L7, L9, L10). The current bundling reads as exhaustiveness for its own sake.

### Issue 2: R5 Stage 2's exhaustive class-partition is an "exhaustiveness claim" anti-bloat pattern

**ASN-0086, R5 Stage 2**: "We argue in two stages... Stage 2 — no invariant opposes the construct. The substrate-wide invariant base partitions into three classes... [Class i, Class ii, Class iii, each discharged by a single argument]."

**Problem**: Stage 2 enumerates every ASN-0034 / ASN-0036 / ASN-0043 invariant and dismisses each as not opposing. This is precisely the "exhaustiveness claim" pattern flagged by the anti-bloat classifier. The genuine question is: "does any single invariant *plausibly* constrain endset content?" The answer is no, because L4(c) is the only invariant that constrains endset targets and it explicitly permits link-subspace targets. A two-line argument identifying L4(c) as the only relevant invariant and observing that it admits the construction would suffice.

**Required**: Replace the three-class partition with a focused argument: "L4(c) is the only L-invariant that constrains endset target addresses; it permits link-subspace targets directly. No other invariant on the ASN-0043 / ASN-0034 / ASN-0036 stack constrains endset content. Therefore non-opposition follows from L4(c) alone."

### Issue 3: Triple-redundant hypothesis tracking

**ASN-0086, throughout**: Each R-claim carries a three-field headline tag `[setup: ..., discipline: ..., stipulation: ...]`; many also carry inline `[Setup-required]` or `[discipline-conditional]` discussion text; and the closing "Hypothesis dependency view" table re-presents the same dependencies in tabular form.

**Problem**: Three independent mechanisms track the same hypothesis dependencies. The headline tags alone suffice for citation; the inline discussion text duplicates this; the table re-presents it with an "indirect via other R-claims" column that could be a single sentence per claim. This is the "use-site inventory" pattern: the document inventories its own dependency structure across multiple slots.

**Required**: Pick one mechanism. The headline three-field tag is sufficient if extended with one parenthetical for indirect dependencies. Drop the closing table and the inline discussion paragraphs that restate the tags.

### Issue 4: Model Commitments section is itself a use-site inventory

**ASN-0086, "Model Commitments" section**: The section enumerates five hypotheses (Setup, Subspace-distinctness, Sibling-frontier discipline, Unit-depth retraction discipline, R7b stipulation) with status notes and tag-form conventions, then announces that each is "introduced in detail below".

**Problem**: The substance of each hypothesis is restated where it's first consumed (Setup before R0, sibling-frontier before R0a, etc.). The Model Commitments section is purely a navigation aid — meta-prose about how to read the rest of the document. The tag-form convention paragraph explains a notation that the document then uses; the table at the end re-presents the same information. The five-bullet enumeration is essay content in a structural slot.

**Required**: Remove the Model Commitments section. Introduce each hypothesis at its first consumption site only, with the three-field tag convention explained inline at first use.

### Issue 5: R7's composite framing inflates a stipulation into a "lemma"

**ASN-0086, R7**: R7 is presented as a "composite" lemma whose two sub-claims R7a (PROVEN) and R7b (STIPULATED) are numbered as if they had similar standing. The Properties Introduced table labels R7 as COMPOSITE-typed, R7a as LEMMA, R7b as DEF.

**Problem**: R7b is essentially the *definition* of what "the relational layer" is (it commits to Emit_K as the sole class-(iii) primitive). Calling R7b a numbered sub-claim alongside R7a obscures that R7b is definitional, not theorem-like. The "composition" of a derivation with a definition is application of the definition, not a separate proof step. The repeated defensive language ("stipulation-conditional", "model commitment, not derived", "the asymmetric standing of its two sub-claims hoisted into the citation form") is meta-prose justifying the framing rather than advancing content.

**Required**: Restate as: (a) R7a (LEMMA) — no `Σ.L`-affecting transition exists outside class (iii). (b) Definition of the relational layer — its state-affecting operations are {Emit_K, Observe_K, Nullify}; Nullify is `Emit_R` with designated argument shape. (c) Consequence (one-line) — under this definition, R7a implies all visible relational-layer state change reduces to Emit_K. Drop the R7b/R7-composite numbering.

### Issue 6: R0a-Cor2 has more discussion than proof

**ASN-0086, R0a-Cor2**: The proof is four lines. The "Narrowing — design-vs-implementation tension" paragraph that follows is substantially longer than the proof, discussing Nelson's design intent, the udanax-green implementation, separability from R0a, and forward-pointers to Open Questions.

**Problem**: This is the "essay content in structural slots" pattern. The narrowing-versus-design discussion is genuinely interesting context but does not advance the R0a-Cor2 claim; it justifies the design choice the claim records. The same content also appears in the Open Questions section as a relaxation question. The duplication is the "two paragraphs in different sections say the same thing in different words" pattern.

**Required**: Compress to one sentence: "R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2`, matching the udanax-green implementation; relaxation to deeper-sited links is discussed in Open Questions." Drop the multi-paragraph tension discussion.

### Issue 7: Nullify's "Remark on the role of P3" is defensive justification

**ASN-0086, Definition of Nullify**: The Remark explains at length why P3 is listed as a separate precondition rather than being discharged automatically by R0a's discipline. The paragraph distinguishes "P3's role" from "R0a's role", names what each contributes, and notes P3 is "automatic at every state for every `a ∈ dom(Σ.L)`" under the discipline.

**Problem**: The Remark is meta-prose justifying a design choice. The substantive content — that P3 is the prior-state condition and the discipline supplies the post-state antichain — could be a single sentence in the Definition's precondition discussion. The detailed decomposition of "what P3 does versus what the discipline does" is defensive against a hypothetical reader who might think P3 is redundant.

**Required**: Replace with one sentence in the Definition: "Under the sibling-frontier discipline, P3 is automatic at every reachable state; it is stated as an explicit precondition to keep Nullify's contract usable for systems where the discipline is not yet a global guarantee."

### Issue 8: Worked Sketch Step 5 sub-step 5.2 admits to being schematic

**ASN-0086, Worked Sketch Step 5, Sub-step 5.2**: "Arrangement-modifying transitions are out of scope for ASN-0086 (owned by ASN-0036 and its extending editing-operation ASNs), so `Σ_4 ↦ Σ_5` is exhibited schematically: take it to be *any* arrangement-modifying transition admitted at Σ_4."

**Problem**: The worked sketch is framed as "concrete instantiation" with "every set-theoretic claim verified by direct inspection". Sub-step 5.2 then admits the arrangement-modifying step is not concrete. The substantive verification at Σ_5 then proceeds purely from the frame condition (`Σ_5.L = Σ_4.L`), which makes the sub-step a frame-application exercise rather than a concrete exhibition. The concrete-ness framing is undermined.

**Required**: Either (a) drop sub-step 5.2 — R6c-Corollary's content is the frame application, which can be stated as one sentence rather than exhibited as a "step"; or (b) reframe sub-step 5.2 as "frame-condition exercise" rather than concrete instantiation, acknowledging that the arrangement-modifying step is opaque.

### Issue 9: Appendix A.1 re-explains substrate primitive commitment from the body

**ASN-0086, Appendix A.1**: "At the allocator-state level... the substrate primitive's atomic class-(iii) step implicitly discharges T10a's child-spawn admissibility at each intermediate spawn pair on the L1c witness chain, in one indivisible action..."

**Problem**: The body's substrate emission primitive section already states this commitment in load-bearing detail (the *Allocator-state commitment* paragraph). A.1 re-explains it with additional Nelson citations and udanax-green references but adds no new mathematical content. This is the "essay content" pattern in an appendix slot, plus the "explains why the axiom is needed rather than what it says" sub-pattern.

**Required**: Either fold A.1's substantive citation (the Nelson ghost-element quote) into the body's commitment paragraph, or drop A.1 entirely if the body already suffices. Appendix A.2 (the coarsening discussion) contains substantive content and can stand.

### Issue 10: Unit-depth retraction discipline placed structurally inconsistently

**ASN-0086, between Emit_K and Nullify Definitions**: The "Definition — Unit-depth retraction discipline" is placed between Emit_K and Nullify, while the sibling-frontier discipline is defined earlier (before R0a). The two disciplines play parallel roles — both are caller-level hypotheses on class-(iii) emission practice — but live in different structural slots.

**Problem**: Structural inconsistency forces readers to discover the second discipline mid-operation-definition, then refer back. The body acknowledges this with phrases like "Distinct from (3) — orthogonal in scope" in the Model Commitments index.

**Required**: Move the Unit-depth retraction discipline Definition to the Model Commitments section (alongside Setup, Subspace-distinctness, and Sibling-frontier discipline), or co-locate all four hypotheses in a single section structured uniformly. Currently they're split across Setup-section + body + Emit_K-vicinity, with the Model Commitments index as the only place they're collected.

### Issue 11: R6b's derivation as "from quantifier-range choice" is under-shown

**ASN-0086, R6b**: The justification is presented as a three-step derivation ("Step 1 — quantifier-range identification", "Step 2 — witness sufficiency", "Step 3 — non-recursion") with the conclusion that "deciding `a ∈ nullified(Σ)` requires only one level of existential check".

**Problem**: The "derivation" is essentially restating the Definition's quantifier range three times. R6b's content is that the Definition's choice of `L_R^Σ` (rather than `A_R^Σ`) means the predicate doesn't recurse. This is a one-line observation: "By the Definition's quantifier range over `L_R^Σ` (the audit slice, not the active subset), `a ∈ nullified(Σ)` is witnessed by any retraction tuple in `L_R^Σ` whose to-coverage contains `a`, regardless of that witness's own active-subset status." The three-step structure inflates the observation. The subsequent two-emission worked example (Σ_1, Σ_2) is genuine illustration and should stay.

**Required**: Compress R6b's main justification to one paragraph. Keep the (1)/(2) emission example as illustration.

## OUT_OF_SCOPE

### Topic 1: Multi-arity link relations

**Why out of scope**: The ASN restricts to standard-triple links and explicitly defers `L_K^{(n)}` for higher arity to a separate development. The Open Questions section lists this. Extending the active-subset machinery to multi-arity is a future-ASN concern.

### Topic 2: Concurrent emit/observe consistency model

**Why out of scope**: The ASN treats `→` as sequential. Concurrency semantics, atomicity of `Emit_K` against `Observe_K`, and observable consistency models are not addressed; the Open Questions section flags them.

### Topic 3: Relaxation of the sibling-frontier discipline to admit deeper sub-links

**Why out of scope**: R0a-Cor2 records the narrowing; Open Questions lists the relaxation. Reformulating R0a's sibling-stream invariant over a tree of allocators is a separate development.

### Topic 4: Type catalog coordination across layers

**Why out of scope**: The ASN takes `T_admissible` as unconstrained per L9. Coordination protocols and collision handling between layers choosing type addresses are higher-layer policy.

VERDICT: REVISE
