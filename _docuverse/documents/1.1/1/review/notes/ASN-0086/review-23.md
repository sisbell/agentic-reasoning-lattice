# Review of ASN-0086

## REVISE

### Issue 1: R6's framing as "the substrate's own contribution" overstates what R6 actually claims

**ASN-0086, opening paragraph and R6**: "Of the seven structural properties... six (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution" and R6's statement "A_K^Σ is well-defined and computable from Σ.L alone, with no auxiliary state."

**Problem**: R6 is essentially well-definedness by construction — `A_K^Σ = L_K^Σ \ {(a, F, G) : a ∈ nullified(Σ)}` is computable from Σ.L by inspection of the definition. The substantive contribution is the *active/audit distinction* (the concept that two views co-exist over the same store), realized in R6a–R6c. Labeling R6 itself as the "substrate's own contribution" misdescribes which lemma carries the load.

**Required**: Reframe so R6 is presented as well-definedness, and R6a (RetractionStability) + the active/audit distinction is identified as the conceptual contribution. The Setup paragraph claim should similarly be revised.

### Issue 2: The Shared depth-1 element-field allocator derivation is dense and would benefit from being a named lemma

**ASN-0086, Setup section**: "Shared depth-1 element-field allocator — corollary of L0 + T10a + S7d" with multi-paragraph derivation labeled (i), (ii), (iii).

