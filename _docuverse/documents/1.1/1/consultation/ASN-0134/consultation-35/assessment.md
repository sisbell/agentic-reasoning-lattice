# Channel Assignment — ASN-0134 review-35

**Date:** 2026-06-14 09:25

## Issue 1: The m=0 / m=1 degenerate-batch atomicity is stated three times
Reason: Pure deduplication of a fact already fully established in the note — the `m ≥ 2` boundary and the degenerate `m=0`/`m=1` cases are stated outright; consolidating them into A5 and shrinking A1/the table needs no design intent or implementation evidence.

## Issue 2: A6 is a single monster paragraph carrying defensive justification of its own package composition
Reason: Both parts are internal — (a) trimming package-composition apologetics is editorial, and (b) the M1-independence point rests on facts already in the ASN (per-state `C2`/`L1a` constrain only content-hosting documents; no `→_sh` step removes a document per ASN-0093's `M1`), so restating the independence in one sentence without the imagined childless-removal scenario draws only on the note's own invariants.

## Issue 3: Repeated cross-section deferrals and an intro that previews §8/§9 as an abstract
Reason: Deduplicating the OQ5/OQ9 deferrals and cutting the intro's §8/§9 preview are editorial restructuring; all referenced content already lives in the ASN.

## Issue 4: The "cross-doc cross-subspace pair CrossDocumentDisjointness leaves unnamed" observation is repeated across H0, H1, W1 — and inside H1 itself
Reason: The absorption argument is accepted as correct, so saying it once in H1 and citing it from H0/W1 is pure deduplication; the foundation-lemma scope (what `CrossDocumentDisjointness`/`DisjointSubAllocatorChains` name) is a sibling-note fact the ASN already characterizes, not a Nelson/Gregory matter.

## Issue 5: §9 and G0 carry essays justifying what the contract omits and why a non-load-bearing clause is kept
Reason: Trimming the "conspicuous by what they omit" inventory, the clause-6 defense, and G0's "not an oversight" line while retaining the drop-one minimality list is editorial; no claim changes.

## Issue 6: §4 instance (i) buries a load-bearing lemma (I1a literal-vs-operative) under editorial framing and restates its conclusion
Reason: The literal-vs-operative divergence is already fully derived in instance (i) and accepted as correct, so promoting it to a named result and stripping the connective prose is reorganization, not re-derivation; the quoted I1a clause and induction step come from the sibling dependency ASN-0128, which is the author's own context rather than the design-intent or implementation channels.

## Issue 7: "stale is ... never single-index" is false at the empty-active-slice boundary
Reason: The correction follows from the note's own decomposition of `stale` (one active-view `Observe_K` plus one frontier descent per member home) — at `N=0` the active slice is empty, so zero frontier descents leave a single read — and the analogous single-type-join boundary is the same arithmetic; applying the stated structure to the degenerate case is internal.
