# Review of ASN-0058

I checked the proofs for rigor and scanned for the forward-reference/meta-prose accretion the `review-mode.anti-bloat` classifier targets. The mathematics is sound throughout — M-int, M16a, M12a/M12b, C0, and C2 all carry their cases explicitly (boundary cases `k=0`, `n=1`, empty arrangement, prefix-confinement infinitude are each discharged). The findings below are residual framing/essay prose, not correctness gaps.

## REVISE

### Issue 1: Inflated authorial framing at M13
**ASN-0058, M13 (SharedContent), opening sentence**: "We have been careful to call the V→I function a 'mapping' rather than a 'permutation' in the strict algebraic sense."
**Problem**: This is self-referential framing about the authors' word choice, not object-level content. The load-bearing statement is the next sentence ("M(d) is not necessarily injective"). The precise reader has to step past the framing to reach the claim — exactly the meta-prose the anti-bloat pass removes.
**Required**: Drop the "We have been careful to call…" sentence; open M13 directly with the non-injectivity statement that the claim actually formalizes.

### Issue 2: Out-of-scope deletion exegesis as motivation under M15
**ASN-0058, M15 (MappingIndependence), closing paragraph**: "Deletion is an *arrangement* operation — it modifies `M(d_1)` — and it does not propagate to `M(d_2)`. The frame condition on split and merge is sharper still…"
**Problem**: Operation effects on arrangements (INSERT/DELETE/COPY/REARRANGE) are listed OUT OF SCOPE for this ASN. The Nelson quote grounds M15, but the subsequent exegesis asserts DELETE's behavior and contrasts it with split/merge as essay-style motivation that advances none of M15's conjuncts (a) or (b). It is commentary occupying a structural slot.
**Required**: Keep the Nelson quote as evidence for M15; remove the DELETE behavioral exegesis. The "split and merge do not modify `M(d)`" point is already stated and proved in M6f/M7f and need not be re-argued in prose here.

### Issue 3: Proof-method narration at M-int
**ASN-0058, M-int (TumblerIntervalCharacterization), component-`m` reduction**: "We split on `k` because TumblerAdd is defined for ordinal displacements `δ(k, m)` only when `k ≥ 1`; the boundary case `k = 0` is governed by OrdinalShiftBase instead."
**Problem**: This narrates *why* the proof case-splits rather than performing the split. The two cases (`k = 0`, `k ≥ 1`) that immediately follow already make the structure self-evident; the explanatory sentence is bookkeeping about the argument, not the argument.
**Required**: Delete the sentence and let the labeled cases stand on their own.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to the block algebra and resolution; it cites only foundation ASNs (0034, 0036, 0053) and does not stray into operations, links, or versioning.

VERDICT: REVISE
