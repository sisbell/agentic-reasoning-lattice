# Review of ASN-0071

The mathematics here is sound. PC, PC-RANGE, and F-DEEP are derived rigorously, the case splits on `#v` relative to `#u` are complete, and the worked scenarios verify the key postconditions against concrete states (single-address, multi-address, multi-source dedup, cross-depth capture, and the deep-anchor dual). The boundary handling — exclusive reach `r ∉ ⟦σ⟧`, empty `Q`, empty content subspace, source depth `≠ #u` — is genuinely covered. My findings are confined to the anti-bloat patterns this note is flagged for.

## REVISE

### Issue 1: Σ-reachability justified twice
**ASN-0071, A worked scenario**: The preamble to step 1 states "Each precondition is discharged by the prior state; we narrate the result," and the post-step-13 *Reachability.* paragraph then re-states the same argument for the same construction: "Each step above is a standard allocate–place–record … composite … with its precondition discharged by the prior state. A reachable state extended by such composites remains reachable."
**Problem**: Two paragraphs make the identical reachability argument for the single state `Σ` (the steps-14–15 note is separate, covering `Σ⁺`). This is the "two paragraphs say the same thing in different words" pattern the anti-bloat mandate targets.
**Required**: Keep one reachability statement for `Σ` (the closing *Reachability.* paragraph suffices); drop the redundant preamble clause.

### Issue 2: Prose gloss restates the `iaddrs_one` formula and drifts to `find`
**ASN-0071, Resolution**: Immediately after the formal `iaddrs_one` definition: "`iaddrs_one(d_s, σ)(Σ)` is the set of I-addresses `d_s`'s arrangement assigns to span positions, deduplicated, with any span position absent from `dom(M(d_s))` quietly omitted (F-FILT). Since `find` is set-valued, order and multiplicity are discarded."
**Problem**: The first sentence restates the set-builder already given one line above; the second discusses `find` (not yet defined) inside the `iaddrs` section — topic drift plus a forward reference. Neither advances the reasoning.
**Required**: Delete the restatement. If the F-FILT (silent-omission) point is worth surfacing here, keep only that half-sentence and move the set-valuedness remark to *The operation*, where `find` is defined.

## OUT_OF_SCOPE

### Topic 1: Relationship to the historical containment relation `R`
**Why out of scope**: The currency contract (F-CUR) deliberately reads only current `M`, and the Open Questions already defer the `find`-vs-`R` relationship and the contraction-transition invariant to future work. Correctly excluded.

VERDICT: REVISE
