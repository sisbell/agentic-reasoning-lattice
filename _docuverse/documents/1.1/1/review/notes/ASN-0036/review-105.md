# Review of ASN-0036

## REVISE

### Issue 1: Triplicate derivation of subspace preservation under shift

**ASN-0036, S7c Consequence (b), subspace_I postcondition (c), and ShiftPreservation conclusion (iv)**: All three establish the same conclusion — `subspace_I(shift(a, k)) = subspace_I(a)` — with substantively overlapping derivations.

**Problem**: The position-arithmetic step `#a − δ + 1 < #a` (equivalently `#a − #E(a) + 1 < #a`) is derived three times, each invocation chaining the same NAT facts: `1 < δ` from `δ ≥ 2` (via NAT-addcompat's strict successor `1 < 2` plus NAT-order's <-≤ mixed transitivity); `(#a − δ) + 1 < (#a − δ) + δ = #a` (via NAT-sub's left/right inverses, NAT-addcompat's left order compatibility, NAT-cancel's strict-to-strict lift); then TumblerAdd's prefix rule. The dependency chain itself — subspace_I (c) and S7c (b) both forward-reference ShiftPreservation — signals that the natural organization is the reverse of the textual one.

**Required**: Consolidate to a single derivation, ideally in ShiftPreservation as conclusion (iv). Either (a) reorder so ShiftPreservation precedes S7c and subspace_I, with (b) and (c) reduced to brief citations; or (b) remove the position-arithmetic re-derivations from S7c (b) and subspace_I (c), retaining only the citation. The current "three independent presentations" structure violates "prove once, cite elsewhere" and risks divergence under future revision.

### Issue 2: Misleading S7b dependency description in S8's Formal Contract

**ASN-0036, S8 Formal Contract, Depends section**: "S7b (Element-level I-addresses) — supplies zeros(a) = 3 for the singleton-run construction's structural well-formedness"

**Problem**: The proof body explicitly contradicts this attribution: "No structural facts about a beyond its existence are invoked by the existence argument: neither S7b (zeros(a) = 3) nor S7c (#E(a) ≥ 2) is needed at k = 0, since both shifts are identities." S7b is invoked only by the run-corollary (via ShiftPreservation) at k ≥ 1, which is vacuous on the singleton witness exhibited in the proof.

**Required**: Re-attribute S7b in the Formal Contract to the corollary, not to the singleton-run construction. E.g.: "S7b — required by the run-corollary (via ShiftPreservation) for k ≥ 1 cases; not invoked by the singleton-run existence construction, which only uses k = 0 where shifts are identities."

VERDICT: REVISE
