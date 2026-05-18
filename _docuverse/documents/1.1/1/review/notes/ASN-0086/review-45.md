# Review of ASN-0086

## REVISE

### Issue 1: R7a's proof treats L12 + L12a as cross-references when they are load-bearing

**ASN-0086, R7a proof**: "The argument is directly from the Frame conditions on `→` (above)... L12 and L12a are consistency consequences of the same Frame, mentioned only for cross-reference."

**Problem**: R7a's claim quantifies over `↝` (categorical, "any-layer operations"), but the proof argues only from `→`'s frame conditions for classes (i), (ii), (iii). Both cases conclude with "No class (iv) exists, so both sub-cases are excluded" — but this is precisely what R7a is trying to establish. The proof is structurally circular: it argues that any non-class-(iii) Op cannot affect `Σ.L` because the *only* admissible classes are (i), (ii), (iii) — which is R7a itself. The frame conditions are definitional for each class but say nothing about what higher-layer operations admit. For the categorical scope to hold, the proof must invoke L12 + L12a (which forbid modification/removal across *all* layers as substrate invariants) as load-bearing.

**Required**: Reorder the argument: (1) L12 + L12a, as substrate-wide invariants, forbid any operation in any layer from modifying or removing existing `Σ.L` entries. (2) Any `↝`-step with `Σ.L ≠ Σ'.L` must therefore extend `dom(Σ.L)` by at least one fresh address. (3) The substrate model's structural commitment fixes class (iii) as the unique primitive that extends `dom(Σ.L)`. (4) Therefore the step is a class-(iii) `→`-step. Remove the demotion of L12+L12a to "cross-reference only."

### Issue 2: R0a-Cor1's worked-sketch verification is missing

**ASN-0086, Worked Sketch concrete instantiation**: "*Step 1 (concrete)*... *Step 2 (concrete)*... `A_K^{Σ_2} = {(a₂, F₁, G₁)}`."

**Problem**: The concrete instantiation traces a₁, b₁, a₂ through `dom(Σ_i.L)` and verifies invariants at each address individually, but never states or checks R0a-Cor1's contiguous-prefix claim (J_d^{Σ_2} = 2, occupied indices = {0, 1, 2}). R0a-Cor1 is the substantive new lemma supporting Emit_K's seed-independence — it should appear concretely in a sketch claiming to verify the substrate's behavior.

**Required**: Add one paragraph at the end of "Step 2 (concrete)" verifying R0a-Cor1: `{a' ∈ dom(Σ_2.L) : home(a') = d} = {inc⁰(d.0.s_L.1, 0), inc¹(d.0.s_L.1, 0), inc²(d.0.s_L.1, 0)} = {a₁, b₁, a₂}`, with `J_d^{Σ_2} = 2`. Similarly verify R0a-Cor2 (`#E = 2` at each of a₁, b₁, a₂).

### Issue 3: Verbose "T4-validity chain induction" sub-paragraph

**ASN-0086, R0 Step 2 Case A**: "*T4-validity chain induction.* *Base:* the seed `d.0.1 = inc(d, 2)` is T4-valid... *Step:* assume `d.0.k` is T4-valid for some `k ∈ {1, …, s_L − 1}`; the sibling step `d.0.(k+1) = inc(d.0.k, 0)` preserves T4-validity unconditionally by TA5a..."

**Problem**: This is a fairly trivial induction — TA5a (k=0) preserves T4 unconditionally — expanded into Base/Step paragraphs. The conclusion follows from one citation.

**Required**: Compress to one sentence: "By TA5a (k=0) applied along the sibling sweep d.0.1, ..., d.0.s_L, every intermediate is T4-valid, including d.0.s_L which feeds step (iii)'s spawn."

### Issue 4: Meta-prose "Terminology note on 'enumeration index' vs. 'last-component value'"

**ASN-0086, R0 Step 2 Case A**: "*Terminology note on 'enumeration index' vs. 'last-component value'.* T10a.7 (EnumerationInjectivity, ASN-0034) names an allocator's domain `{tₙ : n ≥ 0}` indexed from zero... 'enumeration index' is reserved for T10a.7's index-from-zero; sibling-sweep traversals and concrete tumbler digit values are stated as 'last-component value' to avoid the off-by-one ambiguity."

**Problem**: This is a terminology-disambiguation sub-paragraph expanded into a substantial block. The distinction can be stated as a single parenthetical at first use, or simply by writing the numerals consistently.

