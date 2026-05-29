# Channel Assignment — ASN-0036 review-147

**Date:** 2026-05-29 01:54

## Issue 1: "attribution is structural, not detachable metadata" asserted three times
Reason: Pure deduplication — removing two of three restatements requires no design intent or implementation evidence, only the ASN's own text. Internal.

## Issue 2: S7 body prose pre-proves the proof's "Uniqueness across documents" step
Reason: The derivation already exists in S7d's postcondition and the S7 proof; dropping the body restatement is an internal edit needing no external channel. Internal.

## Issue 3: S8 conjunct (b) "definition, not a theorem" stated four times
Reason: Consolidating a status clarification that already appears in the ASN is purely editorial, derivable from existing content. Internal.

## Issue 4: ValidInsertionPosition postcondition (b) asserted without derivation
Reason: The one-line derivation follows mechanically from the explicit form `v = [1, ..., 1+j]` already in the ASN — every component ≥ 1, so `zeros(v)=0`. No design intent or implementation evidence needed. Internal.
