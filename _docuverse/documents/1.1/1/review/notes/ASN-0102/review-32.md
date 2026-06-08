# Review of ASN-0102

This is a strong, heavily-revised note. The formal core — the three-class arrangement rewrite, the `wp(COPY, S3★)` reduction, the tiling argument of X16, and the foundation-invariant discharge in X14 — is rigorous and the edge-case coverage (empty subspace, append, self-transclusion, cross-origin) is genuinely thorough. The issues below are about concrete verification depth and one redundant derivation, not correctness errors I could find.

## REVISE

### Issue 1: The discriminating merge behavior (X8, X12) is stated but never exercised by any worked example
**ASN-0102, X8 / X12 and the four worked examples**: X8 claims "canonical block count is `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent"; X12 gives leading/trailing absorption conditions that fire "exactly when" I-adjacency holds.
**Problem**: All four worked examples land on the *non-merging* side of these claims. Example 1 (cross-origin) has `canonical = k = 2` because origins differ; Examples 2–4 have `k = 1`. X12's absorption is checked in Example 1 and explicitly noted as "generically neither fires," and no later example fires it either. So the most error-prone, discriminating sub-cases — an I-adjacent inter-reference coalescence (`canonical < k`) and a *fired* leading/trailing boundary absorption with surrounding content — are derived in prose but never verified against a concrete instance. The review standard requires key postconditions to be checked against at least one specific scenario; here the *non-trivial* half of X8 and X12 is the half left unexercised.
**Required**: Add (or extend) a worked example exhibiting (a) two adjacent references sharing an origin and abutting in I-space so the inter-reference boundary coalesces (`canonical = k − 1`), and (b) a leading or trailing boundary that actually absorbs (e.g. predecessor I-reach `= a_1` with shared origin), so the merge predicates are shown firing, not merely shown failing.

### Issue 2: X8's within-reference non-coalescence re-derives a guarantee `resolve` already supplies
**ASN-0102, X8, first bullet ("Within a single reference, consecutive runs never coalesce…")**: the paragraph re-proves, via run maximality over the V-contiguous restriction domain, that consecutive blocks of a single reference are non-I-adjacent.
**Problem**: `resolve(d_s, σ)` (ASN-0058) is defined to return the *maximally-merged* block decomposition (C1a / M12). Consecutive blocks of one reference are therefore non-I-adjacent and (on the V-contiguous domain) V-adjacent by that construction. X8's first bullet reconstructs this established fact rather than citing it, so the only genuinely new content in X8 is the *inter*-reference boundary analysis. The re-derivation is correct but is the kind of foundation-fact re-proof the note should avoid.
**Required**: Replace the within-reference paragraph with a one-line citation that `resolve` already yields maximally-merged, V-adjacent per-reference blocks, and keep only the inter-reference-boundary argument (the actual new content).

## OUT_OF_SCOPE

### Topic 1: Discoverability/projection consequences of copied content under later displacement
The first and fourth Open Questions (continued discoverability of a copied address after subsequent displacement; identity when the allocating document becomes unreachable) belong to the link-projection layer (ASN-0098), not to COPY's state contract. Correctly deferred.

VERDICT: REVISE
