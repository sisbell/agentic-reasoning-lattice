# Review of ASN-0086

## REVISE

### Issue 1: R7's headline overstates a stipulation-conditional conclusion

**ASN-0086, R7 section**: "Under R7a and R7b jointly, the relational layer admits exactly two operational primitives... and every relational-layer state change reduces to a single `Emit_K` call."

**Problem**: R7's substantive content is split into R7a (proven, from L12 + L12a + Frame) and R7b (explicitly stipulated, not derived). The note acknowledges this in prose — "R7's headline is therefore irreducibly conditional" — but the resulting "reduction" is then cited throughout (R6c Consequence (d), Properties Introduced table) as if it were a derived theorem. A reduction whose key half is a definitional commitment is not the same kind of result as one derived from invariants.

**Required**: Either (a) reformulate R7 explicitly as a *model commitment* that the relational layer adopts (parallel to the Setup hypothesis and the sibling-frontier discipline) — letting R7a stand alone as the derived "no-extra-class" theorem and R7b stand alone as the layer's charter; or (b) downgrade R7's "all relational-layer state change reduces to `Emit_K`" headline to "given the relational-layer commitment R7b, the relational layer admits {Emit_K, Observe_K, Nullify-as-alias} as its primitives." The current presentation conflates a derivation with an adoption.

### Issue 2: R6 is essentially definitional, not a lemma

**ASN-0086, R6 section**: "For every state Σ and every K ∈ T_admissible, A_K^Σ is well-defined and computable from Σ.L alone."

**Problem**: The "proof" is one paragraph that observes A_K is defined by set-difference between L_K and tuples whose addresses are in nullified(Σ), both of which depend only on Σ.L. This follows immediately from the Definition of ActiveSubset; there is no substantive deductive step. The note even concedes "R6 itself is essentially a definitional check" in the headline narrative. Classifying R6 as a LEMMA inflates the result inventory.

