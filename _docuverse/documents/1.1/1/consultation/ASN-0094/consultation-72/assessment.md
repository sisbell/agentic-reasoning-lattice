# Channel Assignment — ASN-0094 review-72

**Date:** 2026-05-25 13:33

## Issue 1: Cross-ASN references to non-foundation ASNs (ASN-0036, ASN-0093)
Reason: Internal organizational decision. The fix is to either declare ASN-0036 and ASN-0093 as additional foundation or scrub non-foundation citations and rely on locally-stated scaffolding clauses; no design-intent or implementation question is needed.

## Issue 2: Redundant restatement of ASN-0086's SubstrateConformingLayer
Reason: Internal duplication removal. ASN-0086's definition already exists; cite by reference and drop the verbatim restatement.

## Issue 3: Meta-prose accretion across multiple sections
Reason: Internal exposition cleanup. The flagged paragraphs explain organizational choices rather than advance claims; cut or compress in place.

## Issue 4: Forward-reference accretion
Reason: Internal restructuring. Either inline deferred content at first use or remove the back-references; both are local edits.

## Issue 5: Sh5 is META; the canonical catalog occupies disproportionate space
Reason: Internal organizational decision. Sh5 self-classifies as META; whether to move catalog/walkthroughs to an appendix or trim to a single instantiation is the author's call, informed by the ASN's own classification.

## Issue 6: Property table reports types without further classification
Reason: Internal. Splitting the table into load-bearing claims and supporting definitions uses information already in the ASN (the type column).

## Issue 7: Lemma — LinkAddressNotPrefixOfEmit could use the simpler freshness route
Reason: Internal proof simplification. ASN-0086's FreshEmissionAddress + R0a-Cor1 already establish that `a_emit(Σ, d) ∉ dom(Σ.L)`, which discharges Case II.A directly; the author can verify against the foundation without external input.

## Issue 8: Definition — FreshEmissionAddress is restated from ASN-0086
Reason: Internal duplication removal. Cite ASN-0086's definition by reference and drop the restatement.

## Issue 9: Definition — RelationalLayer paragraph mixes definition with motivation
Reason: Internal exposition cleanup. The load-bearing NullifyActiveSubsetCompatibility corollary already exists; tighten the surrounding Nullify Compatibility prose to the corollary plus one context paragraph.
