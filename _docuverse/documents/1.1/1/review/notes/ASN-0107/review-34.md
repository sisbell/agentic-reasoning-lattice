# Review of ASN-0107

## REVISE

### Issue 1: Eligibility of higher-arity links under a three-part request is unexamined

**ASN-0107, "State and the Counting Request" / `sat` / `match`**: "`sat(a, Q, Σ) ≡ (A i : 1 ≤ i ≤ 3 : ...)`" with "`match(Q, Σ) = {a ∈ dom(Σ.L) : sat(a, Q, Σ)}`", justified by "Every link carries at least these three slots, since `|Σ.L(a)| ≥ 3`."

**Problem**: `match` ranges over all of `dom(Σ.L)`, including links of arity `N > 3`, and `sat` evaluates only slots 1–3. So a 5-set link is counted by a FROMTOTHREE request whenever its first three endsets meet `Q₁,Q₂,Q₃`, with slots 4–5 silently ignored. The note resolves the *request*-side `n>3` question ("we fix the standard triple here") but never the *link*-side question: should a three-part request count a five-endset link at all, and on what semantics for its surplus slots? This is a genuine specification decision, and ASN-0086 makes the opposite one for its typed relations (the `|Σ.L(a)| = 3` conjunct "restricts every `L_K` to standard-triple links"). The divergence is undiscussed.

**Required**: State and justify the eligibility rule — either restrict `match` to `|Σ.L(a)| = 3`, or explicitly commit to counting all `N ≥ 3` links on slots 1–3 and say why ignoring the surplus slots is the intended FROMTOTHREE meaning.

### Issue 2: Boundary-case paragraph drifts into implementation mechanics and re-treads D2

**ASN-0107, "How the Count Changes: Content Added"** (paragraph beginning "The boundary case is a warning about *positional* requests"): "...The same caution applies to any raw-positional notation at an implementation layer that renumbers on insert: such renumbering is a K.μ~-style remapping, distinct from the K.μ⁺ extension semantics the rest of this note depends on."

**Problem**: Most of this paragraph re-derives D2's extension-vs-reordering distinction already stated under D2, and the closing sentences descend to "an implementation layer that renumbers on insert" — implementation mechanics, not a system guarantee. This is accreted defensive prose: the load-bearing point (a positional query must be re-anchored after a reorder) is one sentence; the rest restates D2 and cautions about a notation layer the abstract model does not define.

**Required**: Reduce to the single guarantee (content-anchored counts are stable; positional queries must re-anchor after K.μ~) and drop the implementation-layer renumbering discussion.

### Issue 3: CL-OWN aside in the worked example dismisses an inapplicable invariant

**ASN-0107, "A Worked Instance"**: "...which discharges S3★ (GeneralizedReferentialIntegrity) for the content subspace; CL-OWN governs only link-subspace positions and so imposes nothing here."

**Problem**: The queried positions are all content-subspace, so CL-OWN is excluded by its own carrier. Naming it only to say it "imposes nothing here" is reviser drift — prose addressing a case the precondition already excludes. The S3★ discharge advances the example; the CL-OWN clause is noise.

**Required**: Delete the CL-OWN clause; keep the S3★ discharge.

## OUT_OF_SCOPE

### Topic 1: Coincidence conditions for discovery vs. existence count, and count-vs-retrieval staleness
The Open Questions correctly defer (a) independently document-anchored request parts, (b) when every resident match is discoverable, and (c) the count-vs-FINDLINKS-cardinality relationship. These are future ASNs, not gaps in this one.

VERDICT: REVISE
