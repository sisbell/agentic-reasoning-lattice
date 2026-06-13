# Channel Assignment — ASN-0123 review-30

**Date:** 2026-06-13 14:43

## Issue 1: The cross-owner "single mint / no intermediate account" rationale is stated three-plus times
Reason: Pure deduplication of an argument the ASN already establishes correctly (single-mint via the account-tier restriction, node-tier exclusion via P1/P-tier). Choosing where the proof lives (V0) and where to cite is derivable from the ASN's own content; no design-intent or implementation evidence is at stake.

## Issue 2: V-WF previews and duplicates V9's structural derivation
Reason: Internal proof-bookkeeping fix — the finding's own correction (V-WF's composite-validity argument consumes Document(v), freshness, and S3★, not coverer-maximality) is verifiable from the ASN's stated K.μ⁺ precondition and J0/J1★/J1'★ couplings. Deciding what V-WF establishes vs. defers to V9 needs nothing beyond the ASN.

## Issue 3: The "cross-owner derivation is recoverable only via V9w, never the registry" argument is made twice
Reason: Consolidating a conclusion the ASN already proves (severance V9 + symmetric witness V9w) into its natural home (VD's derivation-decidability fragment) and citing from V7. No appeal to design intent or implementation evidence is required.
