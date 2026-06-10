# Channel Assignment — ASN-0116 review-52

**Date:** 2026-06-09 18:31

## Issue 1: I-NEW re-derives a disjointness already asserted, wrapped in per-clause attribution
Reason: Pure internal edit. The block-disjointness fact is already stated in the Effect preamble; the fix replaces the re-derivation with a citation of that fact plus its one-line consequence. No design intent or implementation evidence is involved.

## Issue 2: The K.μ⁺ post-state is conflated with the final post-state
Reason: Internal. The error and its correction follow entirely from the ASN's own composite ordering (K.μ⁺ then K.ρ) and the already-stated facts that K.ρ grows `R` and does not touch `M`. The fix is to delete or restate the sentence using content already present.

## Issue 3: PROV claim is mostly commentary on where the work is done and what the claim adds
Reason: Internal. PROV's substance (`R' = R ∪ {(shift(a,k), d)}`, same-composite) is already given by I-PROV; the fix strips the deferral pointer and meta-framing and states the claim directly. No external channel needed.

## Issue 4: OrdinalShift convention enumerates its downstream uses
Reason: Internal editorial trim. Keeping the convention and the two instantiations while dropping the "indexing below invokes it" clause requires nothing beyond the ASN's own text.
