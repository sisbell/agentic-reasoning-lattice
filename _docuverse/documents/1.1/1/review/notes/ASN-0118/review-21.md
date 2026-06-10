# Review of ASN-0118

The substance is sound. I checked the resolution bridge (CP0), the transclusion frame (CP1), the placement/displacement tiling (CP2/CP3), the composite decomposition (append/empty vs. contraction-then-extension), and the provenance discharge (CP8) in detail, including boundary cases (empty destination, append, `j = 0`, self-transclusion) and the non-trivial link-discoverability wp. Each holds. In particular: the choice to ground single-subspace-ness in the content-residence precondition rather than ASN-0058's well-formedness/C0a is correct and necessary; the CP8 three-way split across J1★/J1'★/P2/P4★ (with the composite-boundary scoping of P4★) is careful and right; and the CP3c domain-closure postcondition correctly closes the S2 double-binding gap that the membership-style postconditions would otherwise leave open. The worked two-source example exercises both provenance branches. No correctness or completeness defects found.

The findings below are the accreted forward-reference prose the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: The I3 caveat and tiling deferral are stated twice, nearly verbatim
**ASN-0118, "The COPY operation" (CP3a discussion) and "The destination's prior arrangement is preserved"**:

Location A: "I3 does *not* establish the function-ness, no-holes, contiguity, and sequentiality of COPY's actual `Σ'.M(d)`: it describes only the shift, leaving the gap `[p, p+W)` empty in its `M'(d)`, whereas COPY fills that gap with the placement positions (CP2). Those properties rest instead on the tiling argument given later under prior-arrangement preservation..."

Location B: "COPY fills that gap with the placement positions (CP2), so the function-ness and no-holes of COPY's actual `Σ'.M(d)` are *not* established by the I3 lemmas: they rest on the tiling argument below..."

**Problem**: The two passages make the identical three points (I3 supplies I3-VP/I3-VD/I3-fin for the *shifted* positions; I3 leaves the gap empty, so it does **not** establish function-ness/no-holes; those rest on the tiling argument). The disjointness-by-shift fact (TS4 at A, TS1/TS4 at B) is likewise duplicated. Location A is a forward-reference preview of Location B, and a reader must reconcile the two to confirm they say the same thing.
**Required**: State the I3 caveat and the shift-disjointness fact once, at the site where the tiling argument is actually delivered (Location B). At CP3a, cite I3 for the shift's per-position facts and reference the tiling result without re-arguing it.

### Issue 2: Essay content in the claims table
**ASN-0118, "Claims Introduced" table**: CP1 — "The boundary distinguishing transclusion from replication"; CP11 — "Replication would collapse it to `⦃d,…,d⦄` — the reveal that separates reuse from replication".
**Problem**: Rhetorical characterization in a structural slot. The table should carry the claim; this framing already appears (correctly) in the prose sections ("the transclusion frame," "the boundary between reuse and replication").
**Required**: Replace the editorial tails with the claim content, or drop them.

## OUT_OF_SCOPE

### Topic 1: Width-preservation under partial binding, mixed-depth assembly, link-subspace transclusion
**Why out of scope**: These are correctly deferred in the ASN's own Open Questions. ASN-0058's C2 genuinely does not survive partial binding, but no in-scope claim (CP2/CP3 are stated in terms of the resolved count `W`) depends on it; mixed source depths and link-subspace placement are new operational territory. No action needed in this ASN — flagging only so the reviser does not pull them in.

VERDICT: REVISE
