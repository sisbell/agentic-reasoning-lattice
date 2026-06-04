# Review of ASN-0099

## REVISE

### Issue 1: Implementation-significance essay in a claim slot (and scope drift)
**ASN-0099, F19 (ResultSetMonotonicity)**: "F19 (and its filtered/scoped instances under F15(c)) is the load-bearing consequence behind any indexed implementation's promise: an index that mirrors `findlinks` is never required to remove entries as the state evolves, only to add them."
**Problem**: This sentence explains F19's downstream *significance for indexed implementations* rather than advancing the formal argument — exactly the implementation-rationale meta-prose the anti-bloat pass targets. It also drifts into indexing/caching, which the ASN's own "What We Have Not Specified" list explicitly excludes ("Caching"). The formal content of F19 (monotonicity, derived in one line from F11) stands without it.
**Required**: Delete the sentence, or reduce to the monotonicity statement. Do not editorialize about index maintenance.

### Issue 2: Defensive realizability/exhaustiveness preamble on F4
**ASN-0099, F4 (MatchIndividuation)**: "The endset shapes are L3-admissible (slot 3 a non-empty type endset, non-type slots possibly empty, with coverage(∅) = ∅) and each I-set is a query parameter (L4 places no constraint on span addresses), so every witness arises by a K.λ allocation under any document."
**Problem**: This is a defensive realizability/exhaustiveness justification appended to the individuation framing. The individuation argument is carried entirely by the per-witness disagreement checks in the strengthenings/weakenings that follow; the "every witness arises by a K.λ allocation" clause is the kind of reachability reassurance the anti-bloat pass flags as noise the precise reader must skip to reach the actual witnesses.
**Required**: Compress to at most a short clause asserting the witnesses are L3-admissible states, or cut entirely and let each witness's stated shape carry it.

### Issue 3: Redundant open question restating F9/A1a
**ASN-0099, Open Questions (third)**: "What is the minimum structural commitment any conforming substrate must make to the link-store-inert fragment of its operation vocabulary in order to support link-discovery invariance under those operations?"
**Problem**: F9 + A1a already answer this for the operative vocabulary — the commitment is publishing `L' = L` across `V ∖ {K.λ}`. Posing it as an open question reads as a deferral to content the ASN has already settled, the kind of duplicate-deferral accretion the anti-bloat pass names.
**Required**: Drop the question, or reframe it to point at the genuinely unresolved part (e.g., substrates whose vocabulary is not yet fixed), distinct from what F9 establishes.

## OUT_OF_SCOPE

None. The ASN correctly confines INSERT/DELETE/COPY/version/replication to its scope list and does not introduce claims for them; FOLLOWLINK/RETRIEVEENDSETS and combined filtered-scoped forms are explicitly named as future work, not specified here.

VERDICT: REVISE
