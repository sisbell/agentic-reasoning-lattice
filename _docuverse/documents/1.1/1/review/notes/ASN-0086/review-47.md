# Review of ASN-0086

## REVISE

### Issue 1: Properties Introduced table — case labels contradict proof structure

**ASN-0086, Properties Introduced table, R0a row**: "(Case 1 = R0 Step 2 + T10a.1 + T10a.2 + T10a.7 + T10a.8 from ASN-0034; Case 2 = L1 (LinkElementLevel) + L1a (LinkScopedAllocation) from ASN-0043 + zero-count additivity along prefix-extension; ...)"

**Problem**: The proof of R0a is structured as Stage 1 (cross-home, unconditional, uses L1 + L1a + zero-count additivity), Stage 2 (same-home, discipline-conditional, uses R0 Step 2 + T10a primitives), Stage 3 (composition). The table's "Case 1" maps to the proof's Stage 2 and "Case 2" maps to Stage 1 — the numbering is inverted, and the "Case" terminology doesn't appear in the proof at all. A reader cross-referencing table to proof will mismap dependencies.

**Required**: Align labels — either rename table to "Stage 1 (cross-home) = ...; Stage 2 (same-home) = ...", or rename proof stages to "Case 1 / Case 2".

### Issue 2: R7a's scope over ↝ is unclear for composite transitions

**ASN-0086, R7a statement**: "for any state-affecting transition `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L`, that transition is a class-(iii) `→`-step at the substrate level."

**Problem**: ↝ is defined to include "every state-transition relation any higher-layer operation may admit". Such relations could include composite transitions that simultaneously extend Σ.L AND Σ.M (or Σ.C). Class (iii)'s Frame explicitly requires Σ'.C = Σ.C and Σ'.M = Σ.M; therefore a composite ↝-step affecting both Σ.L and Σ.M cannot itself "be a class-(iii) step" — its Σ.L-affecting component matches class (iii), but the step as a whole does not. The proof's conclusion ("the step is therefore a class-(iii) → step") is too strong. The downstream Relational Layer Corollary depends on R7a holding for any-layer composites, so this matters.

**Required**: Either (a) restrict R7a to *primitive* ↝-steps (those whose Frame holds Σ.C and Σ.M identical), or (b) reword as "the Σ.L-affecting component of any state-affecting ↝-step decomposes into a class-(iii) → step", and adjust the Relational Layer Corollary's invocation accordingly.

### Issue 3: Subspace-distinctness — "hypothesis" vs "axiom" naming drift

**ASN-0086, multiple sites**: Setup calls it "**Subspace-distinctness hypothesis**". The Properties Introduced table lists it as HYP. But R4's "Remark on the underlying structural mechanism" says "the subspace-distinctness axiom"; Nullify's "Why no content address lies under `a`" says "contradicting the subspace-distinctness axiom"; R0 Step 4's L14/L14a paragraph cites "the subspace-distinctness hypothesis".

**Problem**: Same artifact is named both ways in the same note. Pick one.