**Problem**: The derivation is correct and load-bearing — consumed at R0 Step 2 Case A and at the worked sketch — but is buried in Setup prose. The argument that `(d, 2)` is the unique spawn introducing a depth-1 element-field (the key claim) rests on "each `k'` selects a distinct depth level at which the new zero is introduced" without showing this directly via TA5(d). A reader has to assemble the argument from TA5(d)'s "k - 1 zeros" clause across `k' ∈ {1, 2}`.

**Required**: Lift to a named lemma (e.g., "SharedDepthOneAllocator") with an explicit proof structure: (a) the only T10a-admissible child-spawns from d are (d, 1) and (d, 2); (b) only (d, 2) introduces a zero (by TA5(d) with k' - 1 ≥ 1 only when k' = 2); (c) T10a at-most-once on (d, 2) gives uniqueness. Citations to the corollary then point to the named lemma rather than re-deriving in prose.

### Issue 3: The worked sketch underexercises boundary cases relative to the abstract claims

**ASN-0086, "Worked Sketch" section**: The concrete instantiation exercises Emit_K (Step 2), Nullify (Step 1), and the active-subset transition between them.

**Problem**: Several admissible configurations specified in the abstract are not exercised:
- Emit_K with F = ∅ or G = ∅ (admitted by Endset = 𝒫_fin(Span))
- Cross-document retraction with d_retr ≠ home(a) (newly admitted by Nullify's signature change)
- Retracting an already-nullified tuple (operationally inert but emits a fresh L_R tuple)
- Observe_K invocation (no concrete demonstration of audit vs. operational view)
- A higher-arity admission test (P2 rejection)

The asymmetry between Nullify's "any d_retr ∈ dom(Σ.M)" admission and the worked sketch's implicit use of d_retr = home(a) is particularly notable since the ASN explicitly argues against the prior home(a) default ("Why d_retr is a caller parameter").

**Required**: Add at least one alternate-d_retr concrete trace (a third document d' ≠ d allocating the retraction), and one Observe_K invocation showing both hist and oper views over Σ_2 returning different result sets.

### Issue 4: The Subspace-distinctness axiom's relationship to ASN-0043's L0/L0a partition is underspecified

**ASN-0086, Setup section**: "ASN-0043 names the partition without explicitly axiomatizing s_C ≠ s_L as a single clause; this note consumes the distinctness directly..."

**Problem**: L0a's definition of the `s_C`-resident slice and L14's scoped disjointness already presuppose s_C ≠ s_L — otherwise the slice is not a proper sub-slice and L14 collapses. The axiom is therefore not strictly *new* to ASN-0086; it is implicit in ASN-0043's machinery, and what this ASN adds is the explicit naming. The "axiom of this note" framing suggests a new commitment when what's happening is making implicit content explicit.

**Required**: Clarify that the axiom is being *named* and *explicitized* rather than added — e.g., "We name explicitly the distinctness that ASN-0043's L0/L0a partition presupposes." This is the more accurate framing and avoids the impression of an additional substrate commitment.

### Issue 5: R7's "stipulated half" framing could mislead about the reduction's scope

**ASN-0086, R7 Step 3**: "*Proven half — derived from L12, L12a, and the Frame conditions* ... *Stipulated half — adopted, not derived*: every relational-layer-initiated class-(iii) step is an Emit_K call."

**Problem**: The proof is honest about the decomposition, but R6(d) and the abstract's opening — "all *relational-layer* state change reduces to a single primitive: Emit_K" — read as derived conclusions. A careful reader engaging only with R6(d) or the abstract may not realize the closure depends on a definitional commitment of the relational layer to the sibling-frontier-disciplined subset of the substrate primitive. The breadth-vs-discipline tension noted at R0a is concentrated here too: the substrate emission primitive in isolation admits class-(iii) deposits the reduction excludes.

**Required**: Flag the stipulated half explicitly at R6(d) and at the abstract paragraph ("reduces to a single primitive: Emit_K"), with a one-sentence reference forward to R7's Step 3 decomposition. The reduction claim is best stated as "the relational layer commits to Emit_K as its sole state-affecting primitive" rather than as a derived structural result.

### Issue 6: R0a-Cor1's proof relies on the strengthened invariant as IH without explicitly noting the strengthening direction

**ASN-0086, R0a-Cor1 proof**: "By induction on the →-chain length, parallel to R0a's induction."

**Problem**: The induction is over the contiguous-prefix invariant (the strengthening), not over R0a's sibling-stream invariant. The Sub-case B argument uses the IH "the existing homed set is {inc^j : 0 ≤ j ≤ J_d^Σ}" — which is the strengthened invariant — to bound k. But the proof doesn't explicitly note that the ⊆ direction (every link is at some inc^j) is inherited from R0a, while the ⊇ direction (contiguous prefix, no gaps) is the strengthening proved here.

**Required**: One sentence at the proof's start clarifying which direction is the strengthening over R0a, and that the IH carries the contiguous-prefix property (not just sibling-stream membership). This makes the inductive step self-contained and not requiring the reader to infer which invariant is being maintained.

### Issue 7: R0 Step 2 Case A's sibling-sweep argument relies on the sparse-allocator semantics established at the substrate primitive — the dependence could be more visible at the proof site

**ASN-0086, R0 Step 2 Case A**: "Sibling sweep `inc(·, 0)` within A_d, advancing from A_d's base d.0.1 ... to d.0.s_L (enumeration index s_L at the same depth), applied s_L − 1 times..."

**Problem**: The chain witnesses positions d.0.1, d.0.2, ..., d.0.s_L without requiring intermediate emissions to have occurred. The substrate emission primitive section establishes this via the sparse-allocator interpretation ("at the allocator-state level... the substrate primitive's atomic class-(iii) step implicitly extends Act(s) and n_s"). The proof at Case A acknowledges "L1c asserts the existence of a conforming chain to a, not the re-issuance of every spawn that chain traverses" — but a reader following the proof linearly may not recall that the sparse-allocator semantics is the substantive commitment making this valid.

**Required**: One pointer at the sibling-sweep step back to the sparse-allocator paragraph, or a brief restatement that the chain "witnesses" rather than "materially traverses" the intermediate positions. The current handling is correct but the load-bearing semantic commitment is non-local.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link active-subset machinery (A_K^{(n)})

**Why out of scope**: The ASN appropriately restricts L^Σ to standard-triple (arity-3) links and defers higher-arity treatment to a future ASN. The Open Questions section enumerates this, and the Operational scope discussion at `nullified(Σ)` addresses the asymmetry within the present scope.

### Topic 2: Lifting R0a's discipline to a substrate-level guarantee

**Why out of scope**: The ASN identifies two routes (tightening Emit_K's specification, tightening the substrate primitive) but appropriately leaves this for future work. The discipline-conditionality is honestly traced throughout.

### Topic 3: Relaxing the discipline to admit deeper-sited link addresses (#E ≥ 3)

**Why out of scope**: Nelson's foundational design admits deeper sub-links; R0a-Cor2's narrowing to #E = 2 is documented as a tension. The relaxation requires re-derivation of R0a's sibling-stream invariant over an allocator tree rather than a single stream, properly future work.

### Topic 4: Slice-wise reformulation of Setup-required claims (R0, R4, R5) under L14's native scoped form

**Why out of scope**: Dropping the globally `s_C`-resident-content Setup hypothesis is explicitly listed in Open Questions with a detailed sketch of what would need re-derivation.

### Topic 5: Cross-substrate concurrency model and atomicity of Emit vs. Observe

**Why out of scope**: Listed in Open Questions. The present ASN works in a single-state evolution model.

### Topic 6: Type catalog dynamic extension and collision handling

**Why out of scope**: Listed in Open Questions. L9 admits ghost types; the question of coordination across higher layers is future work.

VERDICT: REVISE
