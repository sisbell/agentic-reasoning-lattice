# Review of ASN-0084

This ASN is unusually rigorous: five worked examples exercise distinct sub-cases, the permutation/well-definedness lemmas are complete, and R-CANON's maximality argument is sound in both directions. The verbatim arithmetic in the examples checks out. My findings are confined to the forward-reference accretion the note's classifier flags, plus scope observations.

## REVISE

### Issue 1: Procedural bookkeeping sentence in R-BLK adds no reasoning
**ASN-0084, R-BLK, "Same-region discharge of the commutation identity"**: "Having discharged its applicability once here, we consume this identity in the conclusions below without re-justifying it."

**Problem**: The sentence is pure proof-bookkeeping — it tells the reader how the rest of the lemma will reuse R-COMM rather than advancing any claim. The preceding two sentences already establish that every post-split run satisfies R-COMM's same-region precondition; the conclusions below simply cite the identity where used. The reader must skip past this to follow the argument.

**Required**: Delete the sentence. The substantive content (R-COMM applies to every post-split run) is fully carried by the prior two sentences.

### Issue 2: I-start claim duplicates the S8-cons derivation it forward-references
**ASN-0084, R-BLK, "I-start, width, and contiguity of reassembled runs"**: "Its I-start is aⱼ by the permutation defining property M'(d)(π(vⱼ)) = M(d)(vⱼ) = aⱼ (the k = 0 instance of the S8-cons derivation that follows)."

**Problem**: This states a fact, labels it "the k = 0 instance of the S8-cons derivation that follows," and the following paragraph then derives the general case `M'(d)(π(vⱼ) + k) = ... = aⱼ + k` whose `k = 0` instance is exactly this I-start claim. One paragraph asserts a special case with a forward pointer; the next proves the general case. This is the forward-deferral / same-content-twice pattern the classifier targets.

**Required**: Either derive S8-cons first (general `k`) and read off the I-start (`k = 0`) as a corollary, or drop the parenthetical forward pointer and let the I-start claim stand on the permutation defining property alone without gesturing at a downstream derivation.

## OUT_OF_SCOPE

### Topic 1: Text subspace at depth m₁ > 2
**Why out of scope**: The depth-2 restriction is load-bearing for the singleton-tumbler-to-ℕ identification that underlies all the width/displacement arithmetic. D-SEQ guarantees the sequential structure at any depth (positions vary only in the last component), so generalization is feasible by treating the last component as the ordinal — but it requires reworking the arithmetic apparatus, which is a separate ASN, not a defect here. Worth noting: R-CANON already operates at general depth `m` to accommodate pass-through non-S runs, so the machinery is partly depth-agnostic already.

### Topic 2: k > 4 cut rearrangements and composition of rearrangements
**Why out of scope**: The ASN's own Open Questions correctly identify these as future territory. Generalizing the pivot/swap to k-cut rearrangements and characterizing the closure of REARRANGE under composition is new content, not a gap in the 3-/4-cut treatment given here.

VERDICT: REVISE