**Required**: Delete the sub-paragraph and use one phrasing consistently (likely "last-component value" since it matches the concrete tumblers in the worked sketch).

### Issue 5: Essay content "Witness, not material traversal"

**ASN-0086, R0 Step 2 Case A**: "*Witness, not material traversal.* The intermediate positions `d.0.1, d.0.2, …, d.0.s_L − 1` need not have been emitted into `dom(Σ.C)` or `dom(Σ.L)` for this sweep to be admissible... The Sparse-allocator hypothesis (above, Setup) licenses this reading directly..."

**Problem**: This restates the Sparse-allocator hypothesis's content in essay form. The hypothesis is established earlier; the chain-witness reading follows from it without restatement.

**Required**: Delete. The reference "by Sparse-allocator" suffices wherever the witness reading is invoked.

### Issue 6: Use-site inventory at R0a-Cor1's "Use" paragraph

**ASN-0086, R0a-Cor1**: "*Use.* R0a-Cor1 licenses the seed-independence argument in `Emit_K`'s Definition (below): under the discipline, Case B's choice of `b` ranges only over the contiguous prefix `{inc⁰, …, incᴶ_d^Σ}`, and the least-`i` selection lands the fresh emission at the *global* next index `J_d^Σ + 1` regardless of which `b` is chosen. The corollary is otherwise dormant — it is consumed exactly at the `Emit_K`-as-function argument."

**Problem**: Use-site inventory in the lemma's introduction. The work belongs at the seed-independence argument, not at the lemma's site. The phrase "otherwise dormant" is defensive.

**Required**: Delete the "Use" paragraph. The seed-independence argument in Emit_K's Definition already cites R0a-Cor1 directly.

### Issue 7: Defensive justifications in subspace-distinctness table entry

**ASN-0086, Properties Introduced table, "Subspace distinctness"**: "adopted as an explicit hypothesis of this note (parallel to the Setup hypothesis), motivated by ASN-0043's L0/L0a partition and L14's scoped disjointness (both collapse if `s_C = s_L`) but not formally axiomatized in the foundation ASNs. Consumed *directly* at R0 Step 4 (L14a and L14 preservation bullets), R4, and Nullify's no-content-address-under-`a` argument; *indirectly* at R5 (via Stage 1's appeal to R0's emission construction, which inherits the L14a-preservation step's use of the distinctness)"

**Problem**: A table entry expanded into a defensive justification with use-site inventory. The pattern repeats for other entries (Setup, R0, R7a).

**Required**: Compress to: "Subspace distinctness | HYP | `s_C ≠ s_L`. | introduced". The motivation belongs once in the hypothesis's introduction at Setup; the use-sites belong at use-site, not in the index.

### Issue 8: Essay content "Why this case is trivial-by-design"

**ASN-0086, wp analysis Case 3**: "*Why this case is trivial-by-design.* This trivial wp is the operational signature of R6b's single-depth retraction design: if `nullified(Σ')` instead recursed through the retraction relation (e.g., by quantifying over `A_R^{Σ'}`), the wp would have to add a conjunct ruling out the recursive un-retraction, breaking the trivial form. The Definition's quantifier-range choice (`L_R^Σ`, not `A_R^Σ`) is exactly what makes the second-order Nullify wp-trivial; relaxing that choice would impose substantial preconditions on the second-order operation."

**Problem**: Restates R6b in essay form within the wp analysis. R6b already establishes this; the wp computation can cite R6b without re-explanation.

**Required**: Replace with one sentence: "The trivial wp form is the operational signature of R6b's quantifier-range choice." Delete the rest.

### Issue 9: Definitions enumerating downstream consumers

**ASN-0086, Convention — RetractionDirectionality**: "*[Substrate-level convention; consumed by Definition of Nullified.]* For the retraction coverage class `[R]`, the to-set carries the retraction's targets..."

**Problem**: The bracketed tag "[Substrate-level convention; consumed by Definition of Nullified.]" enumerates a downstream consumer at the convention's introduction. Same pattern at "Definition — Nullified" with its "*[Inherits Convention — RetractionDirectionality.]*" tag.

**Required**: Delete the bracketed consumer tags. The convention's content stands on its own; downstream sites cite it where they use it.

### Issue 10: Multiple paragraphs deferring to the same downstream location

**ASN-0086, Setup section**: "*Discipline-conditional claims.* R0a, R0a-Cor1, R0a-Cor2, and Nullify's single-tuple-scope guarantee are conditional on the sibling-frontier discipline. The Emit_K *A_K^{Σ'} membership* note and the wp computation for Emit_K's membership in `A_K^{Σ'}` are also conditional on the unit-depth retraction discipline. Downstream sites reference these disciplines by name; the conditionalities are stated once here."

