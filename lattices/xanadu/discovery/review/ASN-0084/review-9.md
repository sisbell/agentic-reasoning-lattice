# Review of ASN-0084

## REVISE

### Issue 1: Commutativity of π with ordinal shift is proved but not labeled
**ASN-0084, Block Decomposition Transformation (R-BLK)**: "first uses the commutativity π(vⱼ + k) = π(vⱼ) + k"
**Problem**: The property π(v + k) = π(v) + k — for v and v + k in the same region, 0 ≤ k < block width — is proved by explicit case analysis across all region types in R-BLK's "*Proof (commutativity)*" section, but receives no standalone label and does not appear in the Properties Introduced table. This is the key structural property enabling R-BLK's B3 verification: it says the permutation commutes with ordinal shift within each region, which is exactly what makes blocks transform cleanly (V-start displaced, I-start and width preserved). It is independently significant and will be needed by any future ASN that reasons about how correspondence runs behave under rearrangement.
**Required**: Promote the commutativity to a labeled lemma (e.g., R-COMM) with its own preconditions (v and v + k lie in the same region after Phase 1 splitting) and postcondition (π(v + k) = π(v) + k). Add R-COMM to the Properties Introduced table. R-BLK's B3 derivation should cite R-COMM by label rather than inlining the proof.

### Issue 2: Invariant preservation paragraph derives S2 from forward-referenced specific proofs
**ASN-0084, State and Vocabulary (Invariant preservation)**: "Together with R-RI (S3), the well-definedness lemmas R-PIV/R-SWP (S2), and C' = C (S0, S1, S7a, S7b, S7c...), every ASN-0036 invariant is maintained by an arrangement rearrangement."
**Problem**: The paragraph establishes invariant preservation for "an arrangement rearrangement" — the abstract class defined three paragraphs earlier. But it derives S2 (arrangement functionality) by forward-referencing R-PIV and R-SWP, which are specific to the pivot and swap postconditions and appear much later in the ASN. For the abstract class, S2 follows directly from the bijectivity of π: each u ∈ dom(M'(d)) equals π(v) for exactly one v (bijectivity on dom(M(d)) = dom(M'(d))), so M'(d)(u) = M(d)(v) is uniquely determined — no forward reference needed. R-PIV/R-SWP then serve their actual purpose later: verifying that the specific pivot and swap postconditions define total functions, which is one step in showing they constitute arrangement rearrangements.
**Required**: In the invariant preservation paragraph, derive S2 from the bijectivity of π (one sentence: "S2 holds because each u ∈ dom(M'(d)) has u = π(v) for exactly one v, so M'(d)(u) = M(d)(v) is uniquely determined"). Remove the R-PIV/R-SWP citation from this paragraph.

## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depth > 2
**Why out of scope**: The ASN explicitly restricts to depth-2 V-positions and notes that generalization is "structurally identical by D-CTG-depth." Formalizing the general case is future work; the depth-2 restriction is a stated scope choice.

### Topic 2: k-cut rearrangements for k > 4
**Why out of scope**: The open questions correctly identify this as future work. The 3-cut and 4-cut forms cover the two natural cases (adjacent and non-adjacent region transposition).

### Topic 3: Composition of rearrangements
**Why out of scope**: Whether the composition of two rearrangements is expressible as a single rearrangement is a natural algebraic question for a future ASN on rearrangement group structure.

VERDICT: REVISE
