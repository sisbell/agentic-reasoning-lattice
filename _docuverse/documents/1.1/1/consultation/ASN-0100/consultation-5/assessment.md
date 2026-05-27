# Channel Assignment — ASN-0100 review-5

**Date:** 2026-05-27 13:44

## Issue 1: FirstEmissionFreshness citation is too narrow for arbitrary k
Reason: The fuller chain machinery (ChainEnumerationInjectivity, ChainMembershipForOrigin, SubAllocatorAxiom.Disjointness, K.α freshness against Σ_k, P0 monotonicity) is already laid out in §Effect One of this same ASN. The fix is to swap in citations the ASN itself already establishes.

## Issue 2: L14 citation in Effect One reverses cause and effect
Reason: The proper discharge (SubAllocatorAxiom.Subspace + L0 + SC-NEQ) is in the same paragraph; the fix is a reframing of the lead-in citation. No external evidence or intent question is involved.

## Issue 3: S8★ preservation not explicitly verified
Reason: S8★ follows from M2 (DecompositionExistence; ASN-0058) on the per-state preconditions already verified in this ASN (S8-fin, S2, S3, S8a, S8-depth, S7b, S7c) plus TA5(c) (ASN-0034) for the Insertion region's I-adjacent run. The review supplies the proof sketch; all cited dependencies are pre-existing.

## Issue 4: shift(p, 0) convention not declared at first use
Reason: The convention is already used silently throughout the ASN and is consistent with OrdinalShiftBase (ASN-0058) per the review's own assessment. The fix is a notational declaration or a piecewise rewrite — purely an authorial choice.

## Issue 5: Empty-case K.α emission framing implicit about prior chain state
Reason: The semantic separation of dom(C) from dom(M(d)) is fixed by P0 (ContentPermanence; ASN-0047, already cited) and the substrate's two-stream architecture documented in §Background. K.α's two-branch emission predicate is in ASN-0093 (already cited). The fix is a clarifying sentence distinguishing the two conditions.
