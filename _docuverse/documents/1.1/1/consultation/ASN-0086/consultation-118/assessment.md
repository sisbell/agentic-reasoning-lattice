# Channel Assignment — ASN-0086 review-118

**Date:** 2026-05-31 22:49

## Issue 1: R6b's universal omits the `a ∈ A_rel` restriction, so the stated lemma is false for non-link `a`
Reason: Fix is internal — R6a already performs exactly the missing step (restrict to `a ∈ A_rel^Σ`, then L12a discharges `a ∈ A_rel^{Σ'}`); the ASN supplies the pattern and the definitions needed. No design intent or implementation evidence is required.

## Issue 2: Derivation inventories and triplicated forward-references (anti-bloat)
Reason: Fix is internal — purely an editorial relocation of premise lists into proofs and de-duplication of the clause-(b) contingency statement; no semantic content changes.

## Issue 3: Notational slip in the worked sketch
Reason: Fix is internal — the chain is already named `A_L(d)` throughout the note; replacing the undefined `A_{a₁}` is a mechanical correction.
