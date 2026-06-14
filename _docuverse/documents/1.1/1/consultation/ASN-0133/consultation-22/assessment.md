# Channel Assignment — ASN-0133 review-22

**Date:** 2026-06-14 01:00

## Issue 1: "What this note commits" is a second copy of the note, not an abstract
Reason: Pure reorganization — condense each commitment bullet to a terse pointer and relocate the counterexamples, "foil" framing, and proof sketches to the sections that already own them. Every argument involved is restated verbatim later in the note, so the fix is internal: nothing about design intent or implementation is at stake.

## Issue 2: RG is an overloaded mega-paragraph
Reason: Structural split — keep the rule/registry/fire definitions plus bare H-FIN/H-ATOM statements, move the justifications and pdef discussion to where they are consumed. All content is present in the ASN; deciding where each piece lands is determinable from the note's own dependency structure.

## Issue 3: The H-W foil apparatus is restated three to four times
Reason: De-duplication and a slot-demotion decision (whether Q5 needs a full theorem). The H-W unsatisfiability proof and the foil point are both fully developed in the note already; the fix is to pick one canonical location and reference it elsewhere — no external evidence required.

## Issue 4: Q6 restates the grow-only / reaching-vs-holding split repeatedly within one section
Reason: Internal de-duplication — cases (1)–(3) already establish the split, so the surrounding recapitulation paragraphs can be cut without losing content. Nothing outside the ASN is needed.

## Issue 5: H-SFAIR carries reviser-drift artifacts
Reason: Editorial cleanup against the note's own definitions — the excluded "firing-or-removal-only H-FAIR" aside contradicts this note's three-escape H-FAIR, and the GF-taken requirement is already stated inline, so both the aside and the "repaired here" residue can be cut from the ASN's own content.

## Issue 6: Pervasive "load-bearing, not …" justification tic and downstream-consumer enumerations
Reason: Pure prose editing — drop the rhetorical necessity-announcements (keeping the counterexamples that actually demonstrate necessity), cut the consumer enumerations, and consolidate the scheduler-deferral to one site. All derivable from the note as written.
