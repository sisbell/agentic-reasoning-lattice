# Review of ASN-0082

## REVISE

### Issue 1: Notational inconsistency — "w > 0" vs Pos(w)
**ASN-0082, Post-Contraction Shift, Contraction formal contract**: "w > 0 — the contraction width is positive."
**Problem**: The foundation (ASN-0034, ASN-0053) uses Pos(w) (TA-Pos) for tumbler positivity. "0" is not a tumbler in T, so the comparison "w > 0" is not directly defined under T1. The notation appears repeatedly in the contraction section, including in OrdinalDisplacementProjection's restatement "When `w > 0` (TA-Pos), `w_ord > 0`" — which mixes the informal `>` notation with the foundation's Pos predicate within the same sentence. The cited foundation OrdinalDisplacementProjection itself uses `Pos(w)`.
**Required**: Replace "w > 0" with Pos(w) (or "w is positive" in prose) throughout the contraction section. Same fix for "w_ord > 0" derivations.

### Issue 2: Missing cross-subspace worked example for contraction
**ASN-0082, Post-Contraction Shift, Worked Example**: All four worked examples for contraction (standard, L = ∅, R = ∅, full deletion) operate on a document with only text-subspace positions.
**Problem**: The insertion section devotes substantial space to a cross-subspace example exercising I3-X with a sparse link subspace V_2(d) = {[2,5], [2,9]}, demonstrating that text insertion leaves the link subspace verbatim. The contraction section provides no parallel example exercising D-CS. D-CS is a key frame condition asserting per-subspace domain equality AND mapping equality across non-S subspaces — without a concrete example, the reader cannot easily verify the contraction's promise that link-subspace tombstones remain intact through a text contraction.
**Required**: Add a worked contraction example with both text and link subspaces present (e.g., V_1(d) ∪ V_2(d) with V_2(d) sparse), showing explicit verification of D-CS over the link positions through a text contraction.

### Issue 3: Terse proof of D-SEP(b)
**ASN-0082, D-SEP — GapClosure, Proof of (b)**: "Either v = r, so r ∈ V_S(d) directly, or v > r, in which case the last element of X (with ordinal ord(p) + c − 1) is in V_S(d), and v ∈ V_S(d) with v > r > last element of X, so D-CTG gives r ∈ V_S(d)."
**Problem**: The proof asserts that X has a last element of ordinal p₂ + c − 1 without showing the chain: (i) p ∈ X since p ≥ p and p < r (the latter from Pos(w) and TA-strict), so X is non-empty; (ii) by D-SEQ on V_1(d), X = {[1, k] : p₂ ≤ k < p₂ + c} (which has c ≥ 1 elements since Pos(w) implies w_2 ≥ 1); (iii) the last element under T1 is [1, p₂ + c − 1]; (iv) [1, p₂ + c − 1] < r since p₂ + c − 1 < p₂ + c. Each step is mechanical but none is stated.
**Required**: Walk the reader through the chain explicitly, citing D-SEQ for the form of X, justifying X's non-emptiness, and identifying the last element.

### Issue 4: D-CTG-post proof cites D-CTG where D-SEQ suffices
**ASN-0082, D-CTG-post proof**: "L consists of positions with ordinals strictly less than ord(p) — by D-CTG on the pre-state, L = {[1, k] : 1 ≤ k < p₂}, which is contiguous."
**Problem**: D-CTG asserts contiguity but does not give the explicit form `{[1, k] : 1 ≤ k ≤ N}`; that explicit form comes from D-SEQ. The same proof later writes "R = {[1, k] : p₂ + c ≤ k ≤ N}" without any citation, even though this form also derives from D-SEQ. The citation should be uniform and precise.
**Required**: Cite D-SEQ (not D-CTG) for the explicit forms of L, X, R, and the post-state V_1(d').

### Issue 5: Introduction undersells the ASN's scope
**ASN-0082, opening paragraph**: "This ASN extends ASN-0053 (Span Algebra) with the post-insertion shift property..."
**Problem**: The introduction describes only the post-insertion property, but roughly half the ASN develops post-contraction shift in equal depth (D-SHIFT, D-BJ, D-SEP, D-DP, and nine preservation lemmas). A reader of the introduction would not anticipate the contraction analysis.
**Required**: Update the opening to mention both the post-insertion and post-contraction shift properties.

### Issue 6: I3-VP wp analysis claims to be a worked example but the others are merely promised
**ASN-0082, Post-Insertion Shift, wp analysis**: "This wp-style derivation generalizes... The reader can verify the remaining cases by the same recipe — we present only I3-VP here as the worked example."
**Problem**: Reading I3-VD, I3-S3, I3-S2, and I3-fin, several of them have non-trivial preconditions worth surfacing via wp. I3-S2 (functionality) in particular depends on the consistency check's pairwise disjointness argument — the wp of "M'(d) is a function" backwards through the four assignment statements would expose exactly why TS2's injectivity is needed and where subspace preservation enters. The standards say wp analysis should hit a non-trivial case; I3-VP is non-trivial but is the easiest of the post-state lemmas. The "by the same recipe" hand-wave skips the more illuminating cases.
**Required**: Either (a) extend the wp analysis to at least one more non-trivial case (I3-S2 is the natural candidate), or (b) excise the claim that the recipe generalizes and present I3-VP as a representative example, dropping the promise.

## OUT_OF_SCOPE

### Topic 1: Contraction at depths greater than 2
The depth scoping axiom #p = 2 is structurally justified via TA4's zero-prefix precondition interacting with S8a's componentwise positivity. The open question on generalization is honestly recorded. The ASN's structural-necessity argument is sound (verified: at depth 3 with w_ord having actionPoint at the deepest position, the round-trip (a ⊕ w_ord) ⊖ w_ord ≠ a because TumblerSub's ZPD finds disagreement at position 1, not at the action point). Generalization belongs in a future ASN that either strengthens TA4 or develops an alternative partial-inverse identity.

### Topic 2: Span-level lemma for contraction
I3-S provides a span-level postcondition for insertion. A natural counterpart for contraction — characterizing how spans within the contracted, vacated, or shifted regions transform under contraction — is not included. Appropriate for a follow-up ASN composing span algebra with contraction.

### Topic 3: Composition with full INSERT and DELETE operations
The ASN explicitly scopes itself to the shift sub-operations and defers content placement (which would weaken I3-C to S0 to permit n new I-addresses) and full operation composition. The scoping discipline here is appropriate.

### Topic 4: Link-subspace mutation
The text-subspace restriction is consistent with the foundation's D-CTG, D-MIN, D-SEQ frame note. Link-subspace mutation (presumably via tombstoning rather than shift-to-close-gap) is correctly deferred to a future ASN.

### Topic 5: External-state V-position reference updating
The first open question — "what must the system provide to allow that reference to be updated after a shift" — is not addressed and belongs in an ASN on durable external addresses (e.g., links from other documents into a document undergoing insertion/contraction).

VERDICT: REVISE
