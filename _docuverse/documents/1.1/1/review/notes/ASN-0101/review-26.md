# Review of ASN-0101

## REVISE

### Issue 1: K.μ~ unavailability analysis ignores clause (v) (link-subspace fixing), giving a wrong "killer case" characterization

**ASN-0101, "The operation" section (second obstacle)**: "(ii) A link-subspace interior deletion is blocked whenever `M(d)|_{dom_C}` has fewer than two distinct values — covering `|V_{s_C}(d)| ∈ {0, 1}` as well as the shared-single-value configuration with `|V_{s_C}(d)| ≥ 2`. The genuine killer case for the K.μ~-then-K.μ⁻ composite-substitute strategy is therefore: an interior deletion (in either subspace) on a document whose content-subspace arrangement `M(d)|_{dom_C}` takes fewer than two distinct image values."

**Problem**: The analysis gates composite availability solely on K.μ~'s *precondition* (content subspace ≥ 2 distinct values), but overlooks K.μ~'s admissibility clause (v) — *link-subspace fixing*: `(A v ∈ dom_L(M(d)) :: π(v) = v)` (ASN-0047, K.μ~). Clause (v) forbids K.μ~ from relocating *any* link-subspace V-position. The composite-substitute strategy for an interior deletion requires K.μ~ to "move the to-be-deleted I-addresses to the suffix of `V_S(d)`"; for `S = s_L` this is structurally impossible regardless of the content subspace, because no admissible π can move a link position. Consequently:

- A link-subspace interior deletion is unavailable via the composite in **all** configurations, not merely when `M(d)|_{dom_C}` has fewer than two distinct values.
- The conclusion "the genuine killer case ... is an interior deletion (in either subspace) on a document whose content-subspace arrangement takes fewer than two distinct image values" is false for the link subspace: a link interior deletion with content `≥ 2` distinct values is *also* a killer case, yet the conclusion (by parallel with case (i)'s explicit "the composite is available ... in that case") implies such a configuration is composite-realisable.
- The obstacle-1 paragraph inherits the same defect: "one could in principle apply K.μ~ with an admissible permutation that moves the to-be-deleted I-addresses to the suffix of `V_S(d)`" silently assumes π can permute subspace-`S` positions, which fails for `S = s_L`.

**Required**: Correct case (ii) and the killer-case conclusion to record that, by clause (v), a link-subspace *interior* deletion is unconditionally unavailable via the K.μ~-then-K.μ⁻ composite (independent of the content-subspace value count) — and restrict the obstacle-1 "one could in principle" strategy to `S = s_C`. This strengthens, rather than weakens, the motivation for DEL as an atomic primitive, but the current value-count characterization of when the composite is unavailable is incomplete/incorrect for the link subspace.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
