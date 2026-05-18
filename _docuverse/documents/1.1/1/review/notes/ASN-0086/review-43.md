# Review of ASN-0086

## REVISE

### Issue 1: wp Case 1 contains an extraneous conjunct
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a) ∧ P2(Σ, a) ∧ P3(Σ, a) ∧ SFD(Σ) ∧ NoCraftedSpanReachesFreshEmitter(Σ, d_retr)`"
**Problem**: The stated postcondition `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` is purely set-theoretic. It requires: (1) `a ∈ A_rel^{Σ'}` (via P1 + L12a), (2) no `a' ∈ A_rel^Σ` with `a ≼ a' ∧ a' ≠ a` (via P3), (3) `a ⊀ b` for the fresh emitter (via SFD/R0a). `NoCraftedSpanReachesFreshEmitter` concerns whether `b ∉ nullified(Σ')` — the retractor's active status — which is a separate property of `A_R^{Σ'}`, not of single-tuple scope as defined in Nullify's Definition.
**Required**: Either remove the extraneous conjunct, or explicitly augment the postcondition to include "the new retraction tuple at `b` is operationally active (`b ∈ A_R^{Σ'}`)" and label the augmentation.

### Issue 2: Notation `↝` in R7a is not formally defined
**ASN-0086, R7a — NoExtraClassAffectsL**: "for any state-affecting transition `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L`, that transition is a class-(iii) `→`-step"
**Problem**: The note defines `→` and `↦` (and their reflexive-transitive closures `⊑` and `⊑̂`), but uses `↝` for "any state-affecting transition" without formal definition. The claim's universal quantifier range — "any-layer operations" — is informally indicated but not pinned down.
**Required**: Either define `↝` formally (the union of all admissible state-transition relations across any layer), or restate R7a with the universal quantifier given over a defined set of operations.

### Issue 3: The "Allocator-state commitment" should be axiomatized, not buried in a remark
**ASN-0086, R0 Step 2 Case A**: "*Allocator-state commitment (load-bearing for R0 Step 2 Case A).* The atomic class-(iii) step implicitly discharges T10a's child-spawn admissibility at each intermediate spawn pair on the L1c witness chain in one indivisible action; allocator state has no observable evolution apart from the emissions whose witness chains it supports. This is a load-bearing design commitment of the substrate model..."
**Problem**: The commitment is self-described as "load-bearing" for R0 Step 2 Case A's argument that the sibling sweep through `A_{d.0.1}` from position 1 to position `s_L` is "witness, not material traversal." Without it, Case A's chain would require per-position deposits at intermediate sibling positions. This is a stronger structural commitment than T10a alone (which constrains child-spawn pairs to at-most-once but is silent on whether sibling-stream enumeration requires materialized intermediate deposits).
**Required**: Lift this commitment to an explicit axiom/hypothesis in the Setup section, parallel to the Setup hypothesis and subspace-distinctness hypothesis. Name it (e.g., "Sparse-allocator hypothesis") and identify each downstream proof that consumes it.

### Issue 4: Rationale subparagraphs justifying design choices that don't advance claims
**ASN-0086, Emit_K Definition, "Why `d` is a caller parameter, not a substrate-internal choice"**: Two subparagraphs labeled *Design-level (the link model)* and *Implementation-level (the udanax-green code path)* explain why the signature exposes `d`.
**ASN-0086, Nullify Definition, "Why `d_retr` is a caller parameter, not `home(a)`"**: Same pattern with *Design-level (Nelson's link model)* and *Symmetry with `Emit_K`* subparagraphs.
**ASN-0086, Emit_K Definition, "Why the construction is bound into the definition"**: Explains why `Emit_K` is bound to the disciplined subset of the substrate primitive.
**Problem**: These subparagraphs explain *why* signature/definition choices were made. The signature already shows `d ∈ dom(Σ.M)` as a parameter; the design rationale is meta-prose that doesn't advance the operation's contract. The "anti-bloat" classifier explicitly flags this pattern.
**Required**: Consolidate into a single brief design-rationale paragraph (or footnote), or remove. Reserve operation-definition prose for stating preconditions, effects, frames, and postconditions.

### Issue 5: Repeated restatements of discipline-conditionality
**ASN-0086, multiple sections**: The sibling-frontier discipline's conditional nature is restated in R0a, R0a-Cor1, R0a-Cor2, Emit_K's Definition (multiple paragraphs including "Why the construction is bound" and "Scope of `Emit_K`'s contract"), Nullify's Definition (multiple paragraphs), Definition of `Emit_K`'s `A_K^{Σ'}` membership note (regime (i)/(ii) distinction), R6c Consequence (e), the wp analysis (Cases 1, 2, 3), the Properties table, and the Open Questions.
**Problem**: The discipline's effect ("under SFD, X holds; without SFD, X fails or requires extra conjuncts") is repeated structurally across these locations rather than referred back to a canonical statement. This compounds across cycles per the anti-bloat classifier.
**Required**: State the discipline once (in the Setup section) with its full effect, then cite the canonical statement from subsequent claims. Subsequent claims should reference "(discipline-conditional per Sibling-Frontier definition)" rather than re-explain.

### Issue 6: Defensive prose anticipating misuse
**ASN-0086, Emit_K Definition, "Scope of `Emit_K`'s contract — substrate-primitive bypass is outside it"**: "Callers that bypass the discipline by invoking the substrate emission primitive directly at a prefix-extension of an existing link address have *not* invoked `Emit_K` and are not covered by R0a or its corollaries..."
**Problem**: This paragraph anticipates caller misuse and disclaims responsibility rather than advancing `Emit_K`'s definition. The operation's signature and discipline-binding already specify what `Emit_K` *is*; documenting what it isn't is unnecessary.
**Required**: Remove. The operation's positive specification suffices.

### Issue 7: "Operational scope of the `A_rel^Σ` filter" paragraph is verbose
**ASN-0086, Definition of Nullified**: An eight-line paragraph discusses what happens for retractions whose `coverage(G')` lies outside `A_rel^Σ ∩ {a : |Σ.L(a)| = 3}` — covering content addresses, ghost tumblers, higher-arity links. It distinguishes "syntactic admissibility" from "operational effect" and forward-references the higher-arity open question.
**Problem**: The paragraph addresses a real subtlety but at considerable length. It also overlaps content addressed in the higher-arity Open Question and at Nullify's "Crafted-span retractions" paragraph.
**Required**: Condense to two sentences: (a) the `A_rel^Σ` filter scopes `nullified(Σ)` to relational addresses, (b) retractions with crafted spans covering non-relational tumblers are well-formed but operationally inert for `A_K`. Move higher-arity discussion to its dedicated Open Question.

### Issue 8: R6c Consequence (e) regime-(ii) strengthening is mislabeled and redundant
**ASN-0086, R6c Consequences (e)**: "*Regime-(ii) strengthening (retraction-discipline-conditional).* Under the unit-depth retraction discipline (regime (i)), the non-monotonicity of `A_K` requires a *retraction step* between `Σ` and `Σ'`..."
**Problem**: The "Regime-(ii) strengthening" label is confusing — the prose actually distinguishes regime (i) from regime (ii) and observes that under regime (ii), `A_K` can fail to grow even on non-retraction class-(iii) steps. This restates content already covered in Emit_K's *A_K^{Σ'} membership* note and R0a-Cor2's discussion.
**Required**: Either remove (the regime distinction is already established in Emit_K) or rename to clarify (e.g., "Regime dependence of A_K growth").

### Issue 9: "Allocator-naming convention" is introduced inline but used inconsistently
**ASN-0086, Setup**: "*Allocator-naming convention.* Throughout this note, `A_x` denotes the allocator whose *first emission* is `x`."
**Problem**: The convention is helpful, but inconsistently applied: the Worked Sketch uses `A_{d.0.s_L.1}` (the depth-2 link allocator under `d`) and `A_{a₁}` (= `A_{d.0.2.1}`) as if they were distinct names, when they refer to the same allocator. Similarly `A_{d.0.1}` is described as the depth-1 allocator under `d` but its first emission is `d.0.1`. The convention works, but the substitutions across sections make it harder than it needs to be to track allocator identity.
**Required**: Pick one form per allocator (e.g., always `A_{first_emission}`) and use consistently. Acknowledge equivalences once (e.g., "`A_{a₁} = A_{d.0.s_L.1} = A_{d.0.2.1}` — all three names refer to the depth-2 link allocator with base `a₁`"), then use one form.

### Issue 10: Two-paragraph "Why the construction is bound into the definition" overlaps "Scope of Emit_K's contract"
**ASN-0086, Emit_K Definition**: Two adjacent paragraphs ("Scope of `Emit_K`'s contract — substrate-primitive bypass is outside it" and "Why the construction is bound into the definition") both argue that `Emit_K` is the disciplined subset and that bypassing it loses guarantees.
**Problem**: Same point made twice in adjacent paragraphs, in slightly different terms. The first frames it from the caller-misuse angle; the second from the binding-rationale angle.
**Required**: Merge into one statement, or remove one. The binding is captured by the operation's signature with its address-construction postcondition; further justification is supportive at best.

## OUT_OF_SCOPE

### Topic 1: Arrangement-`L_K` interaction invariants
**Why out of scope**: The first Open Question asks what invariants must hold between `L_K` and arrangements `Σ.M` when relational predicates depend on visibility. This is genuinely future-ASN territory — the present ASN scopes its claims to `Σ.L`-derived properties.

### Topic 2: Multi-arity active subsets (`A_K^{(n)}`)
**Why out of scope**: The note explicitly restricts to standard-triple (arity-3) links and acknowledges the multi-arity extension as future work. Higher-arity active-subset machinery would require its own definitional and proof apparatus.

### Topic 3: Slice-wise R0/R4/R5 without globally `s_C`-resident Setup
**Why out of scope**: The Open Question identifies how each substrate-level R-claim would restate under L14's native scoped form. The present ASN adopts the Setup hypothesis precisely to avoid this slicing; lifting it is a separate development.

### Topic 4: Discipline elevation, deeper-sited links, Observe ordering, atomicity, cardinality bounds, dynamic type extension
**Why out of scope**: Each of these is a properly-scoped Open Question — they identify directions for follow-on work without claiming the present ASN should resolve them.

VERDICT: REVISE
