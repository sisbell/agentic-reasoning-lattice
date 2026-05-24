# Channel Assignment — ASN-0051 review-66

**Date:** 2026-05-17 18:46

## Issue 1: Structural identity formula incorrect in general
Reason: Pure derivation error from the ASN's own definitions of decomposition terms, coverage, and projection. The correct formula `Σ_a (s_a · m_a − 1)` follows directly from counting (span, block) pairs each I-address inhabits; no design intent or implementation evidence is needed.

## Issue 2: Conflation of term-cardinality inflation with term-vs-fragment count gap
Reason: Internal definitional issue — the ASN already distinguishes decomposition terms from maximal fragments, and the gap formula `(m·p) − fragment_count` versus inflation `Σ|term| − |π_text|` is computable from those existing definitions. No external channel required.

## Issue 3: Informal hedge for (m ≥ 4, p = 2) and (m = 2, p ≥ 4) attainment
Reason: The ASN already supplies explicit base witnesses W(2,2), W(3,2), W(2,3) and formal lift schemata (α), (β); extending the schema's stated coverage is a packaging fix internal to the existing proof apparatus. No design intent or implementation evidence is needed.
