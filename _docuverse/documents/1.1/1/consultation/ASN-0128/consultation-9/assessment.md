# Channel Assignment — ASN-0128 review-9

**Date:** 2026-06-11 01:33

## Issue 1: DR's central derivation rests on an uncited transfer, while the fully-cited alternative is disavowed
Reason: Internal. The note already contains a fully-cited route (R0a via ASN-0126's B2, RP-a, and RP-c); the fix is either to adopt it or to locate the per-state L1/L1b carrier in the cited corpus (ASN-0043/ASN-0126) — a citation-discipline repair within the dependency stack, requiring neither design intent nor implementation evidence.

## Issue 2: I1's irredundant-lists coincidence claim is asserted, not derived
Reason: Internal. The minimal-elements identity and its two-direction proof already exist in I0's text; the fix is to name it as a lemma and write the one-line derivation chain at I1 — pure labeling and citation of content the note already carries.

## Issue 3: retract_stale's counterfactual contradicts the wrapper's stated check discipline
Reason: Internal. The actual design (entry evaluation plus the wrapper's per-call P0 check) is fully specified in BH4 and DR; the fix is to rephrase the counterfactual so it targets a batch admitted only by constituent checks, and to state that both layers check — a wording repair against facts already in the note.

## Issue 4: BH1's rewrite is underspecified under multiple read-filter registrations
Reason: Internal. The Views paragraph's existential phrasing ("when some Unary type registered with BH1…") already commits to union semantics, and mutual filtering follows from "on every other registered type" applied symmetrically; the fix is to make BH1's equation match the commitment the note already makes.

## Issue 5: the example asserts BH3 predicates of a type never registered with BH3
Reason: Internal. The example contradicts the note's own BH3 specification; either declaring `aux2` Binary with BH3 attached or dropping it from the `targets_keyed` output is a one-line consistency fix requiring no external input.

## Issue 6: the same content stated twice — compatibility rationale, and is_in_chain semantics
Reason: Internal. Deduplication of passages the note already contains — choosing one home per fact (R-C0 for the compatibility table, BH4 for the idem=⊥ derivation, BH2 for `is_in_chain`) is editorial restructuring with no new content needed.

## Issue 7: deferral chain around the hit-clause "price"
Reason: Internal. The content is correct and correctly placed at I1 per the review; reducing the three upstream narrations to bare cross-references or deleting them is pure editing.

## Issue 8: recurring importance-announcement rhetoric
Reason: Internal. The review confirms every underlying argument stands without its preamble; deleting the announcement sentences changes no technical content and needs no consultation.
