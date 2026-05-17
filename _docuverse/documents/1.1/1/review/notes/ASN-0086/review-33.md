# Review of ASN-0086

## REVISE

### Issue 1: Hypothesis tagging conflates Setup with Subspace-distinctness

**ASN-0086, Section header on R0**: `*[Setup-required: the L14a-preservation step in Step 4 uses ran(Σ.M) ⊆ s_C-resident content, derived from S3 + Setup.]*`

**Problem**: R0 Step 4 uses *two* hypotheses at distinct bullets. The L14a-preservation bullet uses Setup (via S3). The L14-preservation bullet uses the Subspace-distinctness axiom `s_C ≠ s_L` ("By the subspace-distinctness axiom (`s_C ≠ s_L`) and T3..."). The tag mentions only Setup. The Hypothesis dependency view table likewise has columns "(a) Direct Setup dep" and "(b) Direct discipline dep" but no column for Subspace-distinctness, even though the latter is introduced as a separate explicit hypothesis ("We additionally assume that the content and link subspace identifiers are distinct first-element-field values: `s_C ≠ s_L`").

**Required**: Either (a) extend tagging and the dependency table to distinguish all three hypotheses (Setup, Subspace-distinctness, discipline), or (b) state explicitly in the Setup section that `[Setup-required]` is a shorthand covering both Setup *and* Subspace-distinctness as a bundled hypothesis pair. The current tagging propagates incompletely: R5 inherits Setup via R0, but its Stage 2 L14 check would also pick up Subspace-distinctness — not currently reflected.

### Issue 2: R6c's chain application of R3 elides transitivity

**ASN-0086, R6c proof**: "By R3 (TypedSliceMonotonicity) applied along the inductive chain `Σ = Σ_0 → Σ_1 → … → Σ_n = Σ'`, `(a, F, G) ∈ L_K^Σ ⊆ L_K^{Σ'}`"

**Problem**: R3 is a single-step lemma (`Σ → Σ'`). The chained conclusion requires induction on chain length plus transitivity of `⊆`. The proof above does explicit induction for `a ∈ nullified(Σ')` (using R6a) but jumps directly to the chained `L_K^Σ ⊆ L_K^{Σ'}` without naming the induction. This is trivial — transitivity of `⊆` is unambiguous — but inconsistent with the level of explicitness used in the immediately preceding paragraph.

**Required**: One-sentence inductive statement parallel to the `nullified` induction, or an inline note "by R3 at each step and transitivity of `⊆`".

### Issue 3: Sibling-frontier discipline not formally labeled as DEF

**ASN-0086, Setup section**: "**Implementation discipline — sibling-frontier link emission.** The *sibling-frontier discipline* on `→` requires that every class-(iii) transition (every Emit_K) deposits the fresh link address..."

**Problem**: The discipline is heavily cited downstream (R0a's hypothesis, Nullify's single-tuple-scope, R7b's commitment, Appendix B's failure modes) but is introduced as bold prose rather than a labeled DEF. The Properties Introduced table lists it under "DEF" but the source paragraph isn't formally labeled.

**Required**: Promote the discipline to a labeled definition (parallel to the labeled "Lemma — FramePreservation" and "Lemma — SharedDepthOneAllocator" patterns used elsewhere) so downstream citations have an unambiguous anchor.

### Issue 4: R0a's proof structure interleaves induction and corollary

**ASN-0086, R0a proof**: The proof block contains three logically distinct pieces — (a) statement of the strengthened sibling-stream invariant, (b) the antichain corollary derivation (with same-home and Case 2 sub-cases), (c) the induction on `→`-chain length proving the strengthened invariant — but presents them in the order (a) → (b) → (c), with Case 2 of the corollary derived at the end *after* the induction. A reader following sequentially encounters the corollary's reliance on the invariant before the invariant has been established.

