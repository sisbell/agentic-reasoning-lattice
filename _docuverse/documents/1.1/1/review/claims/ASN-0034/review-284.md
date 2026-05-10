# Cone Review — ASN-0034/TA2 (cycle 8)

*2026-04-18 12:49*

### TumblerSub's ZPD citation explicitly scopes itself to "case (i)" but the precondition-consequence's case (ii) also consumes ZPD's defining property
**Foundation**: ZPD (ZeroPaddedDivergence) — supplies both the case-split clause (`zpd(a, w)` is defined iff the padded sequences disagree somewhere) and the minimality clause (when defined, `zpd(a, w)` is the *first* such disagreement position). TumblerSub's Depends already cites ZPD for case (i); TA2's previous-finding-driven update similarly counts ZPD at two distinct identification sites.
**ASN**: TumblerSub's precondition-consequence proof, case (ii):

> "Prefix divergence — `w` is a proper prefix of `a` ... The padded extension sets `wₖ = 0` for `k > #w` ... Since zpd is defined, the longer operand `a` has some nonzero component beyond `#w`; at `k = zpd(a, w)`, `aₖ ≠ 0 = wₖ`."

TumblerSub's Depends entry for ZPD reads: "ZPD (ZPD) — defines `zpd(a, w)` and supplies the ZPD–Divergence relationship identifying `zpd(a, w) = divergence(a, w) = k` **in case (i)**."
**Issue**: The case (ii) passage performs two ZPD-grounded steps that the citation does not enumerate. (1) *Non-emptiness*: the inference "zpd defined ⟹ some aᵢ ≠ 0 at i > #w" is the contrapositive of ZPD's case-split clause — if every padded position agreed, zpd would be undefined; combined with the prefix agreement `wᵢ = aᵢ` for `i ≤ #w`, the disagreement must lie at `i > #w` where padded `wᵢ = 0`, forcing `aᵢ ≠ 0`. (2) *Identification of k as past #w*: that the named `k = zpd(a, w)` actually falls at one of these `i > #w` positions (rather than somewhere within the prefix range) requires ZPD's minimality clause combined with the same prefix agreement — without minimality, the proof cannot conclude `aₖ ≠ 0 = wₖ` at the *named* k. The Depends entry's "in case (i)" qualifier explicitly excludes this case (ii) consumption, even though TumblerSub's NAT-zero entry separately enumerates a case (ii) site (entry (iv)) — the asymmetry leaves ZPD unchecked at a site where NAT-zero is checked. This parallels the previous TA2 finding's structure but applies to TumblerSub's own per-site accounting.
**What needs resolving**: TumblerSub must either (a) split the ZPD entry to count the case (ii) consumption as a second site (the non-emptiness inference from ZPD's case-split contrapositive plus the minimality-driven identification of `k > #w`), mirroring its own per-site accounting for T3 (sites (i) and (ii)), TumblerAdd (sites (i) and (ii)), and NAT-zero (four sites including case (ii)); or (b) restructure the case (ii) precondition-consequence to derive `aₖ ≠ 0 = wₖ` from a source that does not require ZPD's minimality (and reconcile this with TA2's parallel sub-case (ii), which now does cite ZPD for the same identification pattern). One per-site accounting rule per Depends block.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4027s*
