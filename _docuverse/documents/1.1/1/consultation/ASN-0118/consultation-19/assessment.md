# Channel Assignment — ASN-0118 review-19

**Date:** 2026-06-09 17:27

## Issue 1: CP3c and CP6 carry parallel necessity-justification paragraphs that make the same point twice
Reason: Internal. The fix is pure deduplication — both justification paragraphs already exist in the ASN, the closure principle (postconditions must pin the per-document domain so S2/S3★ are dischargeable without the exhibited composite) is already worked out, and the task is to state it once and reduce CP3c/CP6 to their formal content. No design intent or implementation evidence is at stake.

## Issue 2: The "S3★-over-bound-positions, not ASN-0058 C1; ordinal-level not required" design-choice justification is repeated across three sites
Reason: Internal. The technical basis (single-subspace + S3★ over bound positions, C1's full-binding dropped, depth-parametric) is already fully stated at all three sites — including the existing Gregory-sourced `acceptablevsa` citation — so consolidating it into the resolution section and trimming the V-spec and CP0(a) instances requires no new consultation.

## Issue 3: The composite-validity argument discharges K.μ⁻ and K.μ⁺ elementary preconditions explicitly but leaves K.ρ's unstated
Reason: Internal. K.ρ's elementary precondition is defined in ASN-0047, and every ingredient of its discharge (`cᵢ ∈ dom(C)` by CP0(a) + CP1's content frame; `d ∈ E_doc` by the destination hypothesis) is already present in the ASN — the review itself spells out the one line to add.
