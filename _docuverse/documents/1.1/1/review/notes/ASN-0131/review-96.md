# Review of ASN-0131

I worked through every introduced claim and re-derived the load-bearing ones. The mathematics is sound: RE-NCD's separator-agreement proof is robust across element-field depths; RE-ADDR's two branches (retraction vs. self-retraction) are exactly characterised; RE-UDIST's factoring through the region-independent pool `Avail(Σ)` is correct, as is the necessary-and-sufficient intersection condition in RE-UDIST-∩ (both obstruction constructions earn their place — the injective one shows the obstruction is intrinsic to the `touch` existential, not to non-injectivity); RE-CWP's wp is correctly derived with the right `R = ∅` boundary; the worked instance exercises each distinctive postcondition and computes correctly; and the stability section covers the full ASN-0047 vocabulary. Boundary cases (empty image, no addressable links, empty endset slot, `R = ∅`, self-retraction) are all handled. The findings below are anti-bloat items, flagged at source per the `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: Accreted, misattributed gloss on the R-Scope citation
**ASN-0131, §Stability ("Under retraction")**: "which meets the prefix-antichain `dom(Σ'.L)` (above) in `ℓ` alone (R-Scope SingleTupleScope, ASN-0086, here independent of the retraction's arity since the scope is fixed by the to-set and the antichain, not the tuple's slot count)"

**Problem**: The bare citation "R-Scope SingleTupleScope, ASN-0086" already discharges `{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}` for target `ℓ`. The added clause re-derives R-Scope's own caveat (R-Scope states "*arity-independent*: it holds regardless of `|Σ.L(a)|`"), so it does not advance the argument. Worse, it misidentifies the relevant arity: R-Scope's arity-independence is in the **target** link's arity `|Σ.L(ℓ)|`, whereas the gloss — "the retraction's arity … the tuple's slot count," read against the immediately following "the fresh retraction tuple `b`" — points at the retractor `b`, whose arity is fixed at 3 by `Nullify`, making independence-in-`b`'s-arity a non-statement. A reader must skip the parenthetical to follow the claim.

**Required**: Delete the parenthetical, leaving the R-Scope citation to carry the step. If independence in the *retracted* link `ℓ`'s arity is worth noting, say "for `ℓ` of any arity" — but that is already inside R-Scope.

### Issue 2: Restatements within adjacent material
**ASN-0131, §Stability ("Under retraction"), and §"Fresh emissions" / RE-ADDR table**:
- "Withdrawing `ℓ` is realised as `Nullify(…)`" (para 2) is restated one paragraph later as "(`Emit_Θ(…, ∅, …)`, ASN-0086), withdrawal being realised as a `Nullify`" (para 3).
- "nullified(Σ) is an existential over that slice `L_Θ^Σ ⊆ Σ.L` alone" (§Fresh emissions setup) is restated in the RE-ADDR table as "(scoped to the retraction slice `L_Θ`, all that `nullified` consults)".

**Problem**: The second occurrence in each pair adds nothing the reader did not just receive; this is the micro-duplication the anti-bloat mode flags as compounding across cycles.

**Required**: Keep one occurrence of each fact; drop the parenthetical echoes.

## OUT_OF_SCOPE

Nothing to flag. The seven Open Questions defer genuinely-future territory (touching-spans return value, multiplicity preservation, the rendered/V-order mode, a structurally-checkable intersection-equality condition, non-co-resident link stores, type-slot-against-content matching, link-subspace regions) rather than papering over gaps in this note. The note cites ASN-0127's image and existence/discovery machinery (F-IMG, F-V, D-NONMONO, D-CWP) and ASN-0086's retraction layer rather than rebuilding either, and defines no claims for the out-of-scope sibling operations.

VERDICT: REVISE
