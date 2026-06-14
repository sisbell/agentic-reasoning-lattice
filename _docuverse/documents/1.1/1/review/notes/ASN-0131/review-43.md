# Review of ASN-0131

## REVISE

### Issue 1: The gain/loss taxonomy under shift editing is incorrectly enumerated, and the delete case is asserted by analogy

**ASN-0131, "Stability: the answer as the document is edited"** (the insert/delete paragraph): "So the image both gains and loses only in the through-region case — an insert seated below `W`, or a delete reaching into it — where the region both sheds content and takes on content displaced in from outside it. Where the region instead coincides with the insertion gap, the primitive delivers pure loss: `W`'s content is carried off and the gap left unfilled, so `W ∩ dom(Σ'.M(d)) = ∅` and the image drops to `∅` until a separate step refills it."

**Problem**: The insert half is worked correctly (the conclusion "a gain to the fixed image only when the donor lay below `W`" is right — a within-`W` donor was already imaged, so no net gain). But the delete half is folded in by analogy ("*or a delete reaching into it*") without being computed, and delete is **not** analogous to insert: a deletion *closes* the gap by shifting content down, whereas an insertion *leaves* one. The configurations therefore differ, and the exhaustive word "only" makes both lists false:

- **Omitted gain+loss case (delete below `W`).** Let positions `[1,1]…[1,6]` hold `a₁…a₆`, take `W = {[1,3],[1,4]}` (so the pre-image is `{a₃, a₄}`), and delete the single position `[1,1]` — a removed span lying *entirely below* `W`. By D-SHIFT the content above shifts down: `a₄ → [1,3]`, `a₅ → [1,4]`. The post-image is `{a₄, a₅}`: `a₃` is lost and `a₅` is gained — **both gain and loss** — yet this edit is neither "an insert below `W`" nor "a delete reaching into it." The symmetric counterpart of "insert below `W`" is "delete below `W`," and it is missing from the list.

- **Incomplete pure-loss case.** "Region coincides with the insertion gap → `∅`" is not the only pure-loss configuration. An insert strictly *within* a larger `W` (gap interior to `W`) is also pure loss: the top `n` content pieces are carried above `W` while the gap content merely relocates upward within `W`, so the image loses its top without dropping to `∅`. The given example is one instance, not the class.

**Required**: Either work the delete case explicitly and state the gain/loss/pure-loss partition correctly and completely, or — since RE-EDIT's load-bearing conclusion is only "non-monotone, tracks by membership, spans fixed (RE-IDENT)" — delete the taxonomy entirely. The membership-tracking claim does not depend on which configuration yields gain vs. loss, so this incorrectly-enumerated elaboration is not earning its length.

### Issue 2: Depth-independence overclaims coverage of a delete the foundation establishes only at depth 2

**ASN-0131, "Stability… / Under editing of the queried document"** (cross-model lift paragraph): "The lift is depth-independent: it turns on the edit's write-set being `Σ.M(d)` alone, not on D-SHIFT's `#p = 2`, so it covers the delete at every content depth — even where the common content depth `m_{s_C} ≥ 2` (S8-depth, S8a, ASN-0036) outruns D-SHIFT's depth-2 realisation."

**Problem**: The note itself records that D-SHIFT — the only delete primitive it cites — is "established there only at text depth `#p = 2`." The lift argument establishes that *if* an edit's write-set is `Σ.M(d)` alone, *then* it frames `L, E, R`; that conditional is indeed depth-independent. But "it covers the delete at every content depth" asserts the *existence* of an M-only interior-span delete at depth > 2, which the cited foundation does not supply. At depth > 2 there is no established gap-closing delete (and K.μ⁻, which is depth-general, is tail-truncation, not interior-span deletion, so it cannot stand in). The phrase conflates "the lift applies at any depth" (true) with "there is a delete at every depth for the lift to cover" (not established). The note even flags the tension ("outruns D-SHIFT's depth-2 realisation") and then claims coverage anyway.

**Required**: Restrict the delete-stability statement to depth 2 where D-SHIFT holds, or state it conditionally ("for any M-only delete the model may provide at higher depths"), or acknowledge as a scope limit that interior-span deletion above depth 2 is not yet foundation-established. As written this is an overclaim — and, since RE-EDIT need only cover the operations the foundation actually provides, the depth-independence flourish is also avoidable.

### Issue 3: RE-DEF and RE-WHOLE carry inconsistent provisionality

**ASN-0131, Claims table**: RE-DEF returns `Σ.L(a).eᵢ = e` (status "introduced"); RE-WHOLE — "a surfaced endset is returned in full, *all* its spans" — is status "introduced (provisional)," and the Extent section says "we therefore hold RE-WHOLE provisional pending its resolution."

**Problem**: RE-DEF *encodes* whole-endset surfacing: it returns the full endset value `Σ.L(a).eᵢ`. RE-WHOLE names exactly that property. The two are logically equivalent for the surfaced endset. If Open Question 1 resolves to touching-spans-only, RE-DEF as written becomes false (it would have to return `e ⊆ Σ.L(a).eᵢ`, the touching slice). So RE-DEF is exactly as convention-dependent — and thus as provisional — as RE-WHOLE, yet only RE-WHOLE is marked. The status column is internally inconsistent.

**Required**: Either mark RE-DEF as encoding the provisional convention, or restate RE-DEF convention-neutrally (parameterizing the surfaced endset over the OQ1 choice) so that the definite claim and the provisional one no longer contradict.

## OUT_OF_SCOPE

The note's seven Open Questions correctly defer future territory (whole-vs-touching surfacing, multiplicity preservation, V-rendered answers, intersection-distributivity, non-co-resident link stores, type-slot/content matches, link-subspace regions) without smuggling claims about them into the body. RETRIEVEENDSETS also avoids claim-creep into the out-of-scope sibling operations: FINDLINKSFROMTOTHREE appears only as a contrast, RE-UNIT explicitly *withholds* counting and identity, and RE-SEL relates to `findlinks_V` by citation (F-V) rather than re-derivation. Nothing to add.

META: none — the note specifies an abstract query (state-level RE-DEF, soundness/completeness, arrangement-mediated stability) with guarantees an alternative implementation would also owe, so it is squarely a specification, not implementation mechanics.

VERDICT: REVISE
