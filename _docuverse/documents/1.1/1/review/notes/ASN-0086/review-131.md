# Review of ASN-0086

## REVISE

### Issue 1: WP Case 2 "Direct K.λ callers" paragraph elaborates regimes the note's operations exclude

**ASN-0086, Weakest-Precondition Analysis, Case 2**: "The substrate does not preclude a direct K.λ caller that bypasses the relational layer; such a caller may emit a crafted-span retraction ... (*regime (ii)*) ... or ... (*regime (iii)*) ... and therefore carries the strictly stronger precondition `d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` ... These callers lie outside this note's vocabulary; its operations never reach regimes (ii)/(iii) ..."

**Problem**: The wp is computed for the note's operation set `{Emit_K, Observe_K, Nullify}`. This paragraph then constructs a fuller precondition — introducing the `NoCraftedSpanReachesD` predicate and a self-nullification disjunct — for callers the paragraph itself states are outside the vocabulary and "never reach." This is exactly the flagged accretion pattern: a passage imagining a case the claim's carrier already excludes, expanded into a named predicate. The scoping point ("the simple wp holds only because the note's operations avoid crafted/self-nullifying retractions") can be made in one sentence without exhibiting the out-of-vocabulary precondition.

**Required**: Replace the regime-(ii)/(iii) elaboration and `NoCraftedSpanReachesD` definition with a single sentence noting that the result is relative to this note's operation set and that direct K.λ use voids the unit-depth and sole-R-producer disciplines the derivation relies on.

### Issue 2: R6b's "audit slice, not active subset" point is restated four-plus times

**ASN-0086**: The claim that `nullified`'s existential ranges over `L_R^Σ` (audit) rather than `A_R^Σ` (active) appears in Definition — Nullified ("The existential here quantifies over the *audit* slice `L_R^Σ`, not the active subset `A_R^Σ`"), in R6b's statement, in R6b's proof, in Worked Sketch Step 1 ("the existential ranges over `L_R^{Σ_1}` (audit slice)"), in Step 3, and in the Properties table row for R6b.

**Problem**: The same non-fixpoint semantics is re-explained in different words across at least four locations. This matches "two paragraphs in the same document say the same thing in different words." The worked-sketch occurrences are legitimate verification; the doubled prose explanations (Definition — Nullified + R6b statement + R6b proof) are redundant.

**Required**: State the audit-vs-active distinction once (in R6b), and have the Definition — Nullified note and the table row point to it rather than re-explain it.

### Issue 3: R0's "conjunct-by-conjunct" invariant discharge omits L5 and L6

**ASN-0086, R0 proof, *L-invariant preservation across the K.λ-step***: "We discharge the post-state invariants at the fresh key `a` conjunct-by-conjunct ..." — the proof then addresses S/M/C invariants, L-fin, L12/L12a, L14/L14a, L0/L1/L1b/L1a, L1c, and L3.

**Problem**: ASN-0043's `StateLocalInvariants` catalog (which R0 commits to preserving, and which Σ being state-local-conforming presupposes) lists L0, L1, L1a, L1b, L1c, **L5, L6**, L14, L14a, L-fin. L5 (EndsetSetSemantics) and L6 (SlotDistinction) are named members of that catalog and are never mentioned. A proof that claims conjunct-by-conjunct discharge but silently drops two named conjuncts is incomplete on its own terms, even if those two are trivially preserved.

**Required**: Add one sentence noting that L5 and L6 are preserved by the emitted standard-triple value's construction (`(F, G, K)` with `F, G ∈ Endset`), so the set/slot structure invariants hold at `a` by the `Link` type definition.

### Issue 4: R7a Decomposition Example illustrates a case no operation in this note produces

**ASN-0086, R7a Decomposition Example**: a fully worked length-4 K.σ–K.λ–K.σ–K.λ interleaving for `CreateTwoDocsAndLinks`.

**Problem**: The *Corollary (reduction to Emit_K)* establishes that for relational-layer operations "R7a's multi-step branch with K.σ prefix never fires" and "R7a's replay sequence collapses to length 1." The multi-home interleaving the appendix exercises is therefore never produced by any operation in this note's vocabulary; it illustrates the general-substrate-closure reading of R7a only. Given the anti-bloat classifier, a full worked appendix for a path the note's own operations exclude is scope accretion. The interleaving structure is already described inside R7a's proof (discharge (4)(iii)).

**Required**: Either delete the appendix or compress it to the single-sentence observation already present ("The single-fresh-home case is the `n = 1` collapse ... The multi-home interleaving structure that subsumes it is exercised in the appendix"), removing the standalone length-4 walkthrough.

## OUT_OF_SCOPE

### Topic 1: Cardinality/structural bounds on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: The Open Questions raise whether unbounded retraction is permitted. This is a quantitative substrate guarantee not yet specified anywhere upstream; it belongs in a future ASN, not as a correction here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate-level K-operation
**Why out of scope**: Whether the substrate should expose a dedicated retraction operation with an enforced unit-depth shape (vs. the current layer convention) is a design question for a future ASN; the present note correctly scopes it as a layer commitment.

VERDICT: REVISE
