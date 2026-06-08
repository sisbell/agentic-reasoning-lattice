# Review of ASN-0102

## REVISE

### Issue 1: `k` mischaracterized as the M7-maximal block count of the concatenated region

**ASN-0102, "The source designation and its resolution"**: "Second, *the run count `k` is the total number of runs of the concatenated resolution* — the sum over references `k = (+ i : 1 ≤ i ≤ q : k_i)`, where each `k_i` is the maximal-run count of reference `r_i` taken in isolation (C1a, M12 applied per reference) — **the count of blocks maximal under M7's joint V- and I-adjacency merge condition**."

**Problem**: The trailing em-dash clause characterizes `k` as "the count of blocks maximal under M7's joint V- and I-adjacency merge condition." Read as a statement about the laid-down region, this is false — and the ASN's own X8 says so: "Merging the copied blocks among themselves thus yields `≤ k` blocks, with equality exactly when no inter-reference boundary is I-adjacent." So the M7-maximal block count of the concatenated/copied region is `≤ k`, strictly less whenever an inter-reference boundary coalesces (the coalescing worked example exhibits `canonical = k − 1`). `k` is the *sum of per-reference* maximal-run counts, and M7-maximality holds only *per reference in isolation*, not across the concatenation. The sentence's grammar leaves it ambiguous whether the final clause modifies `k` (wrong) or `k_i` (correct), and the wrong reading directly contradicts X8.

**Required**: Scope the M7-maximality explicitly to the per-reference-in-isolation count `k_i`, or drop the redundant trailing clause. The sentence already defines `k` twice (total concatenated runs; `Σ k_i`); the third characterization adds only a precision hazard. Make it unambiguous that the concatenated list is *not* in general M7-maximal as a whole — that fact is exactly what X8 derives.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer displacement-after-copy discoverability, transitive-source containment, and reachability-of-allocator to future ASNs, and are framed as questions rather than claims.)

Notes on the standard checks, for the record: boundary coverage is complete (empty subspace `n_S=0`/`p=1`, append `p=n_S+1`, leading+trailing both present, self-transclusion overlapping the displaced region, cross-origin fragmentation, coalescing copy); the `wp(COPY, S3★)` analysis is non-trivial and correctly reduced to the copied-region membership obligation discharged by C1; X16's three-class tiling of `[1, n_S+W]` is gap- and overlap-free; S2 disjointness across the `s_C`/`s_L` boundary is properly grounded in component-1 distinctness + T3; the J0/J1★/J1'★/P4★/P4a coupling discharge at the composite boundary is sound, including the `Old`/`New` split. No cross-ASN references outside the foundation set. Nelson/Gregory primary-source groundings are load-bearing attribution and should be retained.

VERDICT: REVISE
