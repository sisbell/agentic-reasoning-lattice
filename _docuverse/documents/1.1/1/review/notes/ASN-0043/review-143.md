# Review of ASN-0043

I worked through the foundation citations, the FSP/FSE/L9/L11b proof chain, PrefixSpanCoverage, and verified the worked example's arithmetic (chains, coverages, disjointness, interval unions) end to end. The mathematical content is sound — the L1c chains, the `[g,g') ∪ [g',h) = [g,h)` coverage equality in Step 6, and the sibling-cone disjointness in Step 4 all check. My findings are confined to accreted/misordered prose, which the anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: L1a previews L2's endset-independence claim — duplicated reasoning across two sections
**ASN-0043, L1a (LinkScopedAllocation)**: "The allocation prefix is determined by the document parameter — a document that must already exist for `docreatelink` to be called — not by the endsets; a link whose endsets reference entirely foreign content is still allocated under the creating document's prefix."
**Problem**: L1a's actual claim is the membership invariant `home(a) ∈ dom(Σ.M)`. The quoted closing sentence does not advance that claim — it asserts that the home/allocation prefix is independent of the endsets, which is precisely the content of L2 (OwnershipEndsetIndependence): "The home document of a link is determined entirely by the link's address and is independent of the link's endsets." Two paragraphs in different sections now make the same not-by-the-endsets point in different words. This is the duplication pattern the anti-bloat mandate flags.
**Required**: Drop the endset-independence preview from L1a (keep only the allocation-under-document-prefix evidence that supports `home(a) ∈ dom(Σ.M)`); let L2 carry the endset-independence statement.

### Issue 2: Worked-example verification is misordered — a check invokes a result established below it
**ASN-0043, Worked Example**: the D-SEQ check reads "a contiguous arithmetic sequence of element-field tumblers at depth 2, **starting at the D-MIN witness `[1, 1]`** and advancing by `inc(·, 0)`", but the D-MIN check (`min(V_1(d)) = [1, 1]`) is verified *after* D-SEQ, not before.
**Problem**: The example uses D-MIN's conclusion to discharge D-SEQ while D-MIN is still unverified, presenting a forward dependency that the reader must resolve by jumping ahead. The disorder is broader: L8 (reflexivity) and L9 (ghost disjointness) are detached from the other L-checks and dropped in among the ASN-0036 S-checks, and the S-block itself runs S3, S7a/b/d, S8a, S8-depth, D-CTG, D-SEQ, D-MIN, then loops back to S2 and S8-fin at the very end. A precise reader has to hunt for each check rather than read top to bottom.
**Required**: Reorder so D-MIN precedes D-SEQ (since D-SEQ cites the D-MIN witness), and group the L-invariant checks together and the S-invariant checks together in a consistent order.

## OUT_OF_SCOPE

### Topic 1: Disjointness over the full content store rather than the `s_C`-resident slice
The ASN scopes `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` to `s_C`-resident states and lists the global-content-subspace question in Open Questions. Extending disjointness to all of `dom(Σ.C)` requires a content-side global subspace invariant, which belongs in a content-side ASN, not here.

VERDICT: REVISE
