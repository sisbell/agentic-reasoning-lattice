## Question 10 [theory]

> What is the design's guarantee regarding the symmetry of this operation — must comparing document A to document B yield a result related to comparing B to A?

# Symmetry of SHOWRELATIONOF2VERSIONS

Nelson does not state a formal symmetry guarantee for this operation explicitly. However, the design implies symmetry through two structural facts:

**1. Correspondence itself is symmetric.** Correspondence is structural, defined by shared Istream origin — if Vstream position X in document A maps to the same Istream address as Vstream position Y in document B, then the relation holds equally in either direction. From `correspondence.md`:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages." (4/53)

And links can traverse correspondence refractively from either side:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

**2. The operation returns *ordered* pairs.** From the FEBE specification:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

Because the result is *ordered* pairs (first element from first spec-set, second from second), swapping the arguments swaps the pair ordering. So:

- `SHOWRELATIONOF2VERSIONS(A, B)` returns `[(a₁,b₁), (a₂,b₂), ...]`
- `SHOWRELATIONOF2VERSIONS(B, A)` returns `[(b₁,a₁), (b₂,a₂), ...]`

**The guarantee, then, is content-symmetric but representation-ordered:** the set of corresponding span-pairs is the same in either direction, but each pair is transposed. The truth about what corresponds to what does not depend on argument order; only how that truth is presented does.

This follows necessarily from the principle that correspondence is a structural property of shared Istream origin, not an asymmetric operation over the arguments. The user can "scroll through any two versions to see corresponding parts" (2/21) — and which side is "left" versus "right" is a presentation choice, not a semantic one.

NEED_RAW: 4/70 — to confirm whether Nelson states any explicit symmetry property of the operation beyond "ordered pairs."