**Problem**: The conditionality table is fine as a single reference, but the same conditionalities are repeated at R0a's introduction (extensive opening prose), R0a-Cor1's introduction, R0a-Cor2's introduction, Nullify's "single-tuple scope" sub-paragraph, and Emit_K's "A_K^{Σ'} membership" paragraph. The "stated once here" promise is not kept.

**Required**: At each downstream site, replace the conditionality restatement with a short citation: "(conditional per Setup *Discipline-conditional claims*)". The full statement appears only at Setup.

### Issue 11: R6c's induction step phrased ambiguously

**ASN-0086, R6c proof**: "*Step*: R6a propagates `a ∈ nullified` across `Σ_k → Σ_{k+1}`, and R3 propagates `(a, F, G) ∈ L_K`. By Definition of `A_K`, `(a, F, G) ∈ L_K^{Σ'} ∧ a ∈ nullified(Σ') ⟹ (a, F, G) ∉ A_K^{Σ'}`."

**Problem**: The Step paragraph mixes per-step propagation ("across `Σ_k → Σ_{k+1}`") with the endpoint conclusion ("at `Σ'`"). A reader has to infer that the induction hypothesis carries `(a, F, G) ∈ L_K^{Σ_k}` and `a ∈ nullified(Σ_k)` forward, and the conclusion at `Σ'` is the case `k = n`.

**Required**: Restate: "IH at Σ_k: `(a, F, G) ∈ L_K^{Σ_k}` and `a ∈ nullified(Σ_k)`. Step: R6a gives `a ∈ nullified(Σ_{k+1})`; R3 gives `(a, F, G) ∈ L_K^{Σ_{k+1}}`. Conclusion at Σ_n = Σ': by Definition of A_K, `(a, F, G) ∉ A_K^{Σ'}`."

### Issue 12: SharedDepthOneAllocator's "lemma" status is decorative

**ASN-0086, Setup section**: "*Lemma — SharedDepthOneAllocator.* Under each document address `d ∈ dom(Σ.M)`, there exists exactly one allocator at allocator-tree depth 1 below `d` whose outputs sit at zero-count depth 1 relative to `d`..."

**Problem**: The lemma is labeled "Lemma" but is in fact a direct three-step consequence of T10a's at-most-once axiom plus TA5(d). Its statement is also tightly wound to a worked-sketch terminology distinction ("allocator-tree depth" vs. "zero-count depth") introduced in the same section. The "depth-2 subspace-specific allocators... are mutually independent" final clause is asserted but not proved within the three steps.

**Required**: Either prove the "mutually independent" clause as Step (d) (T10a imposes no joint constraint on `(d.0.s_C, 1)` and `(d.0.s_L, 1)` since the parent tumblers are distinct), or compress to a Definition naming `A_{d.0.1}` and `A_{d.0.s_L.1}` with the SharedDepthOne identification as a parenthetical citation of T10a's at-most-once.

## OUT_OF_SCOPE

### Topic 1: Multi-arity active subsets

**Why out of scope**: The note restricts `L_K^Σ` to standard-triple links (arity 3) and explicitly defers `L_K^{(n),Σ}` for `n > 3` to the Open Questions. Extending active-subset machinery to arbitrary arity would be a separate ASN.

### Topic 2: Substrate-level guarantee of sibling-frontier discipline

**Why out of scope**: The note's Open Questions raise whether to elevate the sibling-frontier discipline to a substrate-level guarantee (e.g., by tightening Emit_K's specification or the substrate emission primitive). Either tightening would change the substrate model itself, properly belonging in a revision of ASN-0043 or a new substrate-amendment ASN.

### Topic 3: Native scoped form of L14 without globally-s_C-resident-content Setup

**Why out of scope**: The Setup hypothesis globally restricts content to s_C-resident addresses. Dropping this and reformulating R0, R4, R5 slice-wise (with explicit auxiliary preservation arguments at the slice boundary) is a non-trivial refactor properly explored in a separate ASN.

### Topic 4: Concurrency semantics for Emit vs. Observe

**Why out of scope**: Emit/Observe atomicity, ordering guarantees on Observe results, and consistency models for concurrent operations are runtime/concurrency questions outside the abstract substrate model. The Open Questions correctly defer these.

VERDICT: REVISE
