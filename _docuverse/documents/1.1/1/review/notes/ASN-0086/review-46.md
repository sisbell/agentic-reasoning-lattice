# Review of ASN-0086

## REVISE

### Issue 1: R5 status row claims more than the proof delivers

**ASN-0086, Properties Introduced table, R5 row**: "Positive admissibility lemma: Stage 1 constructs the witness, Stage 2 verifies non-opposition by class-partition argument against ASN-0043's L-invariants and (by signature scope) ASN-0034 + ASN-0036 invariants"

**Problem**: The proof body's Stage 2 only inventories ASN-0043 L-invariants (L0/L0a/L1/L1a/L1b/L1c/L2/L3/L4/L5/L6/L7/L8/L9/L10/L11a/L11b/L12/L12a/L12b/L13/L14/L14a/L-fin). The claimed "(by signature scope) ASN-0034 + ASN-0036 invariants" verification does not appear.

**Required**: Either trim the table claim to match what the proof actually inventories, or add an explicit (even one-sentence) note in Stage 2 that ASN-0034/0036 invariants do not constrain endset target content and so are vacuously preserved.

### Issue 2: R7a's "factors through class (iii)" is ambiguous at categorical scope

**ASN-0086, R7a proof**: "any ↝-step that strictly extends dom(Σ.L) factors through class (iii) at the substrate."

**Problem**: ↝ ranges over "any-layer operations" by Definition. "Factors through" could mean (a) the net effect on Σ.L matches what class (iii) would produce, or (b) the layered operation invokes the class-(iii) primitive in its implementation. The proof needs (a) for the categorical claim, but the phrasing reads as (b). A higher-layer operation that bypassed class (iii) but happened to leave Σ.L extended at a fresh address would still be ↝, and the proof needs to show it cannot exist — not that it must invoke the primitive.

**Required**: Restate as net-effect: "any ↝-step with Σ.L ≠ Σ'.L must produce a Σ' identical to the result of some class-(iii) step at Σ" — then the proof's chain (L12 forbids modification, L12a forbids removal, classes (i)/(ii) by frame leave Σ.L unchanged) closes the claim by exhaustion over admissible Σ.L changes.

### Issue 3: R6b's proof body restates META content without proof depth

**ASN-0086, R6b**: classified META; proof body is two paragraphs of worked example showing predicate behavior at Σ_1 and Σ_2.

