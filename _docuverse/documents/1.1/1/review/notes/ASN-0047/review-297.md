# Review of ASN-0047

## REVISE

### Issue 1: J4 fork claims K.δ leaves M unchanged, contradicting K.δ's own Document effect
**ASN-0047, J4 (Fork composite), *Discharge of arrangement-side invariants* → "Link-subspace clearance via K.δ initialisation"**: "Step (i)'s K.δ event places `d_new` into `E_doc` while leaving M unchanged (`M' = M`); since `d_new ∉ E` before the step, `M(d_new) = ∅` by the totality convention holds at the intermediate state Σ_post-K.δ..."

**Problem**: K.δ's own frame, in the *Elementary transitions* / *K.δ* definition, splits on the level of `e` and states for `Document(e)`: "`dom(M') = dom(M) ∪ {e}` with `M'(e) = ∅`". So the K.δ step that creates `d_new` (a document) *does* change M — it registers `d_new ∈ dom(M) = E_doc` with the empty arrangement. The parenthetical "leaving M unchanged (`M' = M`)" is false, and the appeal to the totality convention ("`M(d_new) = ∅` by the totality convention") is the wrong justification: `M'(d_new) = ∅` is an *explicit effect* of the K.δ Document case, not a default-value fallthrough. The discriminator note in *The state model* even warns "`M(d) = ∅` does not signal allocation status — a freshly registered document also has `M(d) = ∅`," so leaning on the convention here is exactly the conflation that note forbids.

**Required**: Replace "leaving M unchanged (`M' = M`)" with the actual K.δ Document effect — K.δ registers `d_new` into `dom(M) = E_doc` with `M'(d_new) = ∅` — and derive `dom(M(d_new)) = ∅ ⟹ V_{s_L}(d_new) = ∅` from that explicit effect rather than from the totality convention.

### Issue 2: Temporal-scope (per-state vs composite-boundary) distinction stated three times in full
**ASN-0047, *ExtendedReachableStateInvariants* definition, the *Extended reachable-state invariants* section preamble, and the *Proof* preamble**: The same two-class distinction — per-state invariants hold at every elementary target including intermediate states; composite-boundary properties hold only at boundaries and may transiently fail — is given in full prose in the ExtendedReachableStateInvariants box ("*Per-state invariants*... *Composite-boundary properties*..."), then again as a two-bullet exposition in the section preamble ("*Per-state invariants* hold at **every** reachable state... *Composite-boundary properties* hold only at *composite boundaries*..."), then again in the Proof preamble ("The two temporal-scope classes of the preamble above carry different obligations...").

**Problem**: The note carries `review-mode.anti-bloat`; this is the flagged pattern "two paragraphs in the same document say the same thing in different words," compounded to three. A reader following the argument re-encounters the same conceptual setup at each section boundary and must verify it adds nothing new each time.

**Required**: State the distinction once (the section preamble is the natural home, since it drives the induction-variable choice) and have the other two sites point to it rather than re-explain it.

### Issue 3: S8★ per-subspace discharge duplicated between its definition and the Class (a) prose
**ASN-0047, *S8★* definition (Amendments section) and the *S8★* paragraph under the Class (a) matrix**: The S8★ definition already gives the full two-route discharge — content subspace via ASN-0036's S8 on `M(d)|_{V_{s_C}(d)}` (with the OrdShiftHom shift-closure step), link subspace via the trivial length-1 decomposition under the `shift(t,0):=t` convention. The Class (a) *S8★* prose then restates the same two routes ("Established per-subspace by the two routes specified at S8★'s definition... *Content subspace:* ...reapplying ASN-0036's S8... *Link subspace:* ...the trivial length-1 decomposition...").

**Problem**: Same anti-bloat duplication pattern. The matrix preamble declares the matrix "a navigational index; each cell summarises the load-bearing argument," yet the trailing prose re-derives content the definition already carries, rather than adding the per-transition preservation step (which is the only thing the Class (a) discharge owes beyond the definition).

**Required**: In the Class (a) S8★ paragraph, keep only the per-transition *preservation* deltas (what K.μ⁺ / K.μ⁺_L / K.μ⁻ / K.μ~ each do to the projections) and cite the S8★ definition for the two-route construction instead of re-stating it.

### Issue 4: NodeRootedForest carries a global use-site justification rather than asserting its structure
**ASN-0047, *NodeRootedForest* (Derived structure — scope of GlobalUniqueness)**: "Consequently **every 'plain GlobalUniqueness' invocation in this ASN is scoped to a single node-rooted subtree**... Without this scoping the GU citations would be unlicensed in a reachable multi-node state; with it, each is a within-subtree application."

**Problem**: The flagged pattern "a definition's introduction enumerates downstream consumers" / "new prose explains why [a fact] is needed rather than what it says." The structural content (nodes enter only via NodeBaptism, so the inc-allocator structure is a forest with each baptised node as a sole GU base) is the assertion; the closing sentences are a defensive note about how every later GU citation should be read. There is also a mild presentational tension worth resolving: NodeLineage forces `n₀ ≼ e` for *all* nodes (a single prefix-root), while NodeRootedForest calls the structure "a forest, not a single tree" — both are reconcilable (prefix-nesting vs inc-descent), but stated adjacently without that one-line reconciliation they read as conflicting.

**Required**: Keep the structural assertion (forest of node-rooted inc-subtrees; GU base = baptised node) and drop the use-site meta-claim about "every GU invocation in this ASN." Add one clause reconciling the "forest" framing with NodeLineage's single-prefix-root (inc-descent ≠ prefix-nesting).

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering (DELETEVSPAN)
**Why out of scope**: The ASN's K.μ⁻ models suffix-only contraction; the implementation's interior `DELETEVSPAN`-with-renumbering is correctly deferred to its own open question and belongs to the operations layer, which the Scope section excludes. Not an error in this ASN.

### Topic 2: Concurrency/serialization of link allocation under a shared home document
**Why out of scope**: Raised as an open question; operation atomicity and concurrency are explicitly excluded by the Scope section. The SequentialTransitionAxiom is sufficient for the abstract model.

VERDICT: REVISE
