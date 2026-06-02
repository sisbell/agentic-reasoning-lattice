# Review of ASN-0047

The core transition model is rigorous. I checked the K.δ case split (k=0/1/2 + node baptism) for level/zeros coverage, the K.μ⁻ constructive-vs-post-state equivalence proof (both directions, including the V_S(d')⊆V_S(d) prefix recovery and depth inheritance), K.μ~-FIX, the FrontierEquivalence biconditional, and the J0/J1★/J1'★ composite-boundary discharge including the K.α→K.ρ→K.μ⁺ ordering robustness. These hold. The findings below are residual completeness/meta-prose issues, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Worked examples fire K.μ~ without discharging its firing precondition
**ASN-0047, "Worked example: fork..." (Reorder d₂) and "Worked example: link allocation..." (Step 3)**: Both invoke K.μ~ — e.g. "*K.μ~:* The bijection π : {[1,1], [1,2]} → {[1,1], [1,2]}..." — and verify J3, ran-preservation, S3★, but never check the operation's stated firing precondition: "`M(d)|_{dom_C(M(d))}` takes at least two distinct values ... a transition whose `M(d)|_{dom_C}` is constant-valued ... does not fire."
**Problem**: The precondition is the necessary-and-sufficient firing condition (it excludes no-op swaps of equal-valued transcluded positions — exactly the case S5 makes possible). A worked example that exercises K.μ~ must discharge it; otherwise the example does not demonstrate that K.μ~ legitimately fires, only that the effect is well-typed. The standard "the ASN should verify its key preconditions against a specific scenario" is unmet for this operation.
**Required**: In each reorder step, state the check explicitly (e.g. "M(d)|_{dom_C} = {[1,1]↦a₁, [1,2]↦a₂} with a₁ ≠ a₂ — two distinct values, so K.μ~ fires").

### Issue 2: NodeRootedForest second paragraph restates the first
**ASN-0047, NodeRootedForest (Derived structure)**: Paragraph 1 establishes "Nodes enter E *only* via NodeBaptism, never as inc-outputs ... The inc-allocator structure is therefore a *forest*." Paragraph 2 then says: "The 'forest' framing is consistent with NodeLineage's single prefix-root `n₀ ≼ e`: prefix-nesting is not inc-descent. Nodes are baptised rather than inc-emitted, so even where one node base prefix-nests under another ... neither is the other's inc-descent — each remains an independent inc-root."
**Problem**: This matches the flagged pattern "two paragraphs in the same document say the same thing in different words." "Nodes are baptised rather than inc-emitted" / "prefix-nesting is not inc-descent" re-encode paragraph 1's "never as inc-outputs" claim. The reconciliation-with-NodeLineage content is a single sentence buried in restatement.
**Required**: Collapse to one sentence appended to paragraph 1: "prefix-nesting (NodeLineage's `n₀ ≼ e`) is not inc-descent, so prefix-nested node bases remain independent inc-roots."

### Issue 3: "Scoped coupling constraints" preamble is imposed-vs-derived meta-prose
**ASN-0047, Scoped coupling constraints (opening)**: "Provenance coupling must be scoped to content-subspace arrangement extensions, scoped per P4★ above, and is *imposed* rather than derived: Nelson's commitment to a permanent reverse index ... is what fixes both directions, while the wp derivations below motivate the couplings without compelling them."
**Problem**: This is "why the axiom is needed" prose preceding the actual definitions (J1★/J1'★). The epistemic disclaimer ("motivate ... without compelling") and the forward pointer ("the wp derivations below") are meta-commentary the reader processes before reaching content; the substantive imposed-vs-derived status is already carried by J0's "**Axiomatic**" label and the J1★/J1'★ derivations' own framing.
**Required**: Reduce to the operative sentence: "J1★ and J1'★ are imposed (not derived); the wp derivations below give the motivating obligation." Remove the Nelson/Gregory restatement (already stated at P0/P2).

### Issue 4: P4a discharge mechanism restated redundantly across matrix and prose
**ASN-0047, Class (b) verification matrix and Class (b) prose**: The matrix cell reads "By the induction-along-the-witnessing-trace mechanism of the P4a definition box." The following prose repeats: "discharged by the induction-along-the-witnessing-trace mechanism of its definition box (all other transitions hold R in frame)."
**Problem**: The discharge lives in the P4a definition box; both the matrix cell and the prose name the same mechanism with the same phrase, so one of the two is pure duplication (distinct from navigational indexing — this is the same sentence twice, not a cell pointing at prose that elaborates).
**Required**: Keep the matrix cell's pointer; in the Class (b) prose, cite the box without re-naming the mechanism, or drop the P4a prose line entirely (the matrix already routes to the box).

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The ASN's own Open Questions already flag that K.μ⁻ models only suffix removal, not the implementation's compact-and-renumber interior `DELETEVSPAN`. This is correctly deferred — named operations and their mechanics are out of scope — so no REVISE is warranted; the suffix-only contraction is internally consistent.

### Topic 2: Link-subspace reordering
K.μ~ is scoped to content reordering (full-clearance retains links pointwise). Reordering links via withdraw-and-re-add is noted under "Link V-position permanence." A dedicated link-reorder primitive is future territory, not a gap here.

VERDICT: REVISE
