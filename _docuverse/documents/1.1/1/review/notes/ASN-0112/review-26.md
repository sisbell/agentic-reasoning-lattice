# Review of ASN-0112

## REVISE

### Issue 1: wp exhaustiveness rests on an uncited foundation fact
**ASN-0112, "Preconditions and well-definedness"**: "The two directions exhaust the cases (an arrangement occupies zero, one, or two subspaces), so the single-subspace condition is both necessary and sufficient, hence the *weakest* precondition."
**Problem**: The exhaustiveness of "zero, one, or two subspaces" is the load-bearing step that makes this a *weakest* precondition rather than merely a sufficient one. It depends on there being no third subspace — i.e., every occupied V-position carries `subspace = s_C` or `s_L`. That is ASN-0047's S3★-aux (SubspaceExhaustiveness), which is *not* among the foundation facts enumerated in "The substrate we measure" and is not cited here. SubspaceConventionAxiom (cited elsewhere for `s_C=1, s_L=2`) fixes the identifiers but does not assert exhaustiveness. The same unstated assumption underwrites V6 ("span more than one subspace") and the V5/V6 dichotomy.
**Required**: Add S3★-aux to the cited substrate facts and invoke it at the wp case-split (and at the V5/V6 dichotomy) to close the "only two subspaces" gap.

### Issue 2: V17 restates V2's positivity and carries provenance bookkeeping
**ASN-0112, V17**: "the extent is *strictly positive* and the span non-empty (TA-strict) — `reach_d > origin_d` always, so the extent is never zero, negative, or degenerate (T12 legality is V2's, cited not re-derived)."
**Problem**: V2 already establishes `Pos(extent_d)` (extent is a positive tumbler) and `reach_d > max O(d) ≥ origin_d`. V17's "strictly positive / never zero / never degenerate" is the same fact in different words. The genuinely new content is the implementation grounding (deletions driving intermediate displacements negative, root width recomputed as a non-negative max-minus-min). The parenthetical "(T12 legality is V2's, cited not re-derived)" is provenance bookkeeping — exactly the meta-prose a precise reader skips past.
**Required**: Reduce V17 to its non-redundant content (the implementation non-negativity grounding); drop the restatement of V2's positivity and the citation-bookkeeping parenthetical.

### Issue 3: V7 promotes foundation span-convexity to a standalone query claim
**ASN-0112, V7**: "the result is always one convex region; fragmentation is unrepresentable in a single span, so a multi-subspace document is reported by enclosure rather than by exact decomposition."
**Problem**: Convexity of `⟦σ⟧` is ASN-0053 S0, and "reported by enclosure" is already V6's conclusion. V7 is the *explanation* for V6 elevated to its own numbered invariant; it introduces no query-specific state, operation, or invariant beyond (foundation convexity) + (V6). As a standalone claim it reads as accreted restatement.
**Required**: Fold V7's reasoning into V6's justification (citing ASN-0053 S0 for convexity) rather than carrying it as a separate claim, or state explicitly what query-specific invariant V7 adds beyond V6 + S0.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-count invariant
The first Open Question (relating reported extent to occupied-position count when the inter-subspace void intervenes) is correctly posed as future work; the single-subspace coincidence is settled by V5. No action needed.

VERDICT: REVISE
