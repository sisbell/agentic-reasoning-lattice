# Channel Assignment — ASN-0118 review-32

**Date:** 2026-06-10 20:11

## Issue 1: V-spec definition silently weakens ASN-0058's ContentReference condition (iii)
Reason: Choosing between inheriting the depth pin and deliberately relaxing it is a design-intent decision the ASN cannot settle internally, and the admissibility of the depth-mismatched example is an empirical question about what the resolver actually accepts — the ASN's existing Gregory citations (acceptablevsa, specset2ispanset) don't specifically address depth mismatch.
Nelson question: Is a span intended to be a pure boundary designator — any pair of tumblers bracketing content, regardless of the depth structure of the positions it captures — or is a span's depth meant to match the addressing depth of the document region it designates?
Gregory question: When a spec's span has a depth (tumbler length) different from the V-position depth of the source's text subspace — e.g., a 3-component start over a depth-2 arrangement — does udanax-green's resolution path (specset2ispanset / acceptablevsa) accept it and resolve by intersection with bound positions, or does any check reject or normalize depth-mismatched spans?

## Issue 2: CP11's multiset gloss contradicts its own formula and the worked example
Reason: Internal fix — the formula and the worked example agree on per-address counting (`⦃d_A, d_A, d_B⦄`), so only the prose gloss needs correcting to match; no design intent or implementation evidence bears on a wording inconsistency.

## Issue 3 (anti-bloat): REPLICATE is defined twice
Reason: Internal fix — purely editorial deduplication; both passages already exist in the ASN, and the consolidation (define once in the transclusion-frame section, reference from the non-contiguous section) requires no external evidence.