**Problem**: If R6b is genuinely META (a reading of the Definition's quantifier choice), the worked example belongs in a Remark rather than as a Proof, and the META framing should be the entire content. As written, the *Proof:* label suggests substantive derivation that does not occur — the conclusion follows from inspecting the Definition.

**Required**: Either relabel as Remark and tighten to one paragraph stating the property as a direct reading of the Definition; or strengthen the proof to show what is non-obvious (e.g., that the alternative quantifier range over A_R^Σ would change the predicate's behavior under retractor-retraction).

### Issue 4: wp Case 1's P3-SFD relationship is unclear

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "Under SFD the wp simplifies to P0 ∧ P1 ∧ P2 ∧ P3 alone (P3 becomes automatic from SFD via R0a's antichain)."

**Problem**: If P3 becomes automatic from SFD, the wp under SFD should reduce to P0 ∧ P1 ∧ P2 (with P3 discharged automatically), not "P0 ∧ P1 ∧ P2 ∧ P3 alone." The parenthetical contradicts the simplification.

**Required**: Pick one form. Either "the wp reduces to P0 ∧ P1 ∧ P2 because SFD discharges P3" (operational form for disciplined callers) or "the wp remains P0 ∧ P1 ∧ P2 ∧ P3 ∧ SFD, with P3 automatic at reachable states" (full form).

### Issue 5: R0 Step 4's ASN-0036 invariant preservation is asserted without enumeration

**ASN-0086, R0 Step 4**: "every ASN-0036 S-invariant hold by input-substitution"

**Problem**: One-line claim covering S0, S1, S2, S3, S7a–S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ — thirteen distinct invariants. R0 modifies only Σ.L (frame conditions on class (iii) hold Σ.C and Σ.M identical), so input-substitution is the right argument, but the table's depth standard for substrate-foundational claims warrants explicit acknowledgement. A reader cannot tell from "by input-substitution" whether each S-invariant has been individually considered.

**Required**: Add one sentence enumerating the S-invariants by their free-variable scope: "Every ASN-0036 S-invariant has free variables only in (Σ.C, Σ.M); since Σ'.C = Σ.C and Σ'.M = Σ.M by the class-(iii) Frame, every such invariant holds at Σ' by direct substitution of the unchanged components." This is roughly the same word count and discharges the verification explicitly.

### Issue 6: Emit_K seed-independence depends on conditional R0a without flagging

**ASN-0086, Definition — Emit_K, "Case B's seed-independence"**: "Under R0a's sibling-stream invariant (above), every a' ∈ dom(Σ.L) with home(a') = d lies on the single sibling stream..."

**Problem**: R0a is conditional on the sibling-frontier discipline (explicitly so in its statement). Emit_K is defined as "the sibling-frontier-disciplined subset of the substrate emission primitive," so the discipline is built into Emit_K's definition — but the seed-independence proof invokes R0a as if unconditional. The reader has to trace: Emit_K is disciplined by construction → R0a applies to Emit_K-induced traces → seed-independence holds. The proof should state this composition explicitly.

**Required**: Insert one sentence near the start of the seed-independence paragraph: "Since Emit_K commits to R0 Step 2's construction by signature, every Emit_K-induced trace respects the sibling-frontier discipline, and R0a (otherwise conditional) applies unconditionally within Emit_K's semantics." This makes the conditional-to-unconditional bridge visible.

### Issue 7: Defensive rationale paragraphs accumulate around design choices

**ASN-0086**: TypedRelation Definition contains "Rationale for coverage-equivalence" (~110 words) and "Asymmetry between T_cat^Σ and L_K^Σ" (~150 words); Implementation hypotheses ends with "Implementation realizability" (~70 words); Frame conditions on the primitive transitions ends with "Concrete implementations may maintain auxiliary backing structures..." (~70 words).

**Problem**: Each paragraph defends *why* the surrounding definition or commitment is the right choice — they explain why coverage-equivalence beats literal equality, why T_cat^Σ is descriptive not constitutive, why the udanax-green realization matters, why implementations may have richer backing. None of this advances the definition itself; the prose reads as drift from prior reviser cycles.

**Required**: Either move these to a separate "Design notes" section at the end (where defensive justifications cannot interrupt structural reasoning) or trim each to one sentence inside its parent definition. The Asymmetry paragraph's load-bearing claim ("L_K^Σ is the coverage-class slice over which active-subset and retraction machinery operate") can be inlined into the TypedRelation Definition itself.

### Issue 8: R5 Stage 2's "Permissive/Orthogonal" inventory is verbose

**ASN-0086, R5 Stage 2**: classifies each L-invariant from L0 through L-fin as "Permissive" or "Orthogonal" with one-clause justifications.

**Problem**: The inventory style enumerates 16 L-invariants, but the load-bearing observation is structural: no L-invariant constrains endset *target content*; L4(c) explicitly permits link-subspace targets. Stating this once with the L4(c) citation suffices for non-opposition; the per-invariant classification adds bulk without advancing the argument.

**Required**: Condense to: "L4(c) explicitly permits link-subspace targets in endset spans; no L-invariant constrains endset target content (each L-invariant's free variables either name the link address, the arity, or the from/to/type *positions* rather than what those positions cover). The construct is therefore admissible by L4(c) + L13 + R0." Drop the enumeration.

### Issue 9: Navigation/scoping paragraphs add meta-overhead

**ASN-0086**: Setup section ends with "Discipline-conditional claims" navigation paragraph; Implementation hypotheses section has its own *Discipline-conditional claims* note; R0a-Cor1's proof has a labeled "Direction of the strengthening" paragraph; R0a's Stage 2 has "Sibling-stream invariant statement" as a labeled sub-paragraph wrapping the statement.

**Problem**: Each of these is a labeled prose container that says "this is where X happens" without performing X. The two Discipline-conditional notes restate each other's content. The "Sibling-stream invariant statement" label adds a frame around what is otherwise a single displayed formula.

**Required**: Drop the labels. State the invariant directly, state the conditionality once at first introduction (Implementation hypotheses) and reference back from Setup. Inline the "Direction of the strengthening" content into the induction's IH statement.

### Issue 10: R0's defensive prose about L1c chain semantics repeats Sparse-allocator hypothesis

**ASN-0086, R0 Step 2 Case A and Case B**: phrases like "L1c asserts the existence of a conforming chain to a, not the re-issuance of every spawn that chain traverses" and "the chain witnesses a as a legal allocator output, not as a re-emission" recur three or four times.

**Problem**: This is the Sparse-allocator hypothesis being re-justified at each invocation site. The hypothesis is stated once in Implementation hypotheses; the proof should be able to invoke "by the Sparse-allocator hypothesis, the L1c chain is a conformance witness, not an operational sequence" once and proceed.

**Required**: Strip the defensive recurrences. Cite Sparse-allocator hypothesis once at the start of Step 2 and let the rest of Step 2 use chain-witnessing without repeated justification.

### Issue 11: Worked Sketch's "Allocator scaffolding" interrupts the main narrative

**ASN-0086, Worked Sketch, Concrete instantiation section**: the *Allocator scaffolding (by SharedDepthOneAllocator, R0a-Cor2)* sub-paragraph (~200 words) interrupts the address-assignment list with extended allocator-tree exposition.

**Problem**: The sketch is meant to verify concrete instantiation of the schematic claims. The allocator-tree exposition belongs in the SharedDepthOneAllocator lemma's own derivation (which already establishes the structure). Re-deriving the chain `(d, 2) → A_{d.0.1}; sibling sweep; (d.0.s_L, 1) → A_{a₁}` here duplicates work and pushes the address-assignment list past the reader's working memory before completing the setup.

**Required**: Move the allocator scaffolding into a single back-reference: "By SharedDepthOneAllocator, A_{d.0.1} is the depth-1 shared allocator under d; A_{a₁} = A_{d.0.s_L.1} is the depth-2 link allocator with first emission a₁." Let the reader trace details back to the lemma.

## OUT_OF_SCOPE

### Topic 1: Multi-arity active subsets

**Why out of scope**: A_K^Σ is defined only over standard-triple links. Higher-arity active-subset machinery (A_K^{(n),Σ}) is properly future work — the open questions enumerate it correctly.

### Topic 2: Atomicity and consistency of Emit relative to Observe

**Why out of scope**: Concurrent semantics is a layer above the per-state substrate definitions this ASN establishes. The open questions identify this correctly.

### Topic 3: Interaction between L_K and arrangement modifications beyond R6c-Corollary

**Why out of scope**: Predicates that depend on whether content referenced by an L_K tuple is currently visible in some Σ.M(d) involve cross-store coordination not yet addressed by either ASN-0036 or this ASN; identified as open question #1.

VERDICT: REVISE
