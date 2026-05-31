# Channel Assignment — ASN-0093 review-47

**Date:** 2026-05-31 09:04

## Issue 1: The anchor/chain construction is derived three times — and the third derivation both defers to and repeats the first
Reason: Pure editorial deduplication — consolidate the anchor-construction admissibility into FirstEmission and cite it once. No design intent or implementation evidence is at stake; the fix is internal to the note's own structure.

## Issue 2: Justification asides explaining *why* the SubspaceConventionAxiom is invoked, rather than what the step computes
Reason: Removing defensive meta-prose; the anchor forms `b_C(d) = [d.0.s_C]`, `b_L(d) = [d.0.s_L]` already encode the dependency. Purely internal prose trimming, no channel needed.

## Issue 3: Premise inventories duplicated from the lemma bodies into the Properties Introduced table
Reason: Table formatting cleanup — replace use-site premise lists with one-phrase source attributions matching the other rows. The premises already live inline at each lemma; nothing external is required.

## Issue 4: C1b and L1b matrix cells restate the identical content↔link argument in full
Reason: Applying the note's own established content↔link symmetry convention to collapse the L1b cell. Entirely internal; the argument and its substitution pattern are already present in the ASN.
