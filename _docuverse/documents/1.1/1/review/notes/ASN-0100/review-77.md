# Review of ASN-0100

This is a thorough, largely sound specification. The three-effect decomposition, the worked examples, and the per-state/composite-boundary invariant verification all check out under scrutiny — I traced the interior, append, and empty-document examples and the INS.proj instantiation numerically and they are correct. My findings are concentrated where the `review-mode.anti-bloat` classifier points: accreted meta-prose and a corollary that reaches into out-of-scope territory.

## REVISE

### Issue 1: INS.identity.version corollary adds nothing INSERT-specific and reaches into out-of-scope version machinery
**ASN-0100, §Derived corollaries of INS.identity / Claims table (INS.identity.version)**: "When a version `d_v = inc(d_src, 1)` is derived from `d_src` (out of scope here, but a substrate operation under K.δ-IsDocument) and subsequently INSERT is invoked on `d_v`, the freshly allocated `a_k` come from `A_C(d_v)` with `origin(a_k) = d_v ≠ d_src`."
**Problem**: This is INS.alloc with `d := d_v` — `origin(a_k) = d` already holds for *any* target document by INS.alloc, regardless of how the document was created. The "version chain" framing contributes no INSERT-specific content and forces the corollary to stand up version-derivation machinery (`d_v = inc(d_src, 1)`, K.δ-IsDocument) that the Scope explicitly excludes ("Version derivation. INSERT does not create versions"). The parenthetical "(out of scope here, but ...)" is an admission that the carrier reaches past the note's boundary.
**Required**: Remove the corollary, or restate it as a pure instance of INS.alloc without invoking version derivation. INS.identity.crossdoc (which genuinely uses SubAllocatorBundle disjointness) and INS.identity.tightsurv (a distinct value-vs-address consequence) are legitimate; INS.identity.version is not.

### Issue 2: Verbatim repetition of the freshness-boundary parenthetical across sections
**ASN-0100, §Effect One, §Permanence (S0,P0), §S2, §Atomicity (content-allocation invariants, S4), §Provenance (P4★)**: the clause "by SubsequentEmissionFreshness (ASN-0093), with FirstEmissionFreshness covering the boundary case `m_d = 0`" recurs near-verbatim in five separate proof obligations.
**Problem**: Each invariant legitimately consumes freshness, but the boundary-case caveat is re-derived in full each time rather than established once and cited. This is exactly the forward-reference accretion the anti-bloat mode targets — the reader re-parses the same lemma chain at every use site.
**Required**: State the freshness fact once (e.g., at INS.alloc: "each `a_k` is fresh against `dom(C) ∪ dom(L)` at its K.α firing, boundary `m_d = 0` included"), then cite INS.alloc downstream rather than re-citing the two ASN-0093 lemmas with the boundary gloss each time.

### Issue 3: Reviser-drift sentence defends a case the frame trivially discharges
**ASN-0100, §Atomicity (entity-set invariants)**: "for ActivatedEmission, the existential witness for each `e ∈ E` is an activated entity-level sub-allocator `A` with `e ∈ dom(A)`, which by ActivatedEmission's own preservation argument is itself unchanged when no K.δ fires."
**Problem**: With `E' = E` (INS.frame.E) and no transition touching entity-level sub-allocator state, ActivatedEmission inherits by frame like every other entity-set predicate in the same paragraph (P8, NodeLineage, M0). Singling out ActivatedEmission to re-justify its witness "by ActivatedEmission's own preservation argument" is circular padding — it cites the invariant to preserve the invariant and explains machinery the frame already settles.
**Required**: Fold ActivatedEmission into the same one-line frame inheritance as P8/NodeLineage/M0; drop the witness-preservation sentence.

### Issue 4: The INSERT-vs-COPY section is essayistic and partly restates INS.identity
**ASN-0100, §INSERT vs. COPY: Identity Through Allocation**: "Fresh allocation is already fixed by INS.C and INS.alloc (§Effect One) ... The defining structural difference from COPY is captured by INS.identity."
**Problem**: The section opens by conceding its content is "already fixed" upstream, then re-narrates fresh allocation and the "the"-coincidence anecdote before restating INS.identity. The COPY contrast itself is permissible (a statement of what INSERT does not do), but the surrounding restatement of already-established claims is meta-prose the reader must skip to reach the genuine corollaries.
**Required**: Reduce to the one load-bearing sentence (INSERT allocates fresh; COPY references without allocating) and the genuinely derived corollaries; drop the re-narration of INS.C/INS.alloc.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, concurrency serialization, derived-attribute updates
**Why out of scope**: The Open Questions correctly defer K.μ⁺_L insertion semantics, concurrent same-position INSERTs, and document-metadata updates to future ASNs. These are appropriately bounded and need no action.

VERDICT: REVISE
