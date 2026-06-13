# Channel Assignment — ASN-0130 review-25

**Date:** 2026-06-13 05:06

## Issue 1: The note's most novel mechanism — expansion with capture-avoiding renaming — is never concretely demonstrated, and the one example cited for it involves no capture
Reason: The fix is entirely an application of the note's own formal machinery — PR3's expansion procedure, PR-ENC's reserved expansion-name supply, PR3a's typing, and ASN-0129's grammar. Writing `expand(gate)`, constructing a binder-vs-argument capture case, and certifying a reference-bearing definition are mechanical exercises of internal content; no design intent or implementation behavior is at stake (the substitution discipline is standard capture-avoidance, fully specified in-note).

## Issue 2: PR5 re-explains PR-VIEW, carries naming-housekeeping meta-prose, and pre-summarizes a proof it defers downstream
Reason: Pure anti-bloat editorial fix — replace the respelling re-explanation with a PR-VIEW citation, drop "named so uniformly throughout," and remove the PR5→PR5a permanence pre-summary. All targets and their replacements already exist within the note; this is internal prose hygiene requiring no external channel.
