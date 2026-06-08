# Review of ASN-0102

This is a strong, thorough specification — the operation is fully framed over all five state components, the wp computation for S3★ is genuine, and the worked examples deliberately exercise the discriminating cases (cross-origin non-merge, self-transclusion overlapping the displaced region, empty-subspace first insertion, append, and coalescing). The correctness core (X1, X3, X7, X16) and the invariant discharge in X14 are sound. My findings are confined to the forward-reference/meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Use-site inventory re-enumerating the foundation vocabulary
**ASN-0102, "Definition of COPY" / Amendment to ValidComposite★**: "We amend ValidComposite★'s atomic enumeration (ASN-0047) — `K.α` (amended), `K.δ`, `K.λ`, `K.μ⁺` (amended), `K.μ⁺_L`, `K.μ⁻` (amended), `K.ρ` — to admit COPY..."
**Problem**: The full re-listing of ASN-0047's atomic transition kinds with "(amended)" tags is a use-site inventory of foundation content that does not advance COPY's definition. The advancing fact is only that COPY is added as a new atomic kind, restricted to standalone composites.
**Required**: Reduce to the advancing statement — "COPY is added to ValidComposite★'s atomic vocabulary (ASN-0047) as a new transition kind, admissible only as a length-1 (standalone) composite" — and drop the re-enumeration.

### Issue 2: Redundant self-restatement of the standalone restriction
**ASN-0102, Amendment to ValidComposite★**: "COPY occurs only as a *standalone* (length-1) composite: COPY must be the sole step of its composite."
**Problem**: The clause after the colon restates the parenthetical "(length-1)" in different words — two phrasings of one constraint.
**Required**: Keep one phrasing.

### Issue 3: X14 crams ~20 distinct discharge obligations into one running paragraph
**ASN-0102, X14**: the single paragraph discharges J0, the New/Old setup, J1★, J1'★, P7 (grounding + well-typedness), P4★, then "the remaining invariants ... by vacuity" enumerates L0/L1/.../CL-UNIQ/P8/NodeLineage/ActivatedEmission, S2/S8a, S3★, S3★-aux, D-CTG★/D-MIN★/D-SEQ★, S8-depth, S7a–S7d/C-fin, S8-fin, C1b, C1c, S8★, S4, P4a, P7a, and finally P3.
**Problem**: Each is a distinct obligation with its own justification; running them together as one prose block defeats the "show each case" standard by making per-obligation verification require unpicking the wall of text. This is the slot where accreted invariant-discharge prose compounds.
**Required**: Break X14 into a short enumerated list (one line/clause per invariant or invariant group), each naming the conjunct and its one-line discharge. The content is correct and complete — this is a structural/verifiability fix, not a logical one.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, containment when a reference-holder is itself re-sourced, time-varying views, identity when the allocating document is unreachable) are correctly future territory and appropriately placed.

VERDICT: REVISE
