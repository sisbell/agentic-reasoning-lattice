# Channel Assignment — ASN-0100 review-47

**Date:** 2026-06-04 14:48

## Issue 1: §Effect One re-derives a foundation lemma instead of citing it
Reason: The fix is internal — replace the manual three-way reconstruction with a citation to ASN-0093's SubsequentEmissionFreshness (and FirstEmissionFreshness for the boundary), both of which are already in the dependency set. No design intent or implementation evidence is needed to swap a re-derivation for the foundation lemma it duplicates.

## Issue 2: Open Question 6 is already answered in the body
Reason: Internal — §Atomicity already derives the ordering constraint and observability conclusion, so removing or restating the question is a self-contained editorial fix against the ASN's own content.

## Issue 3: Duplicated D-CTG★ closed-interval argument
Reason: Internal — both paragraphs are the same T1-based contradiction argument over generic extremes; factoring it into one lemma and instantiating is derivable from the ASN alone.

## Issue 4: Forward-reference accretion and meta-prose (anti-bloat)
Reason: Internal — stripping use-site inventories, repeated deferrals, downstream-consumer justifications, and fixing the "discharged below" mis-pointer are all editorial operations on existing prose; the correct pointer direction is verifiable within the section.

## Issue 5: Coupling-discharge prose duplicated across sections
Reason: Internal — the J0/J1★/J1'★ argument exists twice (Formal Contract and §Provenance); collapsing the contract slot to an assertion and keeping the proof in §Provenance is a structural move within the ASN, no external input required.
