# Review of ASN-0102

I read the note as a complete specification of COPY as a single elementary transition, checked every introduced claim X1–X16, the four worked examples, the weakest-precondition computation, and the discharge of all conjuncts of `ExtendedReachableStateInvariants`, the composite-boundary properties, and `ExtendedTransitionInvariants` (P3).

## Findings

The proofs hold up under scrutiny. The points I tested hardest:

- **wp(COPY, S3★)** is genuinely non-trivial: the three-class partition (unmoved / displaced / copied) correctly reduces S3★ to a membership obligation on the copied region only, discharged at the pre-state by ASN-0058 C1 via the load-bearing P1 conjunct `subspace(u_i) = s_C`. The relation is correctly stated as equality (`dom(Σ'.C) = dom(Σ.C)`), not containment.
- **X16's tiling** `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W] = [1, n_S+W]` is exact, with no gap and no overlap, and S8a is independently verified for the *interior* copied positions and the displaced images (not just the ValidInsertionPosition anchor `v`). The shift's effect on the last component only (via OrdShiftHom) is used correctly.
- **X7** correctly separates "freed slots" `[p, n_S]` from "occupied portion of the copy target" `[p, min(n_S, p+W−1)]` and rests the no-overwrite conclusion on range disjointness rather than on full pre-state occupancy — the right argument.
- **X8** does not appeal to maximality alone for within-reference non-coalescence; it first establishes V-adjacency from span well-formedness + C0a, then derives non-I-adjacency. The constructed-`k` vs. canonical-`≤k` distinction is kept clean.
- **X14** discharges every listed conjunct. The J1'★ Old-branch correctly uses P4★ at the pre-state boundary (justified from trace position, not from COPY's forward effect — not circular), and the idempotent `Σ.R ∪ {…}` interaction is sound. C1b/C1c, S8★ re-derivation, S4, P6, and ActivatedEmission are each addressed by the correct mechanism rather than lumped.
- The four worked examples (interior cross-origin, self-transclusion with `Old ≠ ∅`, empty-subspace first insertion with `New = A`, and append with absent trailing boundary) exercise the genuinely distinct boundary configurations, and the arithmetic checks out in each.

Run-splitting at the insertion point (a pre-state run straddling `p` becomes two post-state runs) is correctly sidestepped: X16 establishes V-contiguity directly via tiling and S8★ is re-derived from S8's hypotheses, not from preserving pre-state runs.

Foundation usage is consistent — all cross-references (ASN-0034/0036/0047/0058/0093) are to foundation ASNs, and the note reuses their definitions rather than reinventing them. Out-of-scope mechanics (INSERT displacement internals) are explicitly deferred.

I found no missing edge case, no proof-by-"similarly", and no checkmark standing in for an argument. The open questions defer genuine future territory.

VERDICT: CONVERGED
