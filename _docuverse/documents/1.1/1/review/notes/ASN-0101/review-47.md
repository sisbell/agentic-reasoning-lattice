# Review of ASN-0101

This ASN is mathematically mature — D0 through D11 are carefully derived, boundary cases are enumerated thoroughly, and the worked examples genuinely exercise the claims they cite. I found no correctness or missing-case defects. The findings below are all anti-bloat / prose findings, consistent with the `review-mode.anti-bloat` classifier this note carries.

## REVISE

### Issue 1: LP-family extension paragraph leads with a downstream-consumer inventory
**ASN-0101, D10, "LP-family extension under DELETE"**: "ASN-0098's projection apparatus — the per-step lemmas LP2–LP14, the discoverability and tightness lemmas LP16–LP21, and the substrate-structural lemmas LP-Sub, LP-Fin, and LP-Fin Corollary — is stated over a vocabulary that predates DEL... no new LP-family lemma is required."

**Problem**: This is a use-site inventory followed by a generic four-bucket exhaustiveness argument ("either is state-relative, is purely tumbler-structural, threads through a prefix... or concerns a non-DEL operation"). The buckets cite no specific lemma; the upfront enumeration of every LP lemma does not advance the closure argument — it only catalogues what is being closed over. This is the "definition/claim introduction enumerates downstream consumers" pattern.

**Required**: Reduce to the load-bearing content: ASN-0098's projection lemmas close over the DEL-extended vocabulary because DEL fixes both stores (D2, D3), frames non-`d` arrangements and the unaffected subspace (D5, D6), and D9/D11 supply the DEL-specific projection facts. Drop the lemma roll-call and the generic bucket taxonomy.

### Issue 2: Enabledness-guard rationale restated at every wp bullet
**ASN-0101, D11 and its worked verifications**: The justification for conjoining `enabled(DEL[d, σ])` recurs at nearly every bullet — "as LP12a... conjoins," "without the guard, a pre-state at which DEL is inapplicable could spuriously satisfy the pullback clause," "the enabledness guard remains, since the postcondition can be guaranteed only when DEL actually runs" — and each worked-example verification re-opens with "with `enabled(DEL[d, σ]) = true` here the pullback factor is...".

**Problem**: The reason the guard is present is a single fact about partial deterministic commands. Restating it per bullet and per example is repeated defensive justification that the reader must skip past.

**Required**: State the enabledness-guard rationale once (it is already given in full in D11's opening), then write each wp bullet as guard-plus-pullback without re-deriving why the guard is there. In the worked examples, note once that DEL is enabled at the example pre-state and drop the per-wp "with enabled = true" preamble.

### Issue 3: D8 and D10 both carry the P4★/P4a/P7a "neutral-to-helpful" argument
**ASN-0101, D8 Group (iii) closing** establishes DEL "cannot break" P4★/P4a/P7a via monotone-shrinking and store/provenance fixing. **D10, "Composite-boundary obligations"** restates: "By D8, DEL is neutral-to-helpful for all three — content-subspace-monotone-shrinking... and store/provenance-fixing... — so no DEL step... can turn a boundary-satisfying state into a violating one."

**Problem**: D10 already cites D8, but then re-characterizes D8's conclusion ("content-subspace-monotone-shrinking and store/provenance-fixing") rather than simply invoking it. The descriptive content appears in two places.

**Required**: In D10, reference D8's conclusion by name and state only the composite-level addition (affirmative establishment is the work of non-DEL steps). Do not re-describe the mechanism by which DEL is neutral.

## OUT_OF_SCOPE

None. The ASN correctly scopes recoverability/versioning, INSERT, and COPY to future work via its Open Questions.

VERDICT: REVISE
