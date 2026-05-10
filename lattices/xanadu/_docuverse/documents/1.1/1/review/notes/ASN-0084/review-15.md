# Review of ASN-0084

## REVISE

### Issue 1: CanonicalBlockDecomposition uniqueness argument is compressed below proof standard

**ASN-0084, Block Decomposition Transformation section**: "Uniqueness follows from M(d) being a function (S2): for any v ∈ dom(M(d)), there is exactly one maximal block containing v, determined by extending forward from v while M(d)(v + k) = M(d)(v) + k holds, and extending backward symmetrically. Two maximal blocks that share any V-position must be identical (both determined by extension from that shared position), so the maximal blocks partition dom(M(d)) uniquely. The canonical decomposition is the result of exhaustively merging all mergeable pairs in any valid decomposition; the result is independent of merge order."

**Problem**: This passage makes four claims in three sentences, each requiring a distinct argument:

(a) For any v, the maximal block containing v is uniquely determined. The sketch ("extending forward ... and extending backward") is the right idea, but the backward extension is never formally defined — only forward shift is available in the ASN. The argument needs to show that, given v and M(d)(v), the start of the maximal block is uniquely determined by walking backward through predecessors while the correspondence holds.

(b) Two maximal blocks sharing a V-position must be identical. This follows from (a), but only after showing that if b₁ and b₂ overlap at some w, then any position in b₂'s V-extent that lies outside b₁'s can be reached by extending b₁ (since b₂ witnesses the correspondence at that position and the position is in dom(M(d))). This contradicts b₁'s maximality unless b₂ ⊆ b₁, and symmetrically.

(c) Merge-order independence. This requires: (i) exhaustive merging terminates (dom is finite, each merge reduces block count); (ii) at termination, every block is maximal — if some block b were non-maximal, its V-adjacent, I-adjacent neighbor would form a mergeable pair, contradicting exhaustiveness; (iii) the decomposition into maximal blocks is unique by (b); (iv) therefore every termination state is the same.

(d) The equivalence of "maximally merged" and "decomposed into maximal blocks" — two maximal blocks cannot be V-adjacent and I-adjacent (their merge would extend both, contradicting maximality). This underpins (c)(ii) but is not stated.

**Required**: Expand the uniqueness argument to show steps (a)–(d) explicitly. The core argument is roughly one paragraph per step. This is the definition that the worked examples and R-BLK's merge phase depend on.

## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depth m > 2
**Why out of scope**: The ASN restricts to depth 2 throughout and correctly identifies that D-CTG-depth reduces the general case to last-component contiguity. Formally establishing the depth-m version — where ordinals are (m−1)-component tumblers and displacements act on the last component — is new territory, not an error in the depth-2 presentation.

### Topic 2: k-cut rearrangements for k > 4, composition, and block-count bounds
**Why out of scope**: Already identified as open questions in the ASN. The current ASN fully characterizes the 3-cut and 4-cut cases; generalization is future work.

VERDICT: REVISE