**Required**: Use "subspace-distinctness hypothesis" throughout (matching the Setup framing and HYP type — it isn't entailed by foundation ASNs; this note adopts it).

### Issue 4: Meta-prose accumulation (anti-bloat classifier)

The note carries `review-mode.anti-bloat`. Multiple paragraphs occupy structural slots without advancing reasoning:

- **R0a proof, opening paragraph**: "Direct induction on the antichain conclusion does not go through: the inductive step that adds a fresh link sharing a home document with an existing link must invoke T10a.2..." — explains *why* the proof has three stages before giving the proof. Reframe as a single-line note or drop.

- **R0a-Cor1 proof, setup paragraph**: "By induction on the `→_D`-chain length ... parallel to R0a's induction. Class-(iii) `→`-steps that *fail* the discipline are outside `→_D` and so outside the chains over which the induction ranges; the Sub-case B argument below explicitly invokes R0a's invariant ... The IH below carries the contiguous-prefix property — that the set of occupied indices forms `{0, 1, …, J_d^Σ}` with no skipped indices — which licenses Sub-case B's bound on `k` and its identification of `i = J_{d_new}^Σ - k + 1`; this strengthens R0a's `⊆` direction (every homed link lies at some `incʲ`) with the `⊇` direction." — entirely meta. The contents either reappear in the proof body or restate the lemma statement.

- **R6b's second paragraph**: "R6b is logical-depth-within-state, distinct from R6a's temporal persistence across state transitions: even at a single fixed state, R6b already determines `nullified(Σ)`'s value, while R6a is vacuous. The wp computation in Case 3 ... exhibits the operational consequence ..." — forward-references the wp section while restating R6b's content. Forward-reference accretion pattern.

- **Weakest-Precondition Analysis, Summary paragraph**: "The three wp computations expose the discipline-conditional structure of `Nullify` and `Emit_K`'s postconditions explicitly..." — recap of the three cases just presented. Drop entirely.

- **Setup section, "conceptual contribution" paragraph**: "The conceptual contribution sits in the *active/audit distinction* itself: two coherent views (`L_K`, the audit trail; `A_K`, the operational currently-in-effect set), co-exist over the same link store, with retractions cleanly mediating between them. The substantive properties carrying that distinction are R6a (RetractionStability — nullification persists across state transitions), R6b (SingleDepthRetraction — the predicate does not recurse), and R6c (RestorationByReemission — once retracted, always out of every future active subset). Their joint content is the substrate's own contribution: a self-referential retraction relation (made possible by R5) computed against a monotone audit trail (R3), yielding a usable active subset that ASN-0043's link model alone does not articulate." — defensive justification of "what this note contributes". This is essay content in an opening slot, and it inventories downstream consumers (R3, R5, R6a/b/c) by name. Drop or compress.

- **R7a proof, third paragraph**: "The claim is about the *net effect* on Σ.L, not about the implementing layer's invocation of the primitive: a higher-layer operation that bypassed class (iii) internally but happened to leave Σ.L extended would still be an `↝`-step..." — defensive justification for the argument's exhaustion structure.

- **Definition of relational layer, Corollary paragraph**: "by R7a + the commitment, every relational-layer-initiated class-(iii) step is an `Emit_K` call. The relational layer's state-affecting operations therefore reduce to `{Emit_K}` (with `Nullify` as alias). 'Update' and 'mutate' do not exist at the relational layer as committed; the substrate itself admits broader class-(iii) emissions outside the commitment's scope." — restates the commitment then re-justifies it.

- **Implementation hypotheses, "Discipline-conditional claims" note**: "Downstream sites reference these disciplines by name; the conditionalities are stated once here." — and yet R0a, R0a-Cor1, R0a-Cor2, Nullify, Emit_K membership, and the wp computations each repeat the conditionality phrasing at their site. Either the central note is sufficient and the per-site repeats can drop, or the per-site phrasings are sufficient and the central note can drop. Both is the bloat pattern.

**Required**: Trim. The structural content of each numbered claim and operation is sound; the prose around it has accumulated across cycles.

### Issue 5: R5 Stage 2 closes by sweeping claim rather than enumeration

**ASN-0086, R5 Stage 2**: "L4(c) ... explicitly permits link-subspace targets in endset spans; no other L-invariant constrains endset target content — each L-invariant's free variables either name the link address, the arity, or the from/to/type *positions* rather than what those positions cover."

**Problem**: The note's other invariant-discharge arguments (R0 Step 4, the worked sketch) enumerate L-invariants explicitly. R5's Stage 2 makes a sweeping claim about "each L-invariant" without listing them. A reader checking soundness has to enumerate independently. The claim does check out under enumeration (L0/L1/L1a/L1b/L1c name the link's structural properties; L2/L11a-b/L12-12b are state-evolution; L4(a)(b) explicitly permit cross-document/intra-document spans; L13 supports R5; L14/L14a are subspace-level), but the prose hands the burden to the reader rather than doing the check.

**Required**: Either enumerate the invariants and pair each with "constrains structure, not endset content" (matching R0 Step 4's style), or accept the sweep and note explicitly which L-invariants would *potentially* constrain endset target content (none, by enumeration).

### Issue 6: Sparse-allocator hypothesis is conditioning R0 without entering Discipline-conditional accounting

**ASN-0086, Setup *Implementation hypotheses***: Lists three hypotheses (Sparse-allocator, Sibling-frontier discipline, Unit-depth retraction discipline) but the "Discipline-conditional claims" subnote covers only the latter two. R0's proof explicitly invokes the Sparse-allocator hypothesis at Step 2.

**Problem**: R0 is therefore Sparse-allocator-conditional. Since R0 underlies R0a, R5, Emit_K, and Nullify, all of these are also Sparse-allocator-conditional in the same sense the latter two disciplines condition specific claims. The note's framing treats Sparse-allocator as an interpretive substrate assumption rather than a per-claim conditionality, but doesn't make that distinction explicit.

**Required**: Either (a) state in *Discipline-conditional claims* that Sparse-allocator is a substrate-level interpretation underlying every R-claim (and so is not separately tracked), or (b) add R0 (and downstream) to the conditionality list with Sparse-allocator named as the conditioner. Currently the note is silent at the meta-level.

### Issue 7: Two parallel passes through the Worked Sketch

**ASN-0086, Worked Sketch**: Steps 1 and 2 are presented schematically (general F₁, G₁, a₁, b₁), then the *Concrete instantiation* subsection re-runs the same Steps 1 and 2 with specific tumbler values (a₁ = 1.0.1.0.1.0.2.1, etc.).

**Problem**: Two parallel passes is more than needed for the verification purpose. The concrete pass is the one that verifies postconditions against actual values; the schematic pass restates R0/Nullify's contracts in narrative form. If R0a-Cor1 and Cor2 verification at Σ_2 is the goal, the concrete pass already covers it.

**Required**: Compress to one pass — either drop the schematic Steps 1/2 (the concrete instantiation is self-explanatory once K, R, d, c₁, c₂ are fixed) or drop the concrete instantiation (the schematic suffices if Cor1/Cor2 verification is moved earlier). The current dual structure duplicates work without adding verification depth.

### Issue 8: R7a's exhaustion argument depends on a structural commitment that should be named

**ASN-0086, R7a proof**: "the substrate model exposes no fourth class — the commitment is structural at the abstract-substrate level — so any `↝`-step that strictly extends `dom(Σ.L)` must produce a Σ' identical in effect to some class-(iii) step at Σ."

**Problem**: "the substrate model exposes no fourth class" is the load-bearing premise. It is not derived from L12 + L12a (which forbid modification/removal but say nothing about how many extension classes the substrate admits). It comes from the Setup's Frame-conditions paragraph, which commits classes (i)/(ii)/(iii) as definitional. This commitment should be named at R7a's proof site so a reader can see whether the substrate model could in principle admit a fourth class.

**Required**: Replace "the substrate model exposes no fourth class — the commitment is structural at the abstract-substrate level" with an explicit pointer: "the Setup Frame conditions commit (i), (ii), (iii) as the *complete* primitive vocabulary of `→`, with no class (iv) admitted."

## OUT_OF_SCOPE

### Topic 1: Multi-arity link retraction semantics

The note restricts active-subset machinery to arity-3 links and acknowledges multi-arity retractions are well-formed Emit_R calls but operationally inert for A_K. Extending A_K^{(n),Σ} to higher arities is correctly deferred to Open Questions.

### Topic 2: Coordination across independent type catalog extensions

L9's TypeGhostPermission admits unilateral type-catalog extensions by different layers. Collision semantics (two layers choosing the same K independently) is genuinely new territory; correctly in Open Questions.

### Topic 3: Slice-wise reformulation without globally-s_C-resident content

The Setup hypothesis is load-bearing for R0 (L14a discharge), R4, and R5. The note explicitly defers the slice-wise version to Open Questions; this is appropriate scoping rather than a gap in the current note.

### Topic 4: Sibling-frontier discipline as substrate guarantee

Whether to tighten the substrate primitive to require the discipline (making R0a unconditional) is correctly placed in Open Questions — it's a design-axis decision, not an error in the present formulation.

VERDICT: REVISE
