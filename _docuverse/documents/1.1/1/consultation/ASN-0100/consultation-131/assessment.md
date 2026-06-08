# Channel Assignment — ASN-0100 review-131

**Date:** 2026-06-08 01:09

## Issue 1: "Transfers verbatim" over-reaches the I3 frame
Reason: This is a scoping fix against the cited ASN-0082's I3 lemmas (which depend on the I3-C content frame that INSERT violates) — all the needed facts are in the ASN and its references; no design intent or implementation evidence is required.

## Issue 2: π is defined two incompatible ways in INS.proj
Reason: Pure internal-consistency fix — reconcile the two π definitions into one covering Left, Right, and link-subspace contributions, all already present in the ASN's own derivation.

## Issue 3: Link/entity frame preservation verified redundantly (anti-bloat)
Reason: Editorial deduplication within the ASN; collapsing repeated frame-inheritance prose requires only the ASN's own content, no external channel.

## Issue 4: Roadmap meta-prose in structural slots (anti-bloat)
Reason: Editorial trim — drop the sufficiency-promise sentence and the §Effect One narration already carried by the worked example; entirely internal.
