# Channel Assignment — ASN-0047 review-310

**Date:** 2026-06-02 01:02

## Issue 1: Dangling reference to an undefined property "P4"
Reason: Purely a notation/internal-consistency fix. The unscoped bound `Contains(Σ) ⊆ R` is already stated within this ASN (J4 section); the repair is to cite it correctly or drop the phantom `P4` label — no design intent or implementation evidence is at stake.

## Issue 2: The "imposed (not derived) / K.α-alone" justification is restated near-verbatim in three sites
Reason: Anti-bloat deduplication of repeated meta-prose; consolidating to the ValidComposite★ definition and cross-referencing is an editorial move fully internal to the ASN.

## Issue 3: J3 self-sufficiency leans on K.μ~-RANGE without surfacing the intermediate-state P4★ behavior
Reason: The required clause (K.μ⁺ step re-adds only already-ranged addresses, so J1★ is vacuous and no K.ρ is needed) follows directly from K.μ~-RANGE and the K.μ⁻+K.μ⁺ decomposition already proved here; derivable from the ASN's own content.
