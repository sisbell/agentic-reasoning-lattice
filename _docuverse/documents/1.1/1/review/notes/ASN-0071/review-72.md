# Review of ASN-0071

## REVISE

### Issue 1: Intro motivation contradicts F-CONTENT
**ASN-0071, opening**: "a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material."
**Problem**: A *citation* in this model is a link, not a content reference. But F-CONTENT proves the operation matches "because it shares *byte content*, never because it shares a *link* address," and `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. A document that *links to* passage `a` without transcluding it is **not** returned. The third motivating use-case (citation enumeration) is exactly the case the operation excludes — the intro overpromises a link-discovery capability F-CONTENT explicitly disclaims. The royalty/transclusion and quotation examples are fine; the citation example is wrong.
**Required**: Drop or reword the citation example so the motivation matches what `find` actually computes (content-containment / transclusion), not link-based citation discovery.

### Issue 2: `vspec` silently duplicates ASN-0058's ContentReference
**ASN-0071, *The query***: "A **vspec** is a pair `(d_s, σ)` where `d_s` is a document address ... and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace..."
**Problem**: ASN-0058 (foundation) already defines `ContentReference = (d_s, σ)` with σ level-uniform, T12, `#ℓ = #u`. The vspec is the same object with two relaxations — it drops well-formedness and the `#u = m` depth-pinning (clause (iii)), which is what enables the F-DEEP/Q_E cross-depth cases. The ASN cites ASN-0058 for M13/M14/C0a but introduces this parallel type and a parallel `iaddrs_one` (overlapping ASN-0058's `resolve`/C1) without relating either to the foundation. Standard 7 requires flagging reinvention of foundation notation.
**Required**: State explicitly that a vspec is ContentReference minus well-formedness and depth-pinning, and that `iaddrs_one` is the set-image counterpart of `resolve` (reproven for integrity because the relaxation puts vspecs outside C1's well-formedness hypothesis). One sentence each suffices; the relaxation is the justification.

### Issue 3: Procedural narration and duplicated exposition (anti-bloat)
**ASN-0071, multiple sites**:
- *Resolution*: "We show subspace confinement first, then apply S3★." — proof roadmap that adds nothing; the two labeled sub-paragraphs already announce the order.
- *The query*, Componentwise fact: "T0 thus excludes `p` as a first point of disagreement, but settling every position needs one further step." — narration of proof structure, not argument.
- Worked scenario, Q_G: "Both layers of deduplication act here: the cross-source union folds the doubly-resolved `a₁`, and the `P(E_doc)` codomain folds the multiply-referencing document." — restates F-DIST and the cross-source union already derived in *The operation* and earlier in the same scenario.
**Problem**: The note carries `review-mode.anti-bloat`. These are meta-prose in argument slots — the reader must skip them to follow the claim.
**Required**: Cut the roadmap/narration sentences; let the structure carry itself. Keep the worked numbers, drop the "both layers" recap.

## OUT_OF_SCOPE

### Topic 1: Relationship to provenance `R`, rejection of unresolvable vspecs, post-contraction invariant
**Why out of scope**: The three Open Questions correctly defer (a) the current-result-vs-historical-`R` guarantee, (b) when to reject rather than silently filter (F-FILT), and (c) the cross-transition invariant under K.μ⁻. These belong in future ASNs; their absence here is not an error. No action.

VERDICT: REVISE
