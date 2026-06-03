# Review of ASN-0069

## REVISE

### Issue 1: Verbatim Nelson quote [LM 2/45] reproduced twice
**ASN-0069, §intro ("We are looking for...") and §"Frame: Source Isolation"**: Both sections quote, verbatim, "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45] (the opening adds "This is done by inclusion links.").

**Problem**: The same source quotation is used twice. The "without damaging the originals" clause is the operative phrase for source isolation (V5), and it is already present in the opening occurrence. Re-quoting the full passage in §"Frame: Source Isolation" is the "two paragraphs say the same thing" pattern the anti-bloat pass targets — the reader hits identical text in two structural slots.

**Required**: Keep the full quote at one site; at the second site either drop the block quote and reference the already-established no-damage commitment, or quote only the operative clause not already cited.

### Issue 2: Redundant no-removal restatement after V12
**ASN-0069, §"Permanence Across Source and Fork"**: "There is no operation in the transition vocabulary of ASN-0047 that removes content from `C`, removes entities from `E`, or removes pairs from `R`."

**Problem**: V12 immediately above already cites the operative no-removal foundations inline — (a) T8/P1, (b) P0/S0, (c) P2. This standalone sentence restates the same fact in prose without adding a new consequence, then the following paragraph derives the actual source-fork consequence (neither owner can remove shared content, via V5a). The middle sentence is the redundant slot.

**Required**: Delete the standalone restatement; let V12's per-clause citations stand and proceed directly to the source-fork consequence paragraph.

## OUT_OF_SCOPE

### Topic 1: Concurrent-fork and descendant-enumeration guarantees
**Why out of scope**: The Open Questions already park concurrency-beyond-atomicity and descendant discoverability for future ASNs. The fork operation here is correctly specified against the sequential atomic transition model; these are new territory, not defects.

### Topic 2: Forking a transcludent source (M(d_src) referencing foreign origins)
**Why out of scope**: Listed as an Open Question. The literal-inheritance discipline (V4) and origin-preservation (S7) already make the behavior derivable, but the invariants specific to transclusion chains belong in a later ASN.

VERDICT: REVISE
