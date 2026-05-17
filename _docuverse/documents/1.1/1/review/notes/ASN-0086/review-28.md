# Review of ASN-0086

## REVISE

### Issue 1: R0a Case 2 sub-argument wording error
**ASN-0086, R0a's antichain corollary, Case 2 sub-argument**: "so the prefixes of a and a' ending at their respective second zeros are the same tumbler (they are the position-for-position-equal prefix of a' of length (position of second zero in a)...). By L1a's definition home(·) = N(·).0.U(·).0.D(·) — exactly this prefix..."
**Problem**: The "prefix of length (position of second zero)" is `N(·).0.U(·).0` (ends with the second zero). But L1a's home is `N(·).0.U(·).0.D(·)` — includes `D(·)` and ends just before the third zero. These are distinct prefixes of different lengths. The argument identifies them as "exactly this prefix" without the bridging step that establishes `D(a) = D(a')`.
**Required**: Either (a) restate the prefix as "of length (third zero position) − 1, which contains D(·)" and show this prefix is shared (which follows from a ≼ a' agreeing on positions 1..#a since p3 ≤ #a), or (b) explicitly add the D-agreement step: since both a and a' have their third zero at the same position p3, D(a) and D(a') occupy the same positions and agree by a ≼ a'.

### Issue 2: R6c proof omits L_K monotonicity step
**ASN-0086, R6c proof**: "Apply R6a to the single step Σ_k → Σ_{k+1} to obtain a ∈ nullified(Σ_{k+1}) = nullified(Σ'). By Definition of A_K, since a ∈ nullified(Σ'), (a, F, G) ∉ A_K^{Σ'}."
**Problem**: To conclude `(a, F, G) ∉ A_K^{Σ'}` via the set-difference `L_K^{Σ'} \ {nullified}`, we need `(a, F, G) ∈ L_K^{Σ'}` first. The hypothesis gives `(a, F, G) ∈ L_K^Σ`, but propagation to Σ' requires R3 (TypedSliceMonotonicity).
**Required**: Add one line: "By R3 applied to the inductive chain, `(a, F, G) ∈ L_K^Σ ⊆ L_K^{Σ'}`; then by Definition of A_K..." The argument trivially closes but is currently incomplete.

### Issue 3: Worked sketch "first four entries" wording
**ASN-0086, Worked Sketch Step 6 P3 verification**: "dom(Σ_5.L) = {a₁, b₁, a₂, b₂, a₃}. The first four entries — a₁, b₁, a₂, a₃ — are all siblings in the depth-2 allocator A_{a₁}..."
**Problem**: A set has no canonical ordering, so "the first four entries" is ill-defined. By emission order the first four are `a₁, b₁, a₂, b₂` (b₂ is cross-document, not in A_{a₁}'s stream). The intended meaning is "the four entries homed at d" but the phrasing creates a momentary inconsistency.
**Required**: Rephrase as "the four entries homed at d — a₁, b₁, a₂, a₃ — are all siblings in A_{a₁}; the fifth entry b₂ is homed at d' and handled separately below."

### Issue 4: R7's stipulated half buried in Step 3 narrative
**ASN-0086, R7 statement and Step 3**: R7's headline reads as a theorem ("the reduction"); the stipulated half ("every relational-layer-initiated class-(iii) step is an Emit_K call") is only distinguished from the proven half (categorical exclusion of non-class-(iii) Σ.L-affecting transitions) midway through Step 3's prose.
**Problem**: A reader of R7's statement alone would naturally treat the reduction as fully derived. The asymmetry between proven and stipulated halves is the single most important caveat of R7, and shifts the operational closure claim from theorem to layer commitment. Burying it in mid-paragraph is a clarity hazard.
**Required**: State R7 in two explicit sub-claims at the top — "R7a (PROVEN, from L12 + L12a + Frame): no Σ.L-affecting transition exists outside class (iii)" and "R7b (STIPULATED, model commitment): every relational-layer-initiated class-(iii) step is an Emit_K call". Then unfold the reduction in Step 4 as their composition.

### Issue 5: Setup/discipline conditionality lacks a consolidated dependency view
**ASN-0086, throughout**: Each R-claim carries `[Setup-required]`, `[Setup-free]`, or `[discipline-conditional]` tags; the "Setup dependence at a glance" paragraph enumerates Setup-dependent claims but does not show discipline propagation, and the Properties Introduced table repeats the tags inline without showing transitive dependencies (e.g., R5's Setup-requirement comes via R0, Nullify's discipline-conditionality comes via R0a).
**Problem**: Tracking which R-claim is grounded in which hypothesis requires correlating the headline tag, the proof's appeals, and the Properties table. The transitive structure (R5 depends on R0, Nullify depends on R0a, etc.) is implicit.
**Required**: Add a dependency table at the end of the "Properties Introduced" section showing for each R-claim: (a) direct dependencies on Setup, (b) direct dependencies on discipline, (c) indirect dependencies on either via other R-claims. This compresses the propagation analysis into one citable view.

### Issue 6: SharedDepthOneAllocator's role in worked sketch chain is implicit
**ASN-0086, Worked Sketch concrete instantiation**: The L1c chain for a₁ traverses `inc(d, 2) → d.0.1`, then sibling sweep within `A_d` from `d.0.1` to `d.0.2`. The SharedDepthOneAllocator lemma establishes that `A_d` is shared across content and link subspaces, but the worked sketch invokes this only via parenthetical phrases like "which serves both content and link subspaces" without re-citing the lemma.
**Problem**: A reader encountering "sibling sweep within A_d from subspace 1 (content) to subspace s_L = 2 (link)" must remember that subspaces 1 and 2 are at the *same* allocator (A_d at element-field depth 1), not at separate per-subspace allocators. Without explicit citation, this can read as if content and link share a stream by accident rather than by design.
**Required**: Add a one-line citation in the worked sketch's setup or at the first use: "By SharedDepthOneAllocator, A_d enumerates subspace identifiers at depth 1; subspace-internal allocators (A_{d.0.1} for content, A_{d.0.2} for links) live one element-field deeper."

### Issue 7: R0 Step 4 L11a discharge for Case A
**ASN-0086, R0 Step 4, L11a bullet**: "Case A: the spawn family terminates at the depth-2 child-spawn (d.0.s_L, 1), and T10a's at-most-once axiom on (d.0.s_L, 1) rules out a prior event opening the same depth-2 link allocator under d."
**Problem**: The discharge relies on T10a's at-most-once for the spawn pair `(d.0.s_L, 1)`. But under the sparse-allocator interpretation (Appendix A.1), R0 Step 2 Case A's chain is a *witness*, not a re-issuance — the (d.0.s_L, 1) spawn might or might not have been physically re-issued at this step. The L11a argument needs to be clearer about distinguishing "this spawn pair is admissible to fire now (Case A's first time) or has already fired and the new emission is at a child of the already-existing A_a allocator (Case B)."
**Required**: Either rework the Case A vs. Case B branching to make the spawn-event vs. witness-chain distinction explicit at L11a's discharge, or add a remark noting that L11a's "distinct allocation events" criterion is at the deposit level (which is class-(iii) atomic and fresh by R0 Step 2's freshness witness), not at the spawn-event level (which is sparse-allocator-mediated).

## OUT_OF_SCOPE

### Topic 1: Substrate-level enforcement of the sibling-frontier discipline
**Why out of scope**: The Open Questions section explicitly proposes elevating the discipline to a substrate-level guarantee via tightening Emit_K's spec or the substrate emission primitive. This would discharge R0a and Nullify's P3 unconditionally. Belongs in a future ASN that revisits ASN-0043's link-store primitives.

### Topic 2: Higher-arity active subsets `A_K^{(n),Σ}`
**Why out of scope**: L3 admits links with `|·| ≥ 3`; this ASN scopes to standard triples. Extending the active-subset machinery to arity-N relations requires defining `L_K^{(n)}` and re-deriving R3-style monotonicity, R6a-style stability, and Nullify's single-tuple-scope at higher arities. Flagged in Open Questions.

### Topic 3: Deeper-sited link addresses (`#E ≥ 3`)
**Why out of scope**: R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2` under the sibling-frontier discipline. Nelson's foundational design admits deeper sub-links (sub-links of sub-links); the udanax-green implementation does not exercise this. Relaxing the discipline to admit `#E ≥ 3` is a parallel design path requiring reformulation of R0a's invariant over a tree of allocators rather than a single stream.

### Topic 4: Concurrent emit/observe semantics
**Why out of scope**: Whether Emit must be atomic with respect to concurrent Observe, and what consistency model governs A_K transitions under concurrency, requires a concurrency model not present in ASN-0034/0036/0043. Flagged in Open Questions.

### Topic 5: Cardinality bounds on `nullified(Σ)` vs. `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted, or some structural ratio must hold, is a quantitative property not constrained by the present invariants. Flagged in Open Questions.

### Topic 6: Type catalog `T_cat` extension semantics under multi-author concurrency
**Why out of scope**: L9 permits ghost type addresses; two layers picking colliding type addresses without coordination is not addressed here. Flagged in Open Questions.

### Topic 7: Invariants between L_K and arrangements `Σ.M` for visibility-dependent predicates
**Why out of scope**: When relational predicates depend on whether from/to-set content is currently visible in some document, the L_K ↔ Σ.M interaction needs additional invariants. Belongs in a future ASN at the interface of relational and arrangement layers.

VERDICT: REVISE
