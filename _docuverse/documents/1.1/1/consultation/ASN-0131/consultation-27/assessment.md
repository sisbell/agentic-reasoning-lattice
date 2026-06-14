# Channel Assignment — ASN-0131 review-27

**Date:** 2026-06-13 19:28

## Issue 1: Delete (D-SHIFT) is mislabeled a "domain-growing" displacement
Reason: The correct semantics are already fixed in the cited foundation ASN-0082 — D-SHIFT is its Contraction (domain-shrinking, D-CTG-post), I3 alone is cardinality-preserving (I3-CS), and the insert composite is what grows the domain — and the note already states the load-bearing conclusion (the image swings, "both gains and loses I-addresses"). Correcting the false "domain-growing" attribution and reframing to "content swings through a fixed region" is a relabeling derivable from cited content; no design intent or implementation evidence is at issue.

## Issue 2: "content slid in from before p" is incorrect
Reason: I3-L (ASN-0082, already cited) settles that content at positions `< p` is frame-fixed, and the correct fill-source — inserted content or content displaced up from `v − n ≥ p` — reads directly off I3's rightward shift. The fix is internal to the cited foundation.

## Issue 3: recurring meta-framing that does not advance the argument
Reason: Purely editorial — trim the repeated "alternative implementation would have to honour" motif to a single statement and drop the redundant mid-stability retraction preview. No external fact is required.
