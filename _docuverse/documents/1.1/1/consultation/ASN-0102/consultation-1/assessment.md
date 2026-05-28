# Channel Assignment — ASN-0102 review-1

**Date:** 2026-05-28 14:02

## Issue 1: Target subspace never constrained to s_C; wp computed against S3, not S3★
Reason: The formal patch (S3★ + C1 force content addresses into s_C) is derivable, but whether COPY is *defined only* over the content subspace or is meant to be total over subspaces (including placing links into s_L) is a design-intent/scope question.
Nelson question: Is COPY intended to operate exclusively on the content subspace, or is placement of existing content into the link subspace also within its intended scope?

## Issue 2: Post-state density (D-SEQ / no V-gap) is asserted, never derived
Reason: The required derivation (unmoved `[1,p)`, copied `[p,p+W)`, displaced `[p+W, n_S+W]` jointly tiling `[1, n_S+W]`) follows entirely from the shift definition and D-SEQ already in the ASN and ASN-0036/0058. Internal.

## Issue 3: Only the leading boundary absorption is considered; X12's "and only then" is unjustified
Reason: The merge condition M7 (ASN-0058) is symmetric in V/I-adjacency and applies equally to the trailing boundary; correcting "and only then" is formal manipulation of an already-cited rule. Internal.

## Issue 4: No concrete worked example
Reason: A worked instantiation exercises only the ASN's own definitions (resolve, B_copy, shift, M7/M16) — no external intent or evidence is required to construct it. Internal.

## Issue 5: Precondition is scattered and incomplete
Reason: Source resolvability (ASN-0058 C1/C2), the empty-subspace first-insertion case (ValidFirstInsertionPosition, D-MIN, S8-depth in ASN-0036), and `W ≥ 1` are all formally available in the cited foundations; consolidation is internal.

## Issue 6: `resolve(R)` evaluation state not pinned (self-transclusion snapshot)
Reason: Pinning to `resolve_Σ(R)` and deriving the snapshot from the SequentialTransitionAxiom (ASN-0047/0093, precondition read against `Σ`) replaces the Gregory citation with the formal semantics already referenced. Internal.

## Issue 7: `wp(COPY, S3) ⊇ …` notation imprecise and partial
Reason: Restating wp as a biconditional over all post-state mappings of `d` (copied must pre-exist; displaced preserved by X1) is a purely notational/logical correction within the ASN. Internal.

## Issue 8: X8 "exactly k blocks" ignores cross-reference coalescence
Reason: The canonical (maximally-merged) count is determined formally by M7/M12 (ASN-0058), but the claim is grounded in cited implementation block-count evidence ("one DOCISPAN per sporgl," Q11/Q18); reconciling the stored count with the canonical count requires knowing whether the implementation coalesces cross-reference I-adjacent spans.
Gregory question: Does `insertspanf`/`docopy` coalesce I-adjacent, V-adjacent spans across distinct content references into a single entry, or always emit one span entry per resolved run regardless of inter-reference I-adjacency?
