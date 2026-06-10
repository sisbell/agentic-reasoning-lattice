# Channel Assignment — ASN-0114 review-8

**Date:** 2026-06-09 21:08

## Issue 1: F5's second qualification paragraph restates the first and previews a section that already covers it
Reason: Pure editorial deletion of a redundant paragraph whose content-identity point is already made in Para 1 and whose forward pointer duplicates a deferral the intro and the boundary section already carry. No design intent or implementation evidence is at issue — the rendering-vs-recorded distinction is already present in the ASN and need only be left to the boundary section.

## Issue 2: F6's disclosure paragraph enumerates the non-conforming-address carve-out three times
Reason: Editorial consolidation only. The carve-out (node/user-level or non-T4-valid interior ⇒ no document field) is already grounded in the ASN's own substrate (L4 EndsetGenerality, T4 field projections, the coverage-as-half-open-interval definition); stating it once rather than thrice changes no claim and needs no external channel.

## Issue 3: the wp analysis computes only trivial cases, omitting the one tied to F7
Reason: Internal derivation. The missing wp line and its `eᵢ = ∅` conjunct follow from claims already in the ASN — F0's precondition, F7's empty/invalid split, and ASN-0053 S2 forcing ⟨⟩ as the unique empty-coverage witness — all of which the note already cites; no design intent or implementation evidence is required.
