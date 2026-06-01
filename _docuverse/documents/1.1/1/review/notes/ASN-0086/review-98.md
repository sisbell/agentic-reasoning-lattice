# Review of ASN-0086

This ASN carries the `review-mode.anti-bloat` classifier. The proofs (R0–R7a, the wp analysis, the worked sketch) are dense but, on checking, sound: the R0a antichain argument, R0a-Cor2's `#E = 2` derivation, the worked-example tumbler arithmetic (`a₁ = 1.0.1.0.1.0.2.1` etc.), and R7a's chain-order replay all hold. The findings below are therefore predominantly accreted meta-prose and duplication, which the active classifier makes REVISE-grade, plus one precision item.

## REVISE

### Issue 1: The `→` definition is stated three times in different words
**ASN-0086, intro / "State transition relation" / Properties table**: the opening paragraph, the dedicated "State transition relation" paragraph (`→ ≡ K.σ ∪ K.α ∪ K.λ`), and the Properties-table `→` row ("Dom-extending state transition relation, identified as `K.σ ∪ K.α ∪ K.λ` from ASN-0093…") all restate the same identity, and the class-(i)/(ii)/(iii) bullet list is re-described again inside R0's proof and R7a's opening.
**Problem**: "Two paragraphs in the same document say the same thing in different words." The reader meets the same definition three times before reaching any claim that uses it.
**Required**: State `→ ≡ K.σ ∪ K.α ∪ K.λ` once, in "State transition relation," and let the table row point to it without re-expanding.

### Issue 2: FreshLinkKeyDisjointness carries a use-site inventory
**ASN-0086, Sub-lemma FreshLinkKeyDisjointness**: "This discharge is cited at each fresh-link-emission site (R0, R5, R7a) rather than re-derived."
**Problem**: Enumerating a lemma's downstream consumers in the lemma's own statement is the "definition's introduction enumerates downstream consumers" anti-pattern; the inventory rots as sites move and adds nothing to the lemma's content.
**Required**: Delete the sentence. The lemma stands on its own; the consuming proofs already cite it by name.

### Issue 3: Observe_K's "Pattern domain" note re-proves decidability twice, then a third time
**ASN-0086, Definition — Observe_K, "Pattern domain — `T`, not `A^Σ`"**: the paragraph establishes decidability of `F̂ ⊆ coverage(F)` ("the finite conjunction … is decidable regardless of `coverage(F)`'s cardinality"), then re-argues it within the same paragraph ("Note `coverage(F)` is in general *infinite* … decidability rests on the finiteness of `F̂` and per-span intrinsic containment"), and then the standalone sentence immediately after restates it a third time ("The match relation is `F̂ ⊆ coverage(F)` … decidable in `℘_fin(T)` by the finiteness of `F̂` and per-span intrinsic containment").
**Problem**: Three statements of one decidability fact in adjacent lines.
**Required**: Keep one sentence: patterns range over `T` to admit ghost queries (L9/L4); the match `F̂ ⊆ coverage(F)` is decidable because `F̂` is finite and per-span containment is decidable by T2. Drop the infinitude aside and the trailing restatement.

### Issue 4: wp Case 2's closing paragraph restates regimes (i)/(ii)/(iii)
**ASN-0086, Weakest-Precondition Analysis, final paragraph of Case 2**: "The Nullify operation scopes its retraction to the unit-depth-span form (regime (i)); whether the wider crafted-span form (regime (ii)) or self-nullifying R-typed emission (regime (iii)) is admitted is a discipline-level property of caller retraction practice, not a K.λ guarantee."
**Problem**: This adds nothing past the regime (i)/(ii)/(iii) definitions and the "Relational-layer specialization" paragraph that already drew the layer-vs-substrate line. Closing summary of points just made.
**Required**: Delete the paragraph; the specialization paragraph already states the layer/substrate distinction.

### Issue 5: Repeated cross-section deferral to "WP Case 2"
**ASN-0086, "Definition — Unit-depth retraction discipline," Open Questions (retraction-discipline bullet), and the wp specialization**: multiple sites point forward/back to WP Case 2 as the place where "the consequence … is made explicit."
**Problem**: "Multiple paragraphs in different sections defer to the same downstream location." The deferral chain forces the reader to hold a pointer instead of reading the claim where it sits.
**Required**: Make the crafted-span consequence local where first raised (one clause), and let WP Case 2 be the single authoritative statement without back-pointers from the Open Questions and the discipline definition.

### Issue 6: R6b mislabeled as a pure consequence of the `nullified` definition
**ASN-0086, R6b (SingleDepthRetraction), header and Properties table**: titled "(Consequence of Definition `nullified`)" / "DEF-Consequence," yet the justification's load-bearing step is "the original tuple `(b, F', G')` persists in `L_R^Σ ⊆ L_R^{Σ'}` (by R3)."
**Problem**: The non-fixpoint claim across a transition `Σ → Σ'` depends on R3 (slice monotonicity), not on the definition alone. As stated, the within-state flatness is definitional but the *cross-state* "un-nullifying has no effect" half is not.
**Required**: Split the claim — the single-pass test is definitional (flat over `L_R^Σ`); the persistence-of-effect across `→` cites R3. Relabel accordingly, or move R3 into the dependency list.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe, ordering of Observe results, cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are correctly deferred in the Open Questions. A consistency model for concurrent `A_K` transitions and an ordering contract for Observe are genuinely new state/operation territory, not gaps in this note's single-authority, set-semantics development.

### Topic 2: Higher-arity links as `n`-ary typed relations
**Why out of scope**: The note explicitly restricts to standard-triple links (`|Σ.L(a)| = 3`); the `L_K^{(n)} ⊆ A_rel × ℘(A)^n` generalization is a separate construction, appropriately left to a future ASN.

VERDICT: REVISE
