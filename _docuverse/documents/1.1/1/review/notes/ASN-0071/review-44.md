# Review of ASN-0071

The core proofs are sound. PC (prefix confinement) is derived honestly from the vspec preconditions with the well-ordering closure made explicit; the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, F-CONTENT (via S3★ ∧ S3★-aux ∧ L14), F-FIN, and the worked scenarios all check out arithmetically (reach computations, multi-block dedup, subtree capture, interior-action-point rejection). I found no defect in the mathematics. The findings below are the forward-reference / redundancy accretion the `anti-bloat` classifier asks for.

## REVISE

### Issue 1: Read/find inverse stated twice
**ASN-0071, intro vs *Discovery through sharing***: Intro — "The answer comes from walking the document's arrangement and resolving each V-position... the read-direction. The same reader can ask the inverse." *Discovery through sharing* — "`find` and read are inverse traversals of the same `M : E_doc → (T ⇀ T)` structure: reading goes from arrangement to content... finding goes from content to arrangement."
**Problem**: Two paragraphs in different sections make the same read/find-duality point in different words. The intro already frames the operation as the inverse of reading; the closing restatement advances no claim.
**Required**: Delete the duplicate from *Discovery through sharing* (the trailing paragraph), keeping the intro framing.

### Issue 2: "Source-anchored" paragraph duplicates F-LOC and gestures out of scope
**ASN-0071, *Resolution*** (final paragraph): "We note a structural property: `iaddrs_one(d_s, σ)(Σ)` depends only on `Σ.M(d_s)`. Each vspec is *source-anchored*... sources can be consulted independently in any order, **by any node holding the relevant arrangement**."
**Problem**: This is F-LOC restated as prose. The trailing clause "by any node holding the relevant arrangement" reaches into distributed deployment, which the note itself declares out of scope (*What we do not specify* (ii); Open Question on replicas).
**Required**: Drop the paragraph; F-LOC carries the locality content. If a one-line note is wanted, state the locality fact without the distributed-node gesture.

### Issue 3: Currency prose pre-answers a deferred Open Question
**ASN-0071, *Currency: state dependence***: "`find` returns currently-containing documents, an `R`-based query returns ever-containing ones, **and they coincide only when no arrangement contraction has touched a queried I-address.**"
**Problem**: The coincidence condition is a substantive claim about the `find`/`R` relationship — but the relationship is explicitly listed as unresolved in Open Questions ("What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?"). Either the claim is established (then it is not an open question) or it is unbacked prose answering a question the note simultaneously defers. The bare statement that `find` does not consult `R` suffices here.
**Required**: Cut the "coincide only when..." comparison; keep "`find` does not consult `R`; current vs. ever-containing is deferred (Open Questions)."

### Issue 4: P1 forward-preservation reassurance in `find`'s precondition
**ASN-0071, *The operation*** (well-definedness): "entity permanence (P1, ASN-0047: `Σ.E ⊆ Σ'.E`) preserves `d_s ∈ E_doc` forward, so a source document available when the vspec was formed remains so at any later `Σ`."
**Problem**: `find(Q)(Σ)` is defined at a single state `Σ` and `wp-defined` is checked at that `Σ`. The "remains available at any later state" remark is a temporal currency aside that does not advance the well-definedness argument and overlaps the *Currency* section's concern. It is meta-prose around the precondition.
**Required**: State `wp-defined` and that `find` is defined exactly when it holds at the evaluation state; drop the P1-forward sentence.

## OUT_OF_SCOPE

### Topic 1: find vs. provenance-relation R reconciliation
**Why out of scope**: The precise guarantee linking current containment to `R` is genuinely new territory (correctly listed as an Open Question); the note should only state that `find` reads `M`, not `R`. Surfacing the full reconciliation belongs to a future ASN, not this one.

VERDICT: REVISE
