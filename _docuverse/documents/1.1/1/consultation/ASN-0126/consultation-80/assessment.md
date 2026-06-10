# Channel Assignment — ASN-0126 review-80

**Date:** 2026-06-10 01:44

## Issue 1: P5 (and RegisteredAdmissible) are defined after the sections that consume them
Reason: Pure organizational relocation — P5's dependencies (gate, effect-identity, projection bridge, RegisteredAdmissible) are all internal and all established before the projection bridge ends, as the review itself notes. No design intent or implementation evidence bears on where a lemma sits relative to its dependencies.

## Issue 2: The "Existence-of-successor results are excluded" paragraph is method meta-prose plus a use-site inventory
Reason: Anti-bloat deletion of a caveat whose content is already entailed by B2's own scoping clause; the reasoning is entirely about this note's own transfer method. Nothing here turns on what the design intended or what the implementation does.

## Issue 3: The wp "absorption" narration restates inherited conditions to justify their absence
Reason: Expository compression of bookkeeping that re-enumerates L3's clauses (already foundation content in ASN-0043) and the `K ∈ T_admissible` discharge; the collapse uses only material already in the note. No external channel needed.

## Issue 4: The worked illustration omits the "possibly zero targets" Multi case
Reason: The boundary is fully specified by the note's own conformance predicate (`Sh-conf(Multi, F, ∅)` holds) and its "shapes classify registrations, not tuples" claim; the fix constructs a one-line example from addresses and registry types already in the illustration. Derivable from the ASN alone.
