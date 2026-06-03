# Review of ASN-0070

The mathematics is sound and unusually thorough — seven worked configurations, both inclusions of the postcondition split out (F-sound/F-complete), and a full existence-and-uniqueness proof for the canonical form. The objections below are mostly anti-bloat (the note carries that classifier) plus one skipped exhaustiveness step.

## REVISE

### Issue 1: Case analysis in F-canonical Step 1 does not state exhaustiveness
**ASN-0070, F-canonical Theorem, Step 1**: "by case analysis on `k = actionPoint(ℓ)`" with cases `1 ≤ k < m_S(d)` and `k = m_S(d)`.
**Problem**: The two cases are exhaustive only because `1 ≤ actionPoint(ℓ) ≤ #ℓ = m_S(d)` (ActionPoint postcondition, ASN-0034). The proof never states this, so the reader must supply the bound that closes the case split — exactly the kind of skipped justification a rigorous proof should not leave implicit. There is also no explicit treatment of `k > m_S(d)` being impossible.
**Required**: One sentence: since `actionPoint(ℓ) ∈ [1, #ℓ]` and `#ℓ = m_S(d)`, the cases `1 ≤ k < m_S(d)` and `k = m_S(d)` are jointly exhaustive (and `k > m_S(d)` cannot arise).

### Issue 2: DEF/THM cataloguing paragraph is meta-prose
**ASN-0070, Canonical Form section**: "The clauses (i)–(iii) above are the *definitional content*... We catalogue them as F-canon-form (DEF). That a canonical form of this shape *exists and is unique*... is a separate proof obligation, established next as a theorem (F-canonical, THM)."
**Problem**: This paragraph explains the note's own labelling scheme rather than advancing the argument. The reader following the canonical-form derivation hits a speed bump that says only "we tagged the above DEF and the next THM." The DEF/THM distinction is already visible from the claim headers.
**Required**: Delete the paragraph; the definition clauses and the theorem that follows speak for themselves.

### Issue 3: F-multi Depends carries "cited only for X, not Y" disclaimers
**ASN-0070, F-multi, Depends**: "K.μ⁺ ... (contrast CL-UNIQ, ASN-0047, which constrains only the link subspace); S5 (UnrestrictedSharing, ASN-0036) — cited only for the abstract-cardinality (model-existence) point, not for reachability."
**Problem**: These are defensive disclaimers about what each dependency is *not* used for — reviser-drift prose that pre-empts a misreading rather than stating the dependency's role. The reader must parse the negative scoping to extract the actual citation.
**Required**: State each dependency's positive role only (S5 supplies the cardinality witness; K.μ⁺'s lack of content-side injectivity makes the hypothesis reachable). Drop the contrast/disclaimer clauses.

### Issue 4: State-Dependence section restates without advancing
**ASN-0070, State-Dependence**: "This is not a derived property of the operation but a structural consequence of two facts already established... The operation itself contributes nothing new; it is a window through which arrangement variability becomes observable."
**Problem**: The first clause carries content (F-state is a corollary, not a lemma); the rest is rhetoric that re-says "the result varies because `M(d)` varies" in three different registers. The "window" framing and "contributes nothing new" add no reasoning a precise reader can act on.
**Required**: Reduce to the operative point: F-state follows because `L(ℓ)` is L12-invariant while `M(d)` — the only state component `R` reads — varies across transitions. Cut the essay sentences.

## OUT_OF_SCOPE

### Topic 1: Reporting which coverage I-addresses failed to resolve (partial-reach detail)
**Why out of scope**: The Open Questions already park this; the result form deliberately reports only what resolved. Designing a failed-reach report is a future ASN, not a defect here.

### Topic 2: Concurrency semantics of `follow` under concurrent modification
**Why out of scope**: F-frame establishes purity; concurrency guarantees are a separate operational concern flagged in Open Questions.

VERDICT: REVISE
