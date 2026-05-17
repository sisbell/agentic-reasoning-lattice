# Review of ASN-0086

I worked through R0 through R7, the operations, and the Worked Sketch. The proofs are largely sound — the compositional structure from ASN-0034/0036/0043 holds, the hypothesis stack is honestly tagged, and the Worked Sketch concretely exercises the substantive claims. My concerns are largely about framing and density rather than correctness.

## REVISE

### Issue 1: R7's title and framing obscure its stipulation-conditionality

**ASN-0086, R7 (NullifyIsEmit)**: "all *relational-layer* state change reduces to a single primitive: `Emit_K`"

**Problem**: The title and headline statement read as a derived theorem. The decomposition into R7a (proven from Frame) and R7b (adopted as model commitment) is clearly explained in the proof and consequence tags, but the composite headline still suggests substrate-level reduction. A reader scanning the table of properties sees "R7 — NullifyIsEmit" and may not register that the closure is stipulation-conditional.

**Required**: Either rename R7 to something like "RelationalLayerOperationClosure (composite, stipulation-conditional)" or restructure to list R7a and R7b as the primary claims and present R7 only as the joint corollary. The headline should not state derived content that is in fact half-stipulated.

### Issue 2: R6's listing as numbered lemma is misleading

**ASN-0086, R6 (ActiveSubsetWellDefinedness)**: "R6 itself is therefore classified as a definitional companion to the Definition of ActiveSubset, not a substantive lemma; we list it for citation symmetry with R6a/R6b/R6c, not as an independent deductive result."

**Problem**: The ASN openly admits R6 is not a substantive result. Yet it appears as a numbered R-claim alongside R6a/R6b/R6c. This creates listing clutter and invites confusion: readers may search for the proof of R6 expecting a derivation. The substantive contribution (the active/audit distinction) is carried by R6a/R6b/R6c — not by R6.

**Required**: Either fold R6's content into the Definition of ActiveSubset (drop the R6 listing entirely), or strengthen R6 to a substantive claim by adding algebraic properties of A_K (e.g., its relationship to L_K under specific operations) that aren't already in R6a/R6b/R6c.

### Issue 3: Allocator naming convention is inconsistent

**ASN-0086, multiple sites (SharedDepthOneAllocator lemma, R0 Step 2, Worked Sketch)**: `A_d` denotes the allocator at depth 1 below `d` (with first emission `d.0.1`); `A_{a₁}` denotes the depth-2 link allocator whose first emission IS `a₁`.

**Problem**: The subscript means different things in the two cases — parent-name in one, first-emission-name in the other. The Worked Sketch's references to "the depth-2 link allocator `A_{a₁}` (rooted at `a₁`)" require the reader to remember which convention is in force at each reference. The SharedDepthOneAllocator lemma compounds this by referring to "the allocator opened by the `(d, 2)` child-spawn" as `A_d`, while the `(d.0.s_L, 1)` child-spawn opens an allocator referred to as `A_{a₁}` in the Worked Sketch (where `a₁ = d.0.s_L.1`).

**Required**: Pick one convention and apply it uniformly. The cleanest choice is first-emission-named: `A_x` denotes the allocator whose first emission is `x`. Under that convention, `A_d` would be replaced by `A_{d.0.1}` everywhere, and the depth-2 link allocator remains `A_{a₁}`.

### Issue 4: Length and density obscure the structural argument

**ASN-0086, full document**: Approximately 25,000 words.

**Problem**: The Worked Sketch alone re-verifies the L0–L14a / L-fin invariants three times (at `b₁`, `a₂`, `a₃`, `b₂`, `a₃`, `b₃`) when R0 Step 4 already discharges these uniformly. The Setup section runs through five non-foundation hypotheses with detailed motivation for each. Appendix B's failure-mode analysis runs to multiple paragraphs with concrete tumbler arithmetic. The "Sole sourcing" paragraph, the "Maintenance protocol" elaboration, and the Hypothesis dependency view table all repeat substantially overlapping content about what counts as a direct vs. indirect dependency.

The substantive contribution — the active/audit distinction (R6a/R6b/R6c) plus the sibling-frontier discipline (R0a) plus the operation closure (R7) — can be presented in approximately one-third the space without losing rigor.

**Required**: Condense or restructure. Suggested moves: (a) Worked Sketch's repeated per-invariant verifications cited as "discharges identically to `b₁`'s verification above" with one canonical worked example; (b) Setup section consolidated to introduce the five hypotheses once with cross-references rather than re-explaining each at every consumption site; (c) Appendix A.3 (Maintenance protocol) merged into the Setup section's main text, removing the duplication.

### Issue 5: Hypothesis dependency table's "(inherited)" notation conflates dependencies

**ASN-0086, Hypothesis dependency view table**: R0a-Cor1 and R0a-Cor2 are tagged "Direct discipline: req (inherited)".

**Problem**: The "Direct" column should record whether the claim's own proof consumes the hypothesis. R0a-Cor1's induction directly requires the discipline at each inductive step (Sub-case B reads off `J_{d_new}^Σ` from the disciplined prefix). The "(inherited)" parenthetical suggests the dependency is indirect via R0a, which understates the direct use. Either it's direct (in which case drop "(inherited)") or it's indirect (in which case move to the Indirect column).

**Required**: Either remove "(inherited)" or move the entry to the Indirect column with a clear "via R0a" justification.

### Issue 6: The "substrate primitive in isolation" framing recurs without consolidation

**ASN-0086, scattered through Setup, R0, R0a, Emit_K, Nullify, Appendix B**: Repeated phrases like "the substrate primitive in isolation admits broader class-(iii) deposits" and "the discipline is realizable but not entailed".

**Problem**: This distinction — between what the substrate primitive permits and what the discipline restricts — is load-bearing for R0a and Nullify. But the framing is scattered across roughly ten passages, each restating the same point with slight variations. The reader has to assemble the picture from fragments.

**Required**: Establish the discipline-vs-primitive distinction once in the Substrate emission primitive paragraph, then refer back rather than re-explaining. The "Breadth of the primitive vs. the discipline R0a names" paragraph should be the single canonical statement, with downstream sites citing it by name.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link active subsets
**Why out of scope**: ASN-0086 explicitly restricts to standard triples; the open question (`A_K^{(n)}` for `|Σ.L(a)| > 3`) is correctly deferred. ASN-0086 should not be expanded to cover this; a future ASN should.

### Topic 2: Concurrency / atomicity of Emit and Observe
**Why out of scope**: ASN-0086 specifies single-state and single-transition semantics. Concurrency is appropriately flagged as a future question.

### Topic 3: Discharging the sibling-frontier discipline at substrate level
**Why out of scope**: A future revision could tighten ASN-0043's L1c or the substrate emission primitive to make R0a unconditional; this is correctly flagged as future work in Open Questions.

### Topic 4: Deeper-sited link addresses (`#E ≥ 3`)
**Why out of scope**: R0a-Cor2 honestly records the tension between the discipline's narrowing and Nelson's foundational design intent; relaxation requires reformulating R0a, Nullify, and the antichain machinery, properly a future ASN.

### Topic 5: L14 in native scoped form (without global s_C-residency)
**Why out of scope**: The Open Questions section identifies the slice-wise reformulation as future work.

### Topic 6: Dynamic type catalog extension under L9
**Why out of scope**: Higher-layer concern, appropriately deferred.

VERDICT: REVISE
