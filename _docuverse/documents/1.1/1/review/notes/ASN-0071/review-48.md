# Review of ASN-0071

## REVISE

### Issue 1: "Prefix names subtree" is asserted as a specification guarantee but never stated as a claim, and the blanket form is false for width > 1

**ASN-0071, A worked scenario (cross-depth query)**: "FINDDOCSCONTAINING is specified to return *'any portion of the material specified ... regardless of where the native copies are located'* (LM 4/63): the user who names the coarse coordinate names its whole subtree — the *'prefix names subtree'* semantics."

**Problem**: This is phrased as a specification guarantee ("is specified to return", "the *'prefix names subtree'* semantics"), but it appears only inside one worked example and never as a derived claim in the Claims table. An implementer cannot rely on "naming a coarse coordinate captures the whole subtree" from a single witnessed instance. Worse, the general statement is only true for a **width-1** span. For `σ = (u, ℓ)` with `#u < m_C`, `⟦σ⟧ ∩ dom(M(d_s))` captures every depth-`m_C` position whose first `#u` components equal `u` *only when reach is `[u₁,…,u_{#u}+1]`* (the width-1 case used in the example, `δ(1,2)`). A width-2 span (`δ(2,2)`) captures two sibling subtrees, not "the subtree." The cross-depth behavior is genuinely important and deserves abstraction — but the current sentence overstates a one-example demonstration into a general guarantee.

**Required**: Either (a) add a named, derived claim stating the cross-depth capture precisely — for a depth-`#u` span, `⟦σ⟧ ∩ dom(M(d_s))` is exactly the set of arrangement positions whose first `#u` components agree with `u` and whose component `#u` lies in `[u_{#u}, reach_{#u})` — with the width dependence made explicit; or (b) downgrade the prose to "in this width-1 instance" and drop the "is specified to" / "prefix names subtree semantics" framing.

### Issue 2: The same Nelson "any portion" quote is made "the operative reading" of two distinct phenomena

**ASN-0071, cross-depth query vs. Partial overlap suffices**:
- Cross-depth: `"any portion of the material specified ... regardless of where the native copies are located" (LM 4/63)` is attached to the query span capturing a subtree.
- Partial overlap: "This is the operative reading of Nelson's 'any portion': completeness is over the existence of non-empty intersection, not over inclusion of the whole."

**Problem**: Two paragraphs lean on the same source phrase for different claims, each calling its use the operative reading. The cross-depth use concerns the **query span** denotation; the partial-overlap use concerns **result documents** each holding a fragment. The phrase "regardless of where the native copies are located" actually supports the transclusion-discovery / partial-overlap reading, not the prefix-subtree reading — so the cross-depth citation is misattributed. There cannot be two operative readings of one phrase.

**Required**: Cite "any portion ... regardless of where native copies are located" once, for partial-overlap/transclusion discovery (where it fits). Give the cross-depth subtree behavior its own justification rather than reusing this quote.

### Issue 3: Completeness/soundness/distinctness are definitional restatements presented as results

**ASN-0071, Completeness and soundness / Set semantics; table rows F-COMP, F-SOUND, F-DIST**: "The membership criterion is a biconditional — the definition of `find(Q)(Σ)` ... decomposes into two directions." Basis columns read "direct from F-find (⟸/⟹ direction of the defining iff)" and "(codomain is `P(E_doc)`)."

**Problem**: `find` is *defined* by the set-builder predicate, so "completeness" and "soundness" are the two halves of the defining `iff` and "distinctness" is just "a set has no duplicates." None require derivation. Calling them completeness/soundness suggests theorems that establish the operation finds everything / nothing spurious, when in fact nothing is proved beyond unfolding the definition. The standalone `##` sections add ceremony around a definition (the anti-bloat pattern this note is flagged for).

**Required**: Fold these into the F-find definition (the labels may remain in the table for downstream reference) and remove the prose that re-states the definition as a decomposed biconditional.

### Issue 4: F-LOC is an orphan claim

**ASN-0071, Resolution / table row F-LOC**: "Source locality: `Σ.M(d_s) = Σ'.M(d_s) ⟹ iaddrs_one(d_s, σ)(Σ) = iaddrs_one(d_s, σ)(Σ')`".

**Problem**: F-LOC is introduced but never consumed — F-CUR (state dependence) is the property the rest of the note actually uses. A locality lemma with no use site is accretion.

**Required**: Drop F-LOC, or show where it is load-bearing (e.g., if it is meant to support F-CUR, state that dependence and cut the duplication).

## OUT_OF_SCOPE

### Topic 1: Relationship to the historical provenance relation R, rejection-vs-filter policy, contraction invariant

These are correctly deferred in Open Questions. The current-state semantics of `find` is self-contained; the `R`-relationship and rejection policy are genuinely new territory, not gaps in this ASN. No action needed.

META: not needed — the ASN defines query state, an operation on it, and its invariants abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
