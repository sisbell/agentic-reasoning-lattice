# Review of ASN-0131

The formal core is sound. I checked the definition, the touch relation, the worked instance (the width-2 straddling span `(a₂, δ(2,#a₂))` covers `[a₂, a₄)` since `a₄ = shift(a₂,2)`; `e₃`'s field-agreement disjointness argument is valid; the `{(1, e₁)}` result exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT correctly), RE-UDIST (the `touch_W(e)` factoring out of the existential is legitimate, and `Avail(Σ)` is genuinely region-independent), RE-SEL, RE-CWP (the drop-condition derivation and the `R = ∅` collapse both check out), and RE-RET (R-Scope confines the nullification to `ℓ`, so the sole-bearer biconditional holds, and the `coverage(Θ)` hypothesis is honestly carried). Depth requirements are met: concrete worked example, non-trivial wp (RE-CWP, retraction), derived consequences (composition, transclusion, stability), foundation-only citations. No correctness defects found.

The findings below are anti-bloat trims — the note carries the `review-mode.anti-bloat` classifier and a small amount of accreted meta-prose remains.

## REVISE

### Issue 1: Global orphaning/resurrection digression in the contraction analysis
**ASN-0131, Stability (contraction bullet)**: "This is a region-local loss of reach, **not** the global *orphaning* of LP17 (ASN-0098)... The genuinely global *orphaning* of LP17 — and the *resurrection* of LP18 (ASN-0098) on later re-arrangement — obtains only in the limiting case where the departed content comes to be arranged by no document at all."
**Problem**: RETRIEVEENDSETS' contraction stability is fully captured by F-IMG-CONTR + RE-CWP, and the useful contrast is already made by the first sentence (region-local, not global) and the positive re-surfacing claim ("Should the content be re-arranged into `d`... the endset is surfaced once more"). The trailing sentence imports LP17 orphaning and LP18 resurrection — a global phenomenon keyed on "arranged by no document at all" — that a single-region query never engages. This is the "imagines a case outside the claim's scope" pattern: a precise reader skips it to follow the contraction claim.
**Required**: Drop the final LP17/LP18 sentence; the region-local clarification and the re-surfacing claim suffice.

### Issue 2: Redundant clause in the ASN-0086 bridge
**ASN-0131, "The unit of the answer"**: "...every ASN-0086 lemma that constrains `Σ.L` alone holds verbatim at every ASN-0047-reachable state, including the *populated-arrangement* states whose arrangements ASN-0086's own (empty-arrangement) layer never reaches."
**Problem**: The bridge itself is load-bearing and correct, but the trailing "including the *populated-arrangement* states..." clause restates what "constrains `Σ.L` alone" already settles. Once the lemmas are qualified as `Σ.L`-only, the empty-vs-populated arrangement difference is *definitionally* irrelevant; spelling it out as a reassurance says the same thing twice (pattern 7).
**Required**: End the sentence at "holds verbatim at every ASN-0047-reachable state." The `Σ.L`-alone qualifier carries the point.

### Issue 3: Stability-section bookend recap and RE-IDENT forward pointer
**ASN-0131, Stability (opening vs. closing)**: opening — "its stability is entirely determined by how state changes move the two things it reads: the region's image and the addressable population"; closing — "the answer's stability has two components... it tracks the *arrangement*... and it respects the *active population*."
**Problem**: The closing paragraph recapitulates the opening's two-component framing after the section has already enumerated every mover. Combined with the RE-IDENT forward pointer in the transclusion section ("a general invariant — independent of transclusion, and **governing the stability analysis below as well** — which we state once here"), the note announces, re-announces, and summarizes the same image-motion/population-motion split three times. The use-site pointer and the closing recap are the trimmable instances.
**Problem severity**: minor — fold rather than excise.
**Required**: Drop the "governing the stability analysis below as well" pointer (state RE-IDENT and let the stability section cite it), and either delete the closing recap or reduce it to a one-line pointer to RE-RET/RE-CWP.

## OUT_OF_SCOPE

The seven Open Questions correctly fence the genuinely future territory — entirety-vs-touching-spans (OQ1), multiplicity preservation (OQ2), the rendered/V-order answer (OQ3), intersection-composability under non-injective arrangement (OQ4), cross-store completeness (OQ5), type-slot-against-content semantics (OQ6), and link-subspace regions (OQ7). Nothing additional needs flagging; the mechanical behavior for each (e.g. a type-slot match *is* surfaced by RE-DEF; only its meaning is deferred) is well-defined within this ASN.

The naming of FINDLINKSFROMTOTHREE in the body is a contrast, not a result-citation by number, and the scope list pre-clears it — not a finding.

VERDICT: REVISE
