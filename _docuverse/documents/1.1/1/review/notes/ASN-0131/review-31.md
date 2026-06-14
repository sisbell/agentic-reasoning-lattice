# Review of ASN-0131

This is a careful, rigorous note. The worked instance computes correctly (I verified the `[a₂, a₄)` coverage via TS3, the `a₁ ≼ a₂` failure, and the `θ`-disjointness field-agreement argument), the retraction analysis (RE-RET) correctly isolates the load-bearing R-Scope/R0a/R6a chain and is honest about conditioning net-removal on the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis, and RE-CWP is a genuine non-trivial weakest-precondition. Two issues remain.

## REVISE

### Issue 1: The central stability enumeration mixes two incompatible foundation transition models for insert/delete

**ASN-0131, "Stability … Under editing of the queried document" (and the RE-EDIT table)**: "Over the transition vocabulary (ASN-0047), only the content-subspace movers on `d` … together with `K.λ` … and the user-facing shift-based insert/delete (content displacements through the region, I3/D-SHIFT, ASN-0082) … can move the answer." And: "a shift is no domain-preserving K.μ~ reorder, and its effect on the image is read off the displacement directly rather than through F-IMG-SWING."

**Problem**: RE-EDIT frames itself as a *completeness* claim over "the transition vocabulary (ASN-0047)," then includes a mover category that is not in that vocabulary and contradicts it. ASN-0047's `K.μ⁺` is defined with **existing mappings unchanged** — `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`, an append at the contiguous frontier. ASN-0082's `I3` instead **shifts existing content** — `M'(d)(shift(v, n)) = M(d)(v)` for every `v ≥ p`. These are different arrangement transformations of the same user operation, and the note never says which ASN-0047 transition (or composite) insert/delete *is*, nor reconciles I3's shift with K.μ⁺'s frame. The "only … can move the answer, over the transition vocabulary (ASN-0047)" claim therefore rests on an undefined, mixed notion of the vocabulary.

The defect bites under both readings:
- *Composite reading* (the natural sense of "the foundation realises them as displacements"): a mid-document insert decomposes as `K.α` + `K.μ⁺` (append at frontier) + `K.μ~` (permute existing content into place); delete as `K.μ~` + `K.μ⁻`. The existing-content motion lives in the `K.μ~` component — which is exactly where **F-IMG-SWING applies**. So the swing *is* captured by the K.μ~ analysis already given, directly contradicting "its effect on the image is read off the displacement directly rather than through F-IMG-SWING."
- *Monolithic reading* (insert/delete are ASN-0082's I3/D-SHIFT primitives): then they are not ASN-0047 transitions at all (no ASN-0047 transition both grows the domain and shifts existing content — K.μ⁺ can't shift, K.μ~ is domain-preserving by K.μ~-FIX, K.μ⁻ truncates only the tail), and "over the transition vocabulary (ASN-0047)" is simply the wrong frame for the enumeration.

**Required**: Pin down the vocabulary the stability analysis ranges over. Either (a) state that insert/delete are composites of ASN-0047 transitions and derive their image effect from the components — in which case the swing is a K.μ~-component effect via F-IMG-SWING and the contrary sentence must go; or (b) state explicitly that the analysis ranges over a combined ASN-0047 + ASN-0082 vocabulary, and reconcile I3's "existing mappings shift" with K.μ⁺'s "existing mappings unchanged" so the reader knows these are not competing descriptions of one transition. Until then the completeness claim ("only [these] can move the answer") is not grounded.

### Issue 2 (anti-bloat): The standing-assumption paragraph front-loads defensive justification and a use-site lemma inventory that are re-cited downstream

**ASN-0131, "The unit of the answer," standing-assumption paragraph**: "The ASN-0047 `K.λ` would otherwise admit a *wide* retraction whose to-set spans a range of link addresses … and such a value could pre-nullify links not yet allocated; the discipline is precisely what excludes it." And: "that same framing lets us *import* ASN-0086's link-store lemmas — the `nullified` set, R0a's flat-domain antichain, R-Scope's single-tuple scope, R6a's retraction permanence, R6c's restoration-by-reemission, and the `wp` of Case 2 …"

**Problem**: The load-bearing content of this paragraph is one fact — *Σ.L evolves only through K.λ (every other transition frames the link store), so ASN-0086's link-store lemmas transfer verbatim to the populated-arrangement states this note queries.* Around it sits skippable meta-prose the classifier targets: the "why the discipline is needed" essay about the excluded wide-retraction case ("why the axiom is needed rather than what it says"), and an upfront inventory of the imported lemmas — each of which is then re-cited at its actual use site (R0a, R-Scope, R6a all reappear in RE-RET; wp Case 2 reappears under "link emission" *and* RE-RET). The same pattern recurs as smaller echoes: "Determinism first. RE(W, d, Σ) is a function of (W, d, Σ) and nothing else … This is the bedrock under everything that follows" restates RE-LOC's determinism, and the wp-Case-2 conjunct discharge is performed once generically under "link emission" and again for the emitter `b` under retraction.

**Required**: Keep the bridge (link store evolves only via K.λ ⟹ the ASN-0086 lemmas hold at populated-arrangement states). Drop the excluded-case justification and the lemma inventory, citing each lemma where it is used. Remove the determinism restatement (RE-LOC suffices) and have RE-RET cite the general addressability fact rather than re-discharging the wp conjuncts.

## OUT_OF_SCOPE

The note's own Open Questions correctly defer the right things — V-position rendering (OQ3), intersection-distributivity given non-injective arrangements (OQ4), non-co-resident link stores (OQ5), type-slot-vs-content matching (OQ6, the sole remaining exception to RE-RET, properly flagged), and link-subspace regions (OQ7). None of these is an in-scope gap mislabeled as future work, and the note includes no claims belonging to the excluded operations (it withholds link identity, never counts, and cites ASN-0127's image/discovery machinery rather than rebuilding it). No additions.

VERDICT: REVISE
