# Channel Assignment — ASN-0043 review-150

**Date:** 2026-05-30 23:45

## Issue 1: Well-definedness of the field projections is re-derived at four sites
Reason: This is a pure restructuring task — consolidate the T4b-domain discharge into L0b and replace the three re-derivations with citations. The argument already exists in the ASN; no design intent or implementation evidence is needed.

## Issue 2: The subspace-disjointness discharge is buried inside L1b, an unrelated claim
Reason: This is an internal relocation — promote the existing disjointness derivation (T7, L0, L0a, L0b, S7b) to a standalone labeled lemma and cite it from its consumers. All the reasoning is already present in the ASN, so neither channel is required.
