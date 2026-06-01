# Review of ASN-0086

I checked the proofs (R0, R0a, L-ContiguousPrefix, R-Scope, R7a, the wp analysis, CoverageEqualityDecidable) and the worked sketch arithmetic. The mathematical content is sound: the freshness arguments, the antichain decomposition into cross-home (zero-counting) and same-home (chain + UL + T3) cases, the wp domain restrictions, and the Step 0–4 tumbler computations all hold. My findings are confined to the meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: R7a motivation is an essay justifying the lemma's retention, not its content
**ASN-0086, paragraph immediately preceding R7a**: "R7a is a substrate *closure* (completeness) result, motivated independently of the relational layer below... This is an auditability guarantee in its own right... The closure is what makes the link store's audit trail (`L_K`) trustworthy as a complete record... So R7a's multi-step, multi-home decomposition is not exercised by any current operation; its value is the closure guarantee itself, retained as a forward-looking completeness statement for any layer that would bundle multiple link emissions, not as machinery the present operation set consumes."

**Problem**: This ~200-word block is meta-prose in a structural slot. The opening one or two sentences state what R7a guarantees (fine); the remainder argues *why the lemma is kept* — "motivated independently," "auditability guarantee in its own right," "what makes the audit trail trustworthy," "not exercised by any current operation," "retained as a forward-looking completeness statement... not... machinery the present operation set consumes." These are precisely the flagged patterns: essay content, use-site inventory, justification-for-existence. The reader must skip past it to reach the lemma. (The embedded udanax-green CREATELINK/LINKFROMSPAN evidence is legitimate implementation content — flag its *framing* as retention-justification, not its existence; move the concrete shape-of-writes fact to where it does work and drop the surrounding "its value is the closure guarantee itself, retained..." apologia.)

**Required**: Reduce to the lemma statement plus, if needed, one sentence of object-level scope. Remove the "why we keep it / not exercised / retained for forward-looking value" justification.

### Issue 2: The "not exercised, retained for closure value" claim is duplicated across two sections that defer to each other
**ASN-0086, Corollary (reduction to Emit_K) proof**: "The relational layer thus instantiates R7a only at `m = 1`; R7a's multi-step, multi-home generality is not exercised here, and is retained for its standalone closure value (motivation above the lemma)."
**and the R7a motivation paragraph**: "...R7a's multi-step, multi-home decomposition is not exercised by any current operation; its value is the closure guarantee itself..."

**Problem**: The same point — R7a's generality is unused and kept for standalone closure value — appears in two places, with the corollary deferring upward ("motivation above the lemma") to the paragraph that already makes the identical claim. This is the flagged "multiple paragraphs in different sections defer to the same downstream/upstream location" pattern, compounded by saying the same thing twice in different words.

**Required**: State the `m = 1` instantiation fact once, at one site. Drop the cross-reference and the second restatement.

### Issue 3: Reduction-corollary proof re-litigates R7a's role instead of citing it
**ASN-0086, Corollary (reduction to Emit_K) proof**: "The reduction itself follows directly from the layer's own *Definition*, with no appeal to R7a's decomposition machinery... R7a contributes the complementary closure guarantee: it certifies the layer admits no *other*, composite route to `Σ.L` — any conforming `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L` is replayable by K-steps — so the enumerated operation set `{Emit_K, Observe_K, Nullify}` is exhaustive of the layer's link-store effects."

**Problem**: After the actual reduction ("the layer's only state-affecting operations are `Emit_K` and its alias `Nullify`, each already a single K.λ `→`-step") the proof spends a further passage narrating what R7a does and does not contribute. This restates Issue 1's "no layer can smuggle an `Σ.L` change past the K-operation contract" in new words and is meta-commentary on the division of labor between the corollary and R7a, not a step of the proof.

**Required**: End the corollary at the reduction itself; if exhaustiveness needs R7a, cite it in one clause rather than re-explaining its guarantee.

## OUT_OF_SCOPE

### Topic 1: Whether the unit-depth retraction discipline should be a substrate-level K-operation
The Open Questions already raise this. The wp Case 2 domain restriction (substrate-conforming *and* unit-depth-disciplined) is correctly handled as a layer commitment here; promoting it to a dedicated retraction K-operation with a shape constraint is new substrate design, belonging in a future ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The note explicitly restricts to standard triples and defers higher-arity projections. This is correctly out of scope.

VERDICT: REVISE