**Required**: Either reclassify R6 as DEF (it's just a property of how A_K is defined), or replace it with a genuinely substantive observation — e.g., that *the active/audit distinction* (which is the actual contribution claimed in the headline) is captured by a single set-difference computation. The current R6 conveys no information beyond restating the definition.

### Issue 3: R0 Step 4's L-invariant verification is excessively granular

**ASN-0086, R0 Step 4**: Sixteen+ L-invariant bullets are enumerated individually (L0, L1, L1a, L1b, L1c, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11a, L11b, L12, L12a, L12b, L13, L14, L14a, L-fin, plus an ASN-0036 S-invariants bullet).

**Problem**: The FramePreservation lemma is introduced specifically to compress such enumerations via input-substitution, but is then used only for the ASN-0036 bullet. For L-invariants, only L0, L1, L1a, L1b, L1c, L11a, L14, and L14a genuinely require new analysis at the fresh address `a`; the remainder (L2, L4–L10, L12, L12a, L12b, L13, L-fin, L11b) follow from FramePreservation applied to predicates over either pre-state values or the new entry's value alone.

**Required**: Apply FramePreservation specialization (a) or (e) uniformly to the routine L-invariants in one consolidated paragraph, then discharge L0, L1, L1a, L1b, L1c, L11a, L14, L14a explicitly. The current style buries the substantive checks under repetitive bookkeeping. The same applies to R5 Stage 2's invariant enumeration.

### Issue 4: SharedDepthOneAllocator's "exactly one allocator at allocator-tree depth 1" statement conflates two depth notions

**ASN-0086, SharedDepthOneAllocator lemma**: "Under each document address d ∈ dom(Σ.M), there exists exactly one allocator at allocator-tree depth 1 below d — written A_d..."

**Problem**: Both child-spawns (d, 1) and (d, 2) are at allocator-tree depth 1 (both are single child-spawn events). The lemma actually establishes uniqueness of the depth-1 allocator *at zero-count depth 1* (the one opened by (d, 2)); (d, 1) also opens a depth-1 allocator by the allocator-tree count, but produces outputs at zero-count depth 0 (extending d's D field, i.e., new documents/versions). The statement reads as if (d, 1) does not open an allocator at allocator-tree depth 1, which is misleading.

**Required**: Restate as "exactly one allocator at allocator-tree depth 1 *whose outputs sit at zero-count depth 1*" (matching step (b) of the proof), or "the unique depth-1 allocator opened by the (d, 2) child-spawn." The current phrasing reads as a stronger claim than the proof supports.

### Issue 5: Cumulative hypothesis stack obscures which claims hold standalone

**ASN-0086, Setup + Subspace-distinctness + Sibling-frontier discipline + Unit-depth retraction discipline + R7b stipulation**: Five separate non-foundation hypotheses are layered through the document.

**Problem**: The dependency table at the end is helpful, but the per-claim tags use compound forms ("[Setup-free, discipline-conditional]", "[Setup-required (indirectly via R0)]") that vary in granularity. A reader trying to determine whether claim X holds under a partial-discipline implementation has to traverse multiple tables and pages of conditional language. The discipline-conditionality of R0a propagates silently into Nullify (single-tuple scope), R6c-Corollary's user-facing form, R7's reduction-via-R7b, etc.

**Required**: Standardize the tagging into a fixed three-field convention: `[setup: req|free, discipline: req|free|N/A, stipulation: req|free|N/A]` applied to every R-claim, corollary, and operation in their section headers. The table at the end can then be confirmation, not the primary mechanism for tracking propagation. Additionally, consider collecting all five hypotheses into one labeled "Model Commitments" section at the top so the reader sees the assumption stack before encountering any claim.

### Issue 6: R5's "exhaustive non-opposition check" mixes two proof strategies

**ASN-0086, R5 Stage 2**: "An exhaustive check of the ASN-0043 invariants confirms none is in opposition to the construction in Stage 1."

**Problem**: R5 is labeled a LEMMA but its proof structure is: Stage 1 constructs a witness (substantive), Stage 2 enumerates 22+ invariants and tags each as "orthogonal" or "compatible" (procedural). The result is more akin to a sanity-check audit than a deductive proof. The "Setup-required (indirectly via R0)" tag further muddies things — Stage 2 itself is Setup-free, but R5 inherits Setup-requirement from R0 which is invoked in Stage 1.

**Required**: Restructure as: (1) Stage 1 (existence) — the substantive content, via L4(c) + L13 + R0; (2) Stage 2 (non-opposition) — restated as a single observation that the invariants are partitioned into (i) those over pre-existing data (preserved by class-(iii) frame), (ii) those over tumbler-algebra properties of `a` (preserved by L4(c) + L13), and (iii) those discharged at R0 Step 4. The current 22-bullet enumeration is reassuring but not how proofs are most efficiently presented.

### Issue 7: Worked Sketch's length crowds out the principle

**ASN-0086, Worked Sketch**: Six steps with full concrete instantiation, including pairwise L-invariant verification at every emitted address.

**Problem**: The sketch exercises R0a, R5, R6a, R6b, R6c, R6c-Corollary, R7a, R7b — which is thorough — but at the cost of being roughly a third of the ASN's length. The per-step L-invariant verification at `b₁`, `a₂`, `b₂`, `a₃`, `b₃` rederives the same pattern (sibling-frontier discharge of L0/L1/L1a/L1b/L1c, Setup-driven discharge of L14/L14a) with mechanical adjustments to enumeration indices.

**Required**: Demonstrate the L-invariant pattern once (at `b₁`), then for subsequent emissions refer back: "L-invariants discharge identically to b₁ with enumeration index advanced to j = N." This preserves the demonstration of rigor while reducing repetition. Steps 3 (cross-document retraction) and 6 (R6b second-order retraction) carry distinctive structural content and should remain expanded; Step 4 (Observe) and Step 5.1 (fresh emission past retraction) could be substantially compressed.

### Issue 8: Class-(iii) frame conditions are presented as derivable but are actually definitional

**ASN-0086, Frame conditions section**: "These commitments are at the substrate-model interface and constrain only the visible values of Σ.C, Σ.M, Σ.L after the transition."

**Problem**: The note later says "Status — model definition, not derivation. The three classes (i), (ii), (iii) jointly *define* the dom-extending transition vocabulary..." But R0 Step 4 then invokes "Σ'.C = Σ.C and Σ'.M = Σ.M *by definition of class (iii)*" in the L-invariant verifications, while elsewhere the note appeals to S0 / S9 / L12 / L12a to justify the same frame components. The dual sourcing (sometimes definitional, sometimes invariant-derived) is confusing — for instance, the "Arrangement-modification frame" note painstakingly traces each component to a specific invariant, while class-(iii)'s frame is invoked definitionally.

**Required**: Pick one convention. If class-(iii)'s frame is definitional, drop the appeals to L12 / L12a as "load-bearing" sources for it in R7a's proof; L12 and L12a become invariants *consistent with* the definitional frame, not derivations of it. If the frame is meant to be invariant-derived, restate it that way and show the derivation. The current mix obscures whether R7a's proof is invariant-driven or definition-driven.

## OUT_OF_SCOPE

### Topic 1: Slice-wise treatment of R0, R4, R5 under L14's native scoped form
**Why out of scope**: The Setup hypothesis (globally `s_C`-resident content) is acknowledged as external and is itself an Open Question. Restating R0, R4, R5 slice-wise belongs in a future ASN that handles `s_L`-resident content or other subspace residencies.

### Topic 2: Higher-arity active subsets `A_K^{(n),Σ}`
**Why out of scope**: The note restricts to standard-triple links (arity 3) and explicitly defers higher-arity machinery to an Open Question. Extending nullified / active-subset semantics to higher-arity tuples is genuinely new territory.

### Topic 3: Substrate-level enforcement of the sibling-frontier discipline
**Why out of scope**: Listed as Open Question. Tightening the substrate emission primitive to forbid prefix-extension emissions would discharge R0a's discipline-conditionality and make Nullify's P3 automatic, but requires changes to ASN-0043's L1c or to the substrate emission primitive itself — out of scope for this ASN.

### Topic 4: Relaxation to admit deeper-sited link addresses (#E ≥ 3)
**Why out of scope**: R0a-Cor2 narrows L1b to #E = 2 under the discipline; relaxing this to admit Nelson's broader recursive sub-link design requires reformulating R0a's sibling-stream invariant over a tree of allocators. Genuinely new design.

### Topic 5: Concurrency, atomicity, and ordering on Observe results
**Why out of scope**: Listed as Open Questions. The ASN intentionally treats `→` as a sequential transition relation; concurrency is not in its scope.

### Topic 6: Cardinality bounds on `nullified(Σ)` and unbounded retraction
**Why out of scope**: Listed as Open Question. The substrate admits unbounded retraction emission per R0 and R3; whether structural ratios should bound this is a separate design question.

VERDICT: REVISE
