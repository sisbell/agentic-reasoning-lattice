# Review of ASN-0093

The mathematical core is sound. I checked the freshness lemmas (FirstEmissionFreshness, SubsequentEmissionFreshness), the ChainMembershipForOrigin induction, the C1b/L1b element-field-depth preservation under `inc(·,0)`, and the cross-document disjointness chain (both the prefix-comparable `d ≺ d'` separator argument and the prefix-incomparable lift). The simultaneous-induction framing correctly avoids circularity: every freshness/lemma appeal at a transition reads the IH pre-state, and the worked example exercises both emission branches and both cross-document cases consistently. No rigor gap found.

The findings below are accretion patterns, surfaced under the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Defensive pre-justification of routine frame behavior
**ASN-0093, State model**: "Throughout, the tumbler projections — origin(·) and T4b's field projection E(·) — are state-independent: each is computed from its address argument alone and reads no state component. Consequently, whenever a store is held in frame, every prior key's value under these projections (its origin, its #E) transfers unchanged."
**Problem**: This is meta-prose explaining why frame conditions transfer projections. A frame condition already states the store is unchanged; that the `origin`/`#E` of an unchanged key are unchanged is immediate and needs no standing paragraph. The reader must skip past this to reach the actual state model.
**Required**: Delete. If a specific discharge needs the fact, cite it inline at that single site.

### Issue 2: Essay content in the anchor definition
**ASN-0093, Address sub-allocators under documents**: "The anchors themselves are *not* in `dom(C) ∪ dom(L)` … so they inhabit the foundation carrier set `T` as structural witnesses without occupying any state component."
**Problem**: The load-bearing content is "anchors have `#E = 1` while content/link addresses have `#E ≥ 2`, so anchors are not stored." The trailing clause "inhabit the foundation carrier set T as structural witnesses without occupying any state component" advances no reasoning — it is decorative restatement of "not stored."
**Required**: Keep the `#E` separation argument; drop the "structural witnesses" gloss.

### Issue 3: Use-site rationale in the induction framing
**ASN-0093, Discharge of stated invariants**: "The conjunction is what licenses the mutual reliance between the K.α/K.λ emission discharges and these lemmas (the K.α first-emit branch invokes FirstEmissionFreshness, itself an IH conjunct)."
**Problem**: This sentence justifies *why* the proof is structured as a simultaneous induction by inventorying which discharge invokes which lemma. The preceding sentence ("the inductive hypothesis at each step is the conjunction of every such property") already states the mechanism; the parenthetical is a use-site inventory that rots as the invariant list changes.
**Required**: Remove the explanatory sentence; the conjunction statement suffices.

### Issue 4: Citation inventory duplicated between prose and table
**ASN-0093, Per-chain disciplines vs. Properties Introduced**: the five disciplines (ChainElementT4Validity, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension) each carry an inline "*Source: ASN-0040 X*", and the Properties table re-lists each as a CITATION row pointing "See *Per-chain disciplines*. Cites ASN-0040 X."
**Problem**: The same local-name → ASN-0040-result mapping appears twice, in two sections, in different words. The table rows add nothing beyond the disciplines block they redirect back to.
**Required**: State each citation mapping once. Either drop the table's CITATION rows or drop the inline "*Source:*" lines, not both locations.

## OUT_OF_SCOPE

### Topic 1: Allocator-conformance of document addresses themselves
K.σ admits any T4-valid `zeros = 2` tumbler as `d` without requiring `d` to be a T10a-produced output. Cross-document disjointness holds regardless (the lemma handles arbitrary distinct documents), so this is not an error — but a higher-layer document-introduction primitive that ties `d` to a version-allocator (named in Scope) is where document-allocator discipline belongs.

META: The ASN defines abstract state, three append-only operations, and the invariants they preserve — it specifies system guarantees, not implementation mechanics; it has not drifted.

VERDICT: REVISE
