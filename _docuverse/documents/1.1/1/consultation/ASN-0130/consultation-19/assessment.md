# Channel Assignment — ASN-0130 review-19

**Date:** 2026-06-13 02:58

## Issue 1: The four-verdict distinction is stated three times in PR5a
Reason: Pure exposition cleanup — dropping a redundant re-enumeration and a forward cross-reference within PR5a. The verdict labels are each defined at their own check inside this note; nothing about design intent or implementation behavior is at stake. Internal to the ASN.

## Issue 2: "vacuously violated" is incorrect terminology (PR5)
Reason: A logic-terminology correction; the note's own surrounding prose already establishes that a falsifying witness makes the universal substantively (not vacuously) false, and the review supplies the replacement wording. Derivable from the ASN alone.

## Issue 3: PR5a's checks re-derive PR5's qualifications instead of citing them
Reason: Citation discipline between two sections of the same note — PR5a (ii)/(iii) should state the check and defer the *meaning* to PR5's View/Parameters qualifications. Both paragraphs are present in the ASN; no external evidence needed. Internal to the ASN.

## Issue 4: Navigational meta-prose around the PR0 wp
Reason: Editorial removal of presentation scaffolding ("first/second use of the discipline", self-forward-reference) around the wp derivation; the discipline's role is already inline in the steps. No design-intent or implementation question involved. Internal to the ASN.
