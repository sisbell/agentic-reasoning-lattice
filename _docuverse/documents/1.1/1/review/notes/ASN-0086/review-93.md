# Review of ASN-0086

## REVISE

### Issue 1: Worked Example Step 0 derives the same address twice
**ASN-0086, Worked Sketch, Step 0**: the operational K.λ deposit computes `a₁ := [d.0.s_L.1] = 1.0.1.0.1.0.2.1`, and then the immediately following paragraph — "*Structural witness from ASN-0093*. ASN-0093's anchor construction realizes `a₁` directly (witnessed by ChainDiscipline + FirstEmission, ASN-0093 — not operationally executed by K.λ)" — re-derives the identical value `1.0.1.0.1.0.2.1` via `b_C(d)`, `b_L(d)`, `t_1^L(d)`.

**Problem**: Two paragraphs compute the same `a₁` by different routes, and the second is explicitly flagged as "not operationally executed." This is the "two paragraphs say the same thing in different words" pattern. The anchor arithmetic adds nothing the K.λ emission rule did not already fix.

**Required**: Delete the "Structural witness" paragraph, or fold a one-clause cross-check ("`= t_1^L(d)` by FirstEmission") into the operational derivation.

### Issue 2: R5 Consequences are a downstream-consumer inventory
**ASN-0086, R5 Consequences**: "(a) *Retraction.* … (b) *Resolution.* … (c) *Agent provenance.* … (d) *Higher-order predicates.*"

**Problem**: This enumerates four downstream constructs (retraction, resolution, provenance, predicate machinery) that R5 makes possible. Retraction is then re-specified formally as the Nullify operation; resolution/provenance never appear again except as motivating prose. This is the "definition's introduction enumerates downstream consumers" pattern — a use-site inventory rather than a property of the self-targeting lemma.

**Required**: Reduce to the single substantive consequence (self-targeting enables Nullify, formalized below). Drop the resolution/provenance/predicate catalog or move it to a non-normative note.

### Issue 3: Consequence-block essay content and typology scaffolding
**ASN-0086, R3 Consequence (d)**: "*No information loss.* No compaction, no garbage collection, no archive tier removes tuples from `L_K`." Similarly R4 Consequence (c) "*Lifecycle separation*", R6c Consequence (a) "*Operational vs. historical views.*"

**Problem**: These [ARCHITECTURE]-tagged bullets restate the monotonicity/disjointness theorems in prose without advancing any argument. The `[COROLLARY]/[POLICY]/[ARCHITECTURE]` tag system plus the repeated cross-reference "(Typology per R2's Consequences key.)" is structural overhead the precise reader must navigate around. A reader checking R3 needs the theorem, not a paragraph asserting there is "no garbage collection."

**Required**: Cut the architecture-essay bullets; retain only consequences that are formally derived and load-bearing downstream. Remove the typology key and the back-references to it.

### Issue 4: "The Two Foundational Sets" restates imports with defensive justification
**ASN-0086, The Two Foundational Sets**: "L0 supplies what an external `s_C`-residency hypothesis would otherwise have to assume." Also the parallel paragraph: "Wherever this note needs distinct content/link subspace identifiers, we cite SC-NEQ rather than re-asserting it."

**Problem**: These paragraphs justify *why* the foundation import suffices and *why* no auxiliary hypothesis is needed — meta-prose about the import discipline rather than content. A single citation ("content is globally `s_C`-resident by ASN-0093 L0; `s_C ≠ s_L` by SC-NEQ") carries the whole load.

**Required**: Collapse the two import paragraphs to their citations; delete the "would otherwise have to assume" / "rather than re-asserting" justifications.

### Issue 5: "Necessity of clause (b)" is a justification sub-argument lodged inside the R7a mega-proof
**ASN-0086, R7a proof, discharge (4)(iii)**: "*Necessity of clause (b).* The tumbler `a* = [d.0.s_L.1.1]` is T10a-conforming and L-invariant-admissible … yet lies off `A_L(d)`'s sibling-frontier chain … clause (b)'s frontier condition excludes it."

**Problem**: This is a necessity-of-the-hypothesis aside explaining *why* clause (b) is needed, embedded mid-proof in an already very long argument that the reader must hold in suspension. Per the anti-bloat guidance, the concrete `a*` counterexample is legitimate content, but its placement inside the determinism discharge interrupts the replay argument.

**Required**: Relocate the `a*` necessity remark to the Definition of substrate-conforming layer (where clause (b) is stated), and keep the R7a proof on the replay-determinism line.

### Issue 6: WP Case 1 labels a sufficiency claim as a weakest precondition
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a)`."

**Problem**: The text shows `P0 ∧ P1` *suffices* (P1 + L12a discharge membership, R0a discharges the antichain), but never argues it is *weakest* — no demonstration that dropping either conjunct admits a state falsifying the postcondition. A wp is the weakest such predicate; without the necessity half this is a sufficient-precondition claim wearing wp notation. Case 1 is also the trivial case (the operation's own preconditions); the persona's standard asks that wp analysis exhibit non-triviality, which only Case 2 does.

**Required**: Either add the one-line necessity argument for each conjunct (drop P1 ⇒ `a ∉ A_rel^{Σ'}` ⇒ intersection `≠ {a}`; drop P0 ⇒ Emit_R undefined), or relabel Case 1 as a sufficiency check and lean the wp framing on Case 2.

### Issue 7: Repeated deferral to "the self-targeting emission recipe (following R5)"
**ASN-0086**: the phrase "by the self-targeting emission recipe (following R5)" recurs in R5 Consequences (a)/(b)/(c) and the Nullify definition, each pointing at the standalone recipe paragraph that itself restates R5 Step 3's emission argument.

**Problem**: Multiple sites defer to one downstream paragraph, and that paragraph duplicates R5's own proof body. This is the "multiple paragraphs defer to the same downstream location" pattern compounded with a near-verbatim restatement of R5.

**Required**: Make the recipe a single named corollary of R5 (one sentence) and cite it; remove the duplicated emission walkthrough.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity of Emit vs Observe
The Open Questions ("Must Emit be atomic with respect to concurrent Observe…") correctly defer a consistency model. The substrate's `SequentialTransitionAxiom` (ASN-0093) already serializes transitions, so a concurrency model is new territory for a later ASN, not a gap here.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
Restricting `L_K` to standard triples and deferring higher-arity projections is a clean scoping decision; the higher-arity treatment belongs in a future note.

### Topic 3: Tightening L1b to `#E = 2` at the source
R0a-Cor2 establishes `#E = 2` for the realized link store; whether the *foundation* invariant L1b should be narrowed is a question about ASN-0043/ASN-0093, not a defect in this note.

VERDICT: REVISE
