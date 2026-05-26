# Channel Assignment — ASN-0087 review-3

**Date:** 2026-05-26 12:19

## Issue 1: Notational overloading of ⊕ in composite expression
Reason: Pure notational fix. The replacement options (`;`, "then") are derivable from the ASN's own content; no theory or implementation evidence is needed to choose new sequencing notation.

## Issue 2: M-Inv omits P4a, P7a, P3, M0, M1
Reason: All invariants are defined in ASN-0047 and ASN-0093 (already cited). The reviewer notes preservation is trivial under the unchanged-component frames; the verifications are mechanical and derivable from the ASN's existing frame claims.

## Issue 3: Freshness argument cites only ChainEnumerationInjectivity
Reason: ChainMembershipForOrigin is an existing ASN-0093 axiom; the reviewer supplies the exact argument structure. The strengthened citation chain is derivable internally without recourse to design intent or implementation.

## Issue 4: L1c chain T4-validity preservation lacks explicit zero-count tracking
Reason: Zero-count bookkeeping follows mechanically from TA5a (ASN-0034, already cited) applied step-by-step. The reviewer provides the exact values; the fix is internal proof annotation.

## Issue 5: M-Disc claim is a restatement of LP12 without MAKELINK-specific content
Reason: Choice between deletion and strengthening is a structural decision about claim novelty within this ASN. Whichever option is chosen, the content is already present (LP12 is at ASN-0098, MAKELINK-specific consequences derive from M-WP and M-Effect).

## Issue 6: M-Inv conflates per-state and transition invariants
Reason: ASN-0047 explicitly defines ExtendedReachableStateInvariants vs. ExtendedTransitionInvariants. The reorganization follows that existing taxonomy directly; no external input required.

## Issue 7: K.μ⁺_L precondition `subspace(v_ℓ) = s_L` not explicitly discharged
Reason: Discharge is by inspection of the constructed `v_ℓ = [s_L, k]` plus the already-cited LinkVPositionDepthAxiom (ASN-0047). Purely an explicitness fix internal to the proof.
