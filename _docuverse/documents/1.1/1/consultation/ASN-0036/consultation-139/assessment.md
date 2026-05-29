# Channel Assignment — ASN-0036 review-139

**Date:** 2026-05-29 00:35

## Issue 1: Deferral prose repeated four times across the S8 region
Reason: Purely editorial deduplication — consolidating a caveat that already exists in the ASN to a single location. No design intent or implementation evidence is involved.

## Issue 2: The general correspondence-run apparatus is unused machinery
Reason: Internal minimality fix — strip unused general-`n` machinery and prove the singleton case the ASN already establishes. Deciding what to defer vs. prove is a structural choice derivable from the existing proof and the spec's own minimality principle.

## Issue 3: "Pairwise disjoint intervals" overstates the proof
Reason: The two repair paths (weaken prose to match the formal claim, or prove interval-level disjointness) both rely only on properties already cited in the proof (T5/T10 subtree containment, same-subspace ordinals). No external channel needed.

## Issue 4: Section-title drift
Reason: A retitle to match the section's sole theorem — entirely internal.
