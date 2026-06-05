# Review of ASN-0113

## REVISE

### Issue 1: W19's justification contradicts the substrate it relies on

**ASN-0113, "Permanence of the report" / W19**: "If document identity is pinned to a fixed version — an immutable arrangement, since editing forks a new version rather than mutating an existing one — then `V_S(d)` is fixed".

**Problem**: The claim that "editing forks a new version rather than mutating an existing one" is false in the very substrate this note is built on. ASN-0047 provides K.μ⁻ (ArrangementContraction — "Existing V→I mappings are removed from some d ∈ E_doc") and K.μ~ (ArrangementReordering), both of which mutate `M(d)` *in place* for an existing `d ∈ E_doc`, with no fork. So a document's arrangement — and hence `V_S(d)` and the reported extents — can change in place under the foundation's own transition vocabulary. The parenthetical asserts a model property that the foundation directly refutes. The conditional claim ("for a fixed version the report is fixed") and W18 (pure function of state) are sound; only the justification is wrong.

**Required**: Remove or correct the parenthetical. Permanence of the report is *inherited from the state being unchanged* (W18) — if no transition occurs, `M(d)` and thus `V_S(d)` are fixed. Do not ground it in a "forking, never mutation" claim that K.μ⁻/K.μ~ contradict.

### Issue 2: Open Question 2 has already been answered normatively by the body

**ASN-0113, "Open Questions"**: "Must an empty subspace be reported as a zero-extent span or may it be omitted entirely, and which choice preserves comparability across all documents?"

**Problem**: This is not open — the body decides it twice. W7 (OneSpanPerOccupiedSubspace) mandates "exactly `|occupied(d)|` members," i.e. empty subspaces are omitted; W14 (Comparability) commits to treating an absent subspace as the value zero so comparison stays total. Moreover, a "zero-extent span" is structurally impossible under the ASN's own machinery: W3 requires `n_S ≥ 1` for well-formedness, and every well-formed span is non-empty (S2, ASN-0053). Listing a resolved (and partly malformed) design choice as open contradicts the normative claims.

**Required**: Either delete this open question, or recast it so it does not contradict W7/W14 (e.g., the deeper question of how a *consumer* should interpret omission across heterogeneous-vintage documents), and drop the "zero-extent span" phrasing since no such span exists.

### Issue 3: W12's reachability construction elides required coupling steps

**ASN-0113, "What the pair reveals…" / W12**: "`c` applications of the content-restricted arrangement extension K.μ⁺ — each adding one text V-position … drive `n_{s_C}(d) = c`".

**Problem**: K.μ⁺ (ASN-0047) cannot, on its own, add a text V-position: its precondition requires that for every new mapping `M'(d)(v) = a`, `a ∈ dom(C)`, so each text position presupposes a prior K.α content allocation, and the valid composite must satisfy the J0 coupling. The construction presents K.μ⁺ as self-sufficient, omitting the K.α allocations and the J0 coupling that the substrate demands. The existence claim is plausible (content is unboundedly allocatable by T0(a)/T0(b)), but as written the transition sketch is not faithful to the foundation's composite-transition discipline.

**Required**: State the per-position step as the coupled K.α + K.μ⁺ pair (satisfying J0), so the reachability of arbitrary `(c, k)` is grounded in legal composite transitions rather than an isolated K.μ⁺.

## OUT_OF_SCOPE

(none — the note stays within the per-subspace extent query and correctly defers content delivery, the single overall extent, link counting/discovery, version comparison, and transclusion to other operations.)

VERDICT: REVISE