**Problem**: Logical dependence is induction → corollary, but presentation order is corollary first. Case 2 is genuinely independent of the discipline-conditional induction, so it could stand earlier as its own piece. The current structure obscures which part of R0a's proof carries the discipline-conditionality versus which is unconditional.

**Required**: Restructure as (i) Case 2 sub-argument (unconditional, just zero-count + L1), (ii) sibling-stream invariant induction (discipline-conditional), (iii) antichain corollary composing the two. Alternatively, explicitly flag at the corollary's same-home case that the invariant is yet to be proved, and forward-reference the induction.

### Issue 5: FramePreservation's specialization (e) lacks a precise predicate-form check

**ASN-0086, FramePreservation lemma, specialization (e)**: "scope-orthogonality to endset content under any frame... whenever `P`'s free variables draw from substrate components disjoint from the endset values of `Σ.L` — i.e., `P` is a predicate over `(Σ.C, Σ.M, dom(Σ.L))` together with the tumbler algebra and the `→`-admissibility relation (both state-independent in the relevant sense — T1 and T3 fix the tumbler algebra as a fixed pre-state structure, and `→`-admissibility is witnessed by L1c chains under the foundation ASNs)..."

**Problem**: The justification "both state-independent in the relevant sense" handles the tumbler algebra cleanly via T1/T3, but `→`-admissibility is *not* state-independent — whether a fresh `a` is `→`-admissible at Σ depends on `dom(Σ.L)` (must be fresh) and on the L1c chain witness, which itself depends on prior allocator history. The lemma should make the dependence on `dom(Σ.L)` explicit (which is in the predicate's allowed free-variable set), and clarify that the L1c witness chain is an *existential predicate* over `(Σ.C, Σ.M, dom(Σ.L))` plus the tumbler algebra — so admissibility is state-dependent in `dom(Σ.L)` but not in the *values* of `Σ.L`. The parenthetical leans toward suggesting it's state-independent, which is misleading.

**Required**: Rephrase to make explicit that `→`-admissibility's state-dependence is on `dom(Σ.L)` only (and on `dom(Σ.M)`), not on `Σ.L`'s pointwise values; specialization (e) then permits `P` to consult `dom(Σ.L)` but not the endset values stored at those addresses.

### Issue 6: Step 5.2's abstraction acknowledged but not fully justified

**ASN-0086, Worked Sketch Step 5.2**: "*This sub-step is structurally abstract by necessity, in contrast to the concrete tumbler-level instantiation of Steps 1–4.* The asymmetry is intrinsic to ASN-0086's scope..."

**Problem**: The justification for the abstraction is sound (ASN-0086 doesn't own arrangement-modifying transitions) but the worked sketch concludes by computing `Σ_5.L = Σ_4.L`, `nullified(Σ_5) = nullified(Σ_4)`, `A_K^{Σ_5} = A_K^{Σ_4}` via FramePreservation substitution. This trivial-substitution argument is the entire content; the lengthy meta-discussion about why the step is abstract obscures the fact that the *actual mathematical work* is one substitution. A reader could reasonably ask: if every arrangement-modifying step gives `A_K` pointwise-identical to before, what does Step 5.2 add to Steps 1–4 beyond R6c-Corollary's already-stated content?

**Required**: Either (a) trim the meta-discussion and present the substitution chain as one sentence (R6c-Corollary already establishes the pointwise preservation; Step 5.2's role is to verify a specific instantiation), or (b) actually exhibit a concrete arrangement-modifying transition (perhaps by populating `Σ.M(d)` at an earlier sketch step and applying an explicit pointwise update from a forthcoming ASN-0036-extending operation). The current intermediate state — abstract claim with full ceremony — gives neither the cleanness of (a) nor the rigor of (b).

### Issue 7: Emit_K's A_K membership analysis depends on retraction discipline not made operational

**ASN-0086, Emit_K Definition, regime (ii)**: "*Crafted-span retractions admitted.* The substrate primitive does not preclude callers from emitting retractions with broader-coverage to-spans — e.g., a subtree-broad retraction `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})` whose coverage is `{t : d ≼ t}`, which intersected with `A_rel^Σ` covers every link sited under `d` (and propagates to every link subsequently emitted under `d`, since R3 preserves the retraction tuple)."

**Problem**: This regime is named but its discipline-level implication isn't tracked in the hypothesis table. Specifically: under regime (ii), `Emit_K(d, F, G)` can produce a fresh `a` with `a ∈ nullified(Σ')` *immediately upon emission*, so `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}`. Consequence R6c(e) says `A_K` is non-monotone, but the regime-(ii) case adds a stronger form: `A_K` may *fail to grow* even when L_K does. This affects what an Observe over A_K can be expected to return. The Worked Sketch operates under regime (i) implicitly (every retraction has a unit-depth to-span); regime (ii) is acknowledged as admissible but its consequences aren't traced.

**Required**: Either flag regime (ii) as a discipline that callers may adopt (parallel to the sibling-frontier discipline), with explicit notes on which R-claims and consequences hold only under regime (i); or add a brief consequence note in R3/R6c about regime (ii)'s effect on Emit_K's relationship to A_K.

### Issue 8: SharedDepthOneAllocator's "extending d's rightmost element-field" terminology

**ASN-0086, SharedDepthOneAllocator lemma, step (b)**: "By TA5 (HierarchicalIncrement, ASN-0034), postcondition (d), `(d, 1)` yields a child with `zeros = 2 + (1 - 1) = 2` — no new zero is introduced, and the resulting tumbler `inc(d, 1)` stays at element-field depth 0 relative to `d` (it extends `d`'s rightmost element-field rather than opening a new one)."

**Problem**: "Element-field" is used in two distinct senses in the ASN: (1) the T4 E-field specifically (last of four fields N/U/D/E), and (2) any field delimited by zeros. Here the lemma is concerned with sense (2), since `d` (with `zeros(d) = 2`) has *three* fields (N, U, D) and no E-field — so "rightmost element-field" must mean D, not E. The terminology overloading risks reader confusion, especially since T4b explicitly names the four projections N/U/D/E.

**Required**: Clarify the term — either use "rightmost field" generically, or specify "rightmost field (which is D for a document-level tumbler)". This is purely terminological but recurs at several sites.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link active subsets

The note restricts to standard-triple links (`|Σ.L(a)| = 3`) and defers `A_K^{(n)}` machinery for higher-arity links to the Open Questions section. The deferral is appropriate — extending active-subset semantics to multi-arity relations requires choices about which slot(s) the retraction can target and how slot-typed projections compose.

**Why out of scope**: This is genuinely a future ASN's territory. ASN-0086's claims about standard triples are self-contained; the multi-arity extension would require its own structural commitments.

### Topic 2: Discipline relaxation for deeper-sited links

R0a-Cor2 narrows L1b's `#E ≥ 2` to `#E = 2` strictly, matching udanax-green but narrower than Nelson's foundational design. Relaxing to admit `#E ≥ 3` (recursive sub-links) would require restructuring R0a's sibling-stream invariant over a tree of allocators.

**Why out of scope**: The note flags this as future work and identifies the necessary structural reformulation. The narrowing to `#E = 2` is consistent with the rest of ASN-0086's claims; admitting deeper links is a separate model commitment.

### Topic 3: ASN-0036 transition closure for arrangement-modifying steps

R6c-Corollary depends on the arrangement-modification frame being inherited from ASN-0036. The note states this frame as a definitional inheritance but doesn't re-verify which ASN-0036 (or editing-operation ASN) is the source.

**Why out of scope**: Arrangement-modifying transitions are owned by ASN-0036 and its extensions; ASN-0086 correctly cites them as foundation material rather than re-proving their frame conditions.

VERDICT: REVISE
