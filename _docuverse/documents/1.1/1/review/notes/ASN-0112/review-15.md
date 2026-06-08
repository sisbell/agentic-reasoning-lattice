# Review of ASN-0112

## REVISE

### Issue 1: Reach biconditional stated twice in succession, wrapped in distinctness meta-commentary
**ASN-0112, "The bounding span and its two endpoints" (V2)**: The paragraph first writes "with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`," then a few sentences later restates it in full: "The reach biconditional is that the reach equals `reach_d` exactly when `#origin_d ≤ #reach_d`: `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`." It then adds "This is an endpoint condition, genuinely distinct from span level-uniformity, and the two point opposite ways..."
**Problem**: The same biconditional is asserted twice within one paragraph, and the trailing clauses ("genuinely distinct," "point opposite ways") are meta-commentary about a terminological distinction rather than reasoning that advances the covering claim — which the paragraph itself proves *unconditionally*. The level-uniform/level-compatible distinction governs only the `m_C ≠ m_L` regime, which the ASN elsewhere states the implementation never realizes (`m_C = m_L`, Q2).
**Required**: State the reach biconditional once. Drop the "genuinely distinct / point opposite ways" framing; retain only the bare arithmetic fact (`σ_d` level-uniform iff `#origin_d ≥ #reach_d`) if it is load-bearing downstream, otherwise cut it.

### Issue 2: V17 closing sentence is a defensive non-dependency that defers to V2
**ASN-0112, "The extent is a well-formed, non-negative displacement" (V17)**: "V17's `Pos` and `actionPoint` claims hold without any endpoint depth relation (established in the V2 well-formedness paragraph via D0); T12 legality is therefore independent of the endpoint depth relation the V2 reach biconditional governs."
**Problem**: This sentence advances no reasoning — it restates that V17 does not depend on the biconditional and points back to V2. It is the "defensive justification deferring to a downstream/upstream location" pattern. V17's proof already establishes its claims via D0; the reminder that it doesn't use the biconditional is noise the reader must skip.
**Required**: Delete the sentence. V17's own derivation suffices.

### Issue 3: Authorization digression in the precondition section is essay content in a structural slot
**ASN-0112, "Preconditions and well-definedness"**: After stating the single precondition, the section adds a paragraph: "This single precondition is all the value semantics require. The abstract state ... carries no session, caller identity, or read-entitlement component ... Gregory's implementation does gate the operation on the document being open in the caller's session (a BERT check), failing the request otherwise ... We note it as an observation and leave authorization to a separate treatment; it forms no part of the precondition for the value this ASN specifies."
**Problem**: This is defensive prose explaining why something is *absent* from the precondition rather than advancing the spec. The closing clause ("forms no part of the precondition") restates the opening ("all the value semantics require") — the same point in different words. The BERT/session detail is implementation mechanics that the model cannot express, by the paragraph's own admission.
**Required**: Reduce to at most one sentence noting authorization is a deployment-level concern outside the value semantics. Cut the restatement and the BERT detail.

## OUT_OF_SCOPE

### Topic 1: Per-subspace exact extent recovery (span-set)
**Why out of scope**: The first open question (recovering per-subspace extents via a span-set) is correctly deferred to RETRIEVEDOCVSPANSET / ASN-0113. V7 establishes the single-span limitation cleanly; the multi-span operation belongs elsewhere.

### Topic 2: Historical-version reporting and out-of-range editing artifacts
**Why out of scope**: The open questions on designated-version faithfulness and addressing arithmetic driven outside the well-formed range are genuinely new territory, not gaps in this query's specification.

VERDICT: REVISE
